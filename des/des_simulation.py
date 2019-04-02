# des_simulation.py initializes the simulation based on inputted parameters, maintains the queues of each intersection, and creates and schedules events
# simulation state variables and initialization

import time
import random
from des_engine import run_simulation, simulation_time, schedule_event
from des_events import *
from des_intersection import *
from des_vehicle import *

#schedule stoplight changes (13th has no stoplight)
schedule_event(StoplightChange(simulation_time(), Intersections.TENTH))
schedule_event(StoplightChange(simulation_time(), Intersections.ELEVENTH))
schedule_event(StoplightChange(simulation_time(), Intersections.TWELFTH))
schedule_event(StoplightChange(simulation_time(), Intersections.FOURTEENTH))

first_vehicle = Vehicle(enter_time=simulation_time())
schedule_event(IntersectionArrival(simulation_time(), Intersections.TENTH, first_vehicle))

start_time = time.time()
run_simulation()
end_time = time.time()

print(end_time - start_time)