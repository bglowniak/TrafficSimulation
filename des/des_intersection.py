from queue import Queue
from enum import Enum

# define an enum for our discrete set of intersections
class Intersections(Enum):
    TENTH = "10th"
    ELEVENTH = "11th"
    TWELFTH = "12th"
    THIRTEENTH = "13th"
    FOURTEENTH = "14th"

# we will represent our simulation as a chain of intersections (think nodes in a network)
class Intersection:
    def __init__(self, intersection_id, green, red):
        # IGNORING YELLOW AND LEFT TURNS FOR NOW, ONLY DOING ONE LANE
        self.intersection_id = intersection_id
        self.stoplight_state = True # True = Green, False = Red
        self.green_duration = green
        self.red_duration = red
        self.lane_queue = Queue()
        self.distance_to_next = 0 # unused for now

    # eventually will implement state machine for each intersection (LT and TR?)
    def toggle(self):
        self.stoplight_state = not self.stoplight_state

    def get_state(self):
        return self.stoplight_state

    def get_green_duration(self):
        return self.green_duration

    def get_red_duration(self):
        return self.red_duration

    def queue_vehicle(self, vehicle):
        self.lane_queue.put(vehicle)

    def next_intersection(self):
        if self.intersection_id is Intersections.FOURTEENTH:
            return None
        else:
            return Intersections(self.intersection_id.value + 1)

# instantiate intersections in dictionary for use by other modules
intersection_list = {
    Intersections.TENTH: Intersection(Intersections.TENTH, 10, 10),
    Intersections.ELEVENTH: Intersection(Intersections.ELEVENTH, 10, 10),
    Intersections.TWELFTH: Intersection(Intersections.TWELFTH, 10, 10),
    Intersections.THIRTEENTH: Intersection(Intersections.THIRTEENTH, 0, 0),
    Intersections.FOURTEENTH: Intersection(Intersections.FOURTEENTH, 10, 10)
}