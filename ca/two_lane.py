from lane import Lane
from cell import Cell
import random


BACK_GAP = 2
LANE_CHANGE_PROB = .5
class Two_Lane():

    def __init__(self, length):
        self.length = length
        self.left_lane = Lane(length)
        self.right_lane = Lane(length)

    def add_stoplights(self, stoplights):
        #stoplights is a dictionary mapping locations to stoplights
        self.left_lane.add_stoplights(stoplights)
        self.right_lane.add_stoplights(stoplights)
    
    def add_light(self, loc, light):
        self.left_lane.add_light(loc, light)
        self.right_lane.add_light(loc, light)

    def timestep_stoplights(self):
        self.right_lane.timestep_stoplights()
    
    def timestep(self):
        '''
        Order? We need to add cars, update gaps, change lanes, update gaps, update speeds, advance vehicles
        '''
        self.right_lane.add_car()
        self.left_lane.add_car()
        
        self.right_lane.update_gaps()
        self.left_lane.update_gaps()

        self.lane_changing()

        self.right_lane.update_gaps()
        self.left_lane.update_gaps()

        self.right_lane.update_vehicle_speeds()
        self.left_lane.update_vehicle_speeds()

        self.right_lane.advance_vehicles()
        self.left_lane.advance_vehicles()

        self.timestep_stoplights()

    def lane_changing(self):
        self.lane_change_helper(self.left_lane, self.right_lane)
        self.lane_change_helper(self.right_lane, self.left_lane)

    def lane_change_helper(self, lane, other_lane):
        vehicles = lane.get_vehicles()
        for loc, vehicle in vehicles.items():
            other_lane_gap = other_lane.check_gap(loc)
            other_lane_back_gap = other_lane.look_back(loc)
            if other_lane_gap > vehicle.get_gap() and other_lane_back_gap >= BACK_GAP and random.random() < LANE_CHANGE_PROB:
                lane.remove_vehicle(loc)
                other_lane.add_vehicle(loc, vehicle)

    def simulate(self, timesteps, freq=1):
        print(self.left_lane)
        print(self.right_lane)
        print('')
        for i in range(timesteps):
            self.timestep()
            if i%freq == 0:
                print(self.left_lane)
                print(self.right_lane)
                print('')
