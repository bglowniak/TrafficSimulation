import queue
from enum import Enum

class Intersections(Enum):
    TENTH = 0
    ELEVENTH = 1
    TWELFTH = 2
    THIRTEENTH = 3
    FOURTEENTH = 4

class Intersection:
    def __init__(self, intersection_id, green, red):
        # IGNORING YELLOW AND LEFT TURNS FOR NOW, ONLY DOING ONE LANE
        self.intersection_id = intersection_id
        self.stoplight_state = True # True = Green, False = Red
        self.green_duration = green
        self.red_duration = red
        self.lane_queue = Queue()
        self.distance_to_next = 0 # unused for now

    def toggle(self):
        self.stoplight_state = not self.stoplight_state