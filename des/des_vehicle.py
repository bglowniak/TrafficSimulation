# vehicle class, keeps track of arrival time and exit time

from des_engine import Intersection

class Vehicle:
    def __init__(self, enter_time, enter_location, exit_location):
        # the timestamp when the vehicle enters the simulation
        self.enter_time = enter_time

        # the timestamp when the vehicle exits the simulation (starts off undefined)
        self.exit_time = None

        # the intersection which the vehicle entered from
        self.entrance = enter_location

        # the intersection which the vehicle will exit from
        self.exit = exit_location

        # for the checkpoint, this is unused
        self.speed = 0


    def calc_travel_time():
        if exit_time != None:
            return self.exit_time - self.enter_time
        else:
            return -1
