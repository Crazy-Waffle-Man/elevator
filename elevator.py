from time import sleep
from typing import List
import threading
from random import shuffle


TIME_DILATION = 600 #run elevators at 10 minutes per second


class Person:
    
    def __init__(self, floor: int):
        self.floor: int = floor
        self.in_elevator: bool = False
        self.elevator_in: List['Elevator'] = [] # not in an elevator yet, use a list so we can have them in no elevator.
    def __repr__(self) -> str:
        return f"Person(floor={self.floor}, in_elevator={self.in_elevator})"
    def push_elevator_button(self, elevator: 'Elevator') -> None: # so that we can use Elevator before definition
        elevator.travel(self.floor)
    
class Elevator:
    
    def __init__(self):
        self.capacity: int = 10
        self.current_floor: int = 0
        self.people: List[Person] = []
    
    
    def add_person(self, person: Person) -> bool:
        if (len(self.people) < self.capacity) and not person.in_elevator:
            self.people.append(person)
            person.in_elevator = True
            person.elevator_in = [self]
            return True
        else: return False

    
    def travel(self, floor: int) -> None:
        global total_travel_time
        travel_time = abs(self.current_floor - floor) * 5
        with threading.Lock():
            total_travel_time += travel_time
        self.current_floor = floor
        sleep(travel_time / TIME_DILATION)
        self.stop()
    
    
    def stop(self):
        global total_travel_time
        for person in self.people:
            if person.floor == self.current_floor:
                person.in_elevator = False
        self.people = [p for p in self.people if p.in_elevator]
        sleep(8 / TIME_DILATION)
        with threading.Lock():
            total_travel_time += 8


class Building:
    
    def __init__(self, num_elevators: int = 4):
        self.elevators: List[Elevator] = [Elevator() for _ in range(num_elevators)]
        self.people: List[Person] = []
        for _ in range(100):
            self.people.append(Person(1))
        for _ in range(120):
            self.people.append(Person(2))
        for _ in range(60):
            self.people.append(Person(3))
        for _ in range(120):
            self.people.append(Person(4))
        for _ in range(80):
            self.people.append(Person(5))
        for _ in range(20):
            self.people.append(Person(6))
        #shuffle the people
        shuffle(self.people)

    
    def load_elevator(self, elevator: Elevator) -> None:
        new_self_people = self.people.copy() #We do this so that we can modify self.people during iteration.
        for person in self.people:
            if len(elevator.people) < elevator.capacity and elevator.current_floor == 0:
                elevator.add_person(person)
                #Remove person from building list
                new_self_people.remove(person)
            else:
                break
        self.people = new_self_people
        print(f"An elevator has been loaded. There are {len(self.people)} people left on the ground floor.")
    
    def load_all_elevators(self) -> None:
        for elevator in self.elevators:
            self.load_elevator(elevator)

building = Building()

#main loop

def elevator_behavior(elevator: Elevator):
    global building
    while True:
        if len(elevator.people) == 0:
            #Go to ground floor and wait
            elevator.travel(0)
            
            # Load people from ground floor

            if len(building.people) > 0:
                with threading.Lock():
                    building.load_elevator(elevator)
            else:
                break


        else:
            for person in elevator.people:
                person.push_elevator_button(elevator)


total_travel_time= 0

elevator_threads: List[threading.Thread] = []

for elevator in building.elevators:
    print("elevator started")
    t = threading.Thread(target=elevator_behavior, args=(elevator,))
    elevator_threads.append(t)
    t.start()

for t in elevator_threads: t.join() # Wait for all elevators to finish
travel_hours = total_travel_time // 3600
travel_minutes = (total_travel_time // 60)%60
total_travel_time %= 60
print(f"total travel time: {travel_hours}:{travel_minutes}:{total_travel_time}")