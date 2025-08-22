from typing import List
import threading
from elevator_lib import *







building = Building()

#main loop



elevator_threads: List[threading.Thread] = []

for elevator in building.elevators:
    print("Elevator started")
    t = threading.Thread(target=elevator_behavior, args=(elevator,))
    elevator_threads.append(t)
    t.start()

for t in elevator_threads: t.join() # Wait for all elevators to finish
total_travel_time /= 4
travel_hours = int(total_travel_time // 3600)
travel_minutes = int((total_travel_time // 60)%60)
total_travel_time %= 60
print(f"total travel time: {travel_hours}:{travel_minutes}:{total_travel_time}")
