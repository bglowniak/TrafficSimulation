# des-simulation.py initializes the simulation based on inputted parameters, maintains the queues of each intersection, and creates and schedules events
# simulation state variables and initialization

# also schedules vehicle entrances at certain times

from enum import Enum

class Intersections(Enum):
    TENTH = 0
    ELEVENTH = 1
    TWELFTH = 2
    THIRTEENTH = 3
    FOURTEENTH = 4

class TrafficSimulation:
    def __init__(self):
        print("woot")