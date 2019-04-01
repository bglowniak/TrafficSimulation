from vehicle import Vehicle
from stoplight import Stoplight
import random
#TODO: this lane either needs traffic lights, or it needs to be connected at the ends somehow
NEW_CAR_PROBABILITY = .85
class Lane():
    '''
    '''

    def __init__(self, length, n_cars, stoplights = {}):
        '''
        length: integer length of the lane
        n_cars: integer number of cars to initialize in the lane
        stoplights: list of integers indicating the locations of the stoplights
        '''
        if (n_cars > length):
            raise ValueError("Number of cars cannot exceed length of the lane!")
        self.length = length
        self.n_cars = n_cars
        self.lane = [None] * length
        self.initialize_vehicles()
        self.stoplights = stoplights
    
    def initialize_vehicles(self):
        locations = random.sample(range(self.length), self.n_cars)
        for position in locations:
            self.lane[position] = Vehicle()
        
    def timestep(self):
        self.update_vehicles()
        for key in self.stoplights.keys():
            self.stoplights[key].timestep()
        new_lane = [None] * self.length
        for position in range(self.length):
            if self.lane[position] is not None:
                speed = self.lane[position].get_speed()
                if position + speed < self.length:
                    new_lane[position + speed] = self.lane[position]
        self.lane = new_lane
        if random.random() < NEW_CAR_PROBABILITY:
            self.lane[0] = Vehicle()

    def update_vehicles(self):
        gap = 5 #initial gap value for last car (maybe this should be the wraparound distance to the first car? something else?)
        #loop backwards through the lane
        #update the gap
        #then update the speed (since you now have the correct gap)
        for position in reversed(range(self.length)):
            if position in self.stoplights:
                if not self.stoplights[position].is_green:
                    gap = 0
            if self.lane[position] is not None:
                self.lane[position].set_gap(gap)
                self.lane[position].update_speed()
                gap = 0
            else:
                gap += 1

    def __str__(self):
        s = ''
        for position in range(self.length):
            if self.lane[position] is not None:
                s += 'X'
            else:
                s += '_'
        for i in range(self.length-1, -1, -1):
            if i in self.stoplights:
                s = s[0:i+1] + '#' + s[i+1:]
        return s
