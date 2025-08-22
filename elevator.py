from time import sleep
from typing import List
import logging


def info(func):
    def wrapper(*args, **kwargs):
        logging.info(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        logging.info(f"{func.__name__} completed")
        return result
    return wrapper


class Person:
    @info
    def __init__(self, floor: int):
        self.floor: int = floor
        self.in_elevator: bool = False
    def __repr__(self) -> str:
        return f"Person(floor={self.floor}, in_elevator={self.in_elevator})"
    
class Elevator:
    @info
    def __init__(self):
        self.capacity: int = 10
        self.current_floor: int = 0
        self.people: List[Person] = []
    
    @info
    def add_person(self, person: Person) -> bool:
        if (len(self.people) < self.capacity) and not person.in_elevator:
            self.people.append(person)
            person.in_elevator = True
            return True
        else: return False

    @info
    def travel(self, floor: int) -> None:
        travel_time = (self.current_floor - floor) * 5
        self.current_floor = floor
        sleep(abs(travel_time))
        self.stop()
    
    @info
    def stop(self):
        for person in self.people:
            if person.floor == self.current_floor:
                person.in_elevator = False
        self.people = [p for p in self.people if p.in_elevator]


class Building:
    @info
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

    @info
    def load_elevator(self, elevator_index: int) -> None:
        new_self_people = self.people.copy() #We do this so that we can modify self.people during iteration.
        for person in self.people:
            if self.elevators[elevator_index].add_person(person) and self.elevators[elevator_index].current_floor == 0:
                #Remove person from building list
                new_self_people.remove(person)
            else:
                break
        self.people = new_self_people
    
    def load_all_elevators(self) -> None:
        for i in range(len(self.elevators)):
            self.load_elevator(i)

building = Building()

