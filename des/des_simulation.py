# des_simulation.py initializes the simulation based on inputted parameters, maintains the queues of each intersection, and creates and schedules events
# simulation state variables and initialization

import time
from des_engine import run_simulation, simulation_time, schedule_event
from des_events import *
from des_intersection import *

# schedule first event
#first_event = IntersectionArrival(current_time(), Intersections.TENTH)
#schedule_event(0.0, first_event)

first_event = StoplightChange(simulation_time(), Intersections.TENTH)
schedule_event(simulation_time(), first_event)

start_time = time.time()
run_simulation()
end_time = time.time()

print(end_time - start_time)