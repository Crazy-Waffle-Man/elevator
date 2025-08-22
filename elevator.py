from time import sleep

from typing import List
import logging
import threading





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
        travel_time = (self.current_floor - floor) * 5
        with threading.Lock():
            total_travel_time += abs(travel_time)
        self.current_floor = floor
        sleep(abs(travel_time) // 5)
        self.stop()
    
    
    def stop(self):
        for person in self.people:
            if person.floor == self.current_floor:
                person.in_elevator = False
        self.people = [p for p in self.people if p.in_elevator]


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

    
    def load_elevator(self, elevator_index: int) -> None:
        new_self_people = self.people.copy() #We do this so that we can modify self.people during iteration.
        for person in self.people:
            if len(self.elevators[elevator_index].people) < self.elevators[elevator_index].capacity and self.elevators[elevator_index].current_floor == 0:
                self.elevators[elevator_index].add_person(person)
                #Remove person from building list
                new_self_people.remove(person)
            else:
                break
        self.people = new_self_people
    
    def load_all_elevators(self) -> None:
        for i in range(len(self.elevators)):
            self.load_elevator(i)

building = Building()

#main loop

def elevator_behavior(elevator: Elevator):
    while True:
        if len(elevator.people) == 0:
            #Go to ground floor and wait
            elevator.travel(0)
            break
        else:
            for person in elevator.people:
                person.push_elevator_button(elevator)


total_travel_time= 0

while len(building.people) > 0:
    building.load_all_elevators()
    threads: List[threading.Thread] = []
    for i, elevator in enumerate(building.elevators):
        threads.append(threading.Thread(target=elevator_behavior, args=(elevator,)))
        threads[i].start()
    for thread in threads: thread.join()
    print(len(building.people), "left on the ground floor.")

print(f"Total travel time: {total_travel_time} seconds.")