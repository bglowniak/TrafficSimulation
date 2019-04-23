# vehicle class, keeps track of arrival time and exit time
from des_intersection import Intersections, Directions, Lanes

class Vehicle:
    vehicle_num = 0
    def __init__(self, enter_time=0.0,
                 velocity=25.0,
                 enter_location=0,
                 exit_location=6,
                 direction=Directions.NORTH,
                 lane=Lanes.LEFT):
        # id to associate with vehicle
        self.vehicle_id = Vehicle.vehicle_num
        Vehicle.vehicle_num += 1

        # the timestamp when the vehicle enters the simulation
        self.enter_time = enter_time

        # the timestamp when the vehicle exits the simulation (starts off undefined)
        self.exit_time = None

        # the intersection which the vehicle entered from
        self.entrance = enter_location

        # the intersection which the vehicle will exit from
        self.exit = exit_location

        # the speed of the vehicle in MPH
        self.velocity = velocity

        # True for Northbound, False for E/W
        self.direction = direction

        # True for left, False for right
        self.lane = lane

    def get_id(self):
        return self.vehicle_id

    def set_exit_time(self, time):
        self.exit_time = time

    def calc_total_time(self):
        if self.exit_time != None:
            return self.exit_time - self.enter_time
        else:
            return -1

    def turn_north(self):
        self.direction = Directions.NORTH

    # returns the time in seconds it takes to travel a certain distance
    def calc_travel_time(self, distance):
        hours = distance / self.velocity
        return hours * 3600

    def __str__(self):
        return "Vehicle(enter_time=" + str(self.enter_time) + " velocity=" + str(self.velocity) + " entrance=" + str(self.entrance) + " exit=" + str(self.exit) + " direction=" + str(self.direction) + " lane=" + str(self.lane) + ")"

