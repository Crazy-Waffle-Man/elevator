import elevator_lib
import threading
from typing import List

#this will be the same as stupid_elevator.py, but with changes to the elevator logic

elevator_lib.building.elevators[0].served_floors = [1, 2]
elevator_lib.building.elevators[1].served_floors = [3, 4]
elevator_lib.building.elevators[2].served_floors = [5, 6]
elevator_lib.building.elevators[3].served_floors = [1, 2, 3, 4, 5, 6]
# Experiment with different served floors for each elevator

def better_elevator_behavior(elevator: elevator_lib.Elevator):
    while True:
        if len(elevator.people) == 0:
            #Go to ground floor and wait
            elevator.travel(0)
            
            # Load people from ground floor

            if len(elevator_lib.building.people) > 0:
                with threading.Lock():
                    elevator_lib.building.smart_load_elevator(elevator)
                    #sort people by floor from least to greatest
                    elevator.people.sort(key=lambda p: p.floor)
            else:
                break


        else:
            for person in elevator.people:
                person.push_elevator_button(elevator)


def go(function = elevator_lib.elevator_behavior):
    elevator_threads: List[threading.Thread] = []

    for elevator in elevator_lib.building.elevators:
        print("Elevator started")
        t = threading.Thread(target= function, args=(elevator,))
        elevator_threads.append(t)
        t.start()

    for t in elevator_threads: t.join() # Wait for all elevators to finish
    elevator_lib.total_travel_time /= 4
    travel_hours = int(elevator_lib.total_travel_time // 3600)
    travel_minutes = int((elevator_lib.total_travel_time // 60)%60)
    elevator_lib.total_travel_time %= 60
    print(f"total travel time: {travel_hours}:{travel_minutes}:{elevator_lib.total_travel_time}")

go(better_elevator_behavior)