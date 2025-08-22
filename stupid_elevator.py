from typing import List
import threading
import elevator_lib

#main loop, use for running the default


test_results: List[float] = []

def go(function = elevator_lib.elevator_behavior):
    elevator_threads: List[threading.Thread] = []

    for elevator in elevator_lib.building.elevators:
        print("Elevator started")
        t = threading.Thread(target = function, args=(elevator,))
        elevator_threads.append(t)
        t.start()

    for t in elevator_threads: t.join() # Wait for all elevators to finish
    
def parse_time():
    test_results.append(elevator_lib.total_travel_time)
    elevator_lib.total_travel_time /= 4
    travel_hours = int(elevator_lib.total_travel_time // 3600)
    travel_minutes = int((elevator_lib.total_travel_time // 60)%60)
    elevator_lib.total_travel_time %= 60
    print(f"total travel time: {travel_hours}:{travel_minutes}:{elevator_lib.total_travel_time}")


for _ in range(20):
    elevator_lib.building.__init__()
    go()
    parse_time()


for result in test_results:
    result /= 4 # 4 elevators each individually added time