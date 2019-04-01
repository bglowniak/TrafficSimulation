# des-simulation.py initializes the simulation based on inputted parameters, maintains the queues of each intersection, and creates and schedules events
# simulation state variables and initialization

from des_engine import run_simulation, current_time, schedule_event
from des_events import *
from des_intersection import *
import time

first_event = IntersectionArrival(current_time(), Intersections.TENTH)
schedule_event(first_event)

start_time = time.time()
run_simulation()
end_time = time.time()

print(end_time - start_time)