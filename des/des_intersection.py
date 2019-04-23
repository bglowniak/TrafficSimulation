# des_intersection defines intersection-related utilities and variables (stoplight timings, inter-distances, etc.). It also defines the intersection list that events interact with.

from queue import Queue
from enum import Enum

# define an enum for our discrete set of intersections
class Intersections(Enum):
    TENTH = 1
    ELEVENTH = 2
    TWELFTH = 3
    THIRTEENTH = 4
    FOURTEENTH = 5

# we will represent our simulation as a chain of intersections (nodes in a network)
class Intersection:
    def __init__(self, intersection_id, green, red, distance_to_next):
        # IGNORING YELLOW AND LEFT TURNS
        self.intersection_id = intersection_id
        self.stoplight_state = True # True = Green, False = Red
        self.green_duration = green
        self.red_duration = red

        # define lane queues
        self.left_lane_queue = Queue() # Northbound, Left
        self.right_lane_queue = Queue() # Northbound, Right
        self.ew_queue = Queue() # E/W, Left
        self.ew_right_queue = Queue() # E/W, Right

        self.distance_to_next = distance_to_next

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

    def num_queueing(self):
        return self.lane_queue.qsize()

    def dequeue_vehicle(self):
        if self.lane_queue.empty():
            return None

        return self.lane_queue.get()

    def next_intersection(self):
        if self.intersection_id is Intersections.FOURTEENTH:
            return None
        else:
            return Intersections(self.intersection_id.value + 1)

    def get_distance_to_next(self):
        return self.distance_to_next

# taken from signalTimings.xls from the NGSIM dataset. These durations only reflect the Northbound TR component.
# green_duration = Green TR + 0.5 * Yellow TR
# red_duration = Red TR + 0.5 * Yellow TR
# adding half the Yellow TR accounts for how some cars may stop and some may continue when a light is yellow

tenth_green_duration = 36.5
tenth_red_duration = 51.1

eleventh_green_duration = 43.1
eleventh_red_duration = 57

twelfth_green_duration = 62.5
twelfth_red_duration = 37.3

fourteenth_green_duration = 36.2
fourteenth_red_duration = 47.7

# distances (in miles) were determined by using online mapping tools
tenth_to_eleventh = 0.1056
eleventh_to_twelfth = 0.0870
twelfth_to_thirteenth = 0.0808
thirteenth_to_fourteenth = 0.0746

# instantiate intersections in dictionary for use by other modules
intersection_list = {
    Intersections.TENTH: Intersection(Intersections.TENTH,
                                      tenth_green_duration,
                                      tenth_red_duration,
                                      tenth_to_eleventh),

    Intersections.ELEVENTH: Intersection(Intersections.ELEVENTH,
                                         eleventh_green_duration,
                                         eleventh_red_duration,
                                         eleventh_to_twelfth),

    Intersections.TWELFTH: Intersection(Intersections.TWELFTH,
                                        twelfth_green_duration,
                                        twelfth_red_duration,
                                        twelfth_to_thirteenth),

    Intersections.THIRTEENTH: Intersection(Intersections.THIRTEENTH, 0, 0,
                                           thirteenth_to_fourteenth),

    Intersections.FOURTEENTH: Intersection(Intersections.FOURTEENTH,
                                           fourteenth_green_duration,
                                           fourteenth_red_duration, 0)
}