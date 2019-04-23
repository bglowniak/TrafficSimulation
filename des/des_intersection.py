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


class Lanes(Enum):
    LEFT = True
    RIGHT = False

class Directions(Enum):
    NORTH = True
    EW = False

# we will represent our simulation as a chain of intersections (nodes in a network)
class Intersection:
    def __init__(self, intersection_id, green, red, distance_to_next, length):
        # IGNORING YELLOW AND LEFT TURNS
        self.intersection_id = intersection_id
        self.stoplight_state = True # True = Green, False = Red
        self.green_duration = green
        self.red_duration = red
        self.length = length

        # define lane queues
        self.north_left_queue = Queue() # Northbound, Left
        self.north_right_queue = Queue() # Northbound, Right
        self.ew_left_queue = Queue() # E/W, Left
        self.ew_right_queue = Queue() # E/W, Right

        self.distance_to_next = distance_to_next

        self.last_left_departure_time = 0.0
        self.last_right_departure_time = 0.0

    # eventually will implement state machine for each intersection (LT and TR?)
    def toggle(self):
        self.stoplight_state = not self.stoplight_state

    def get_state(self):
        return self.stoplight_state

    def get_green_duration(self):
        return self.green_duration

    def get_red_duration(self):
        return self.red_duration

    def queue_vehicle(self, vehicle, lane, direction):
        if direction and lane: # northbound left
            self.north_left_queue.put(vehicle)
        elif direction and not lane: # northbound right
            self.north_right_queue.put(vehicle)
        elif not direction and lane: # EW left
            self.ew_left_queue.put(vehicle)
        elif not direction and not lane: # EW right
            self.ew_right_queue.put(vehicle)

    def num_queueing(self, lane, direction):
        if direction and lane: # northbound left
            return self.north_left_queue.qsize()
        elif direction and not lane: # northbound right
            return self.north_right_queue.qsize()
        elif not direction and lane: # EW left
            return self.ew_left_queue.qsize()
        elif not direction and not lane: # EW right
            return self.ew_right_queue.qsize()

    def dequeue_vehicle(self, lane, direction):
        try:
            if direction and lane: # northbound left
                return self.north_left_queue.get()
            elif direction and not lane: # northbound right
                return self.north_right_queue.get()
            elif not direction and lane: # EW left
                return self.ew_left_queue.get()
            elif not direction and not lane: # EW right
                return self.ew_right_queue.get()
        except Queue.Empty:
            return None

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

# section distances (in miles) were pulled from TrajectoryDataDescription.pdf
tenth_to_eleventh = 0.0814
eleventh_to_twelfth = 0.0781
twelfth_to_thirteenth = 0.0668
thirteenth_to_fourteenth = 0.0652

# intersection lengths (also pulled from TrajectoryDataDescription)
tenth_length = 0.0189
eleventh_length = 0.0246
twelfth_length = 0.0140
thirteenth_length = 0.0126
fourteenth_length = 0.0226

# instantiate intersections in dictionary for use by other modules
intersection_list = {
    Intersections.TENTH: Intersection(Intersections.TENTH,
                                      tenth_green_duration,
                                      tenth_red_duration,
                                      tenth_to_eleventh,
                                      tenth_length),

    Intersections.ELEVENTH: Intersection(Intersections.ELEVENTH,
                                         eleventh_green_duration,
                                         eleventh_red_duration,
                                         eleventh_to_twelfth,
                                         eleventh_length),

    Intersections.TWELFTH: Intersection(Intersections.TWELFTH,
                                        twelfth_green_duration,
                                        twelfth_red_duration,
                                        twelfth_to_thirteenth,
                                        twelfth_length),

    Intersections.THIRTEENTH: Intersection(Intersections.THIRTEENTH, 0, 0,
                                           thirteenth_to_fourteenth,
                                           thirteenth_length),

    Intersections.FOURTEENTH: Intersection(Intersections.FOURTEENTH,
                                           fourteenth_green_duration,
                                           fourteenth_red_duration, 0,
                                           fourteenth_length)
}