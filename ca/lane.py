from cell import Cell
from vehicle import Vehicle
from stoplight import Stoplight
import random

NEW_CAR_PROBABILITY = .30

class Lane():
    '''
    Class describing behavior of a lane for vehicles

    list lane: list of cells that may contain vehicles or stoplights or neither
    integer length: length of the lane in number of cells
    '''

    def __init__(self, length):
        '''
        integer length: length in cells of the lane
        '''
        if length < 1:
            raise ValueError('Length of lane must be greater than one.')
        self.length = length
        self.lane = self.make_lane()

    def make_lane(self):
        lane = []
        for i in range(self.length):
            lane.append(Cell())
        return lane

    def add_stoplights(self, stoplights):
        #stoplights is a dictionary mapping locations to stoplights
        for loc in stoplights.keys():
            self.add_light(loc, stoplights[loc])
    
    def add_light(self, loc, light):
        if self.lane[loc].has_stoplight():
            raise ValueError('Failed to add stoplight; cell is already has stoplight.')
        self.lane[loc].set_stoplight(light)

    def timestep(self):
        #unique to a one lane road
        self.add_car()
        self.update_gaps()
        self.update_vehicle_speeds()
        self.advance_vehicles()
        self.timestep_stoplights()
        
    def add_car(self, pos=0, prob=NEW_CAR_PROBABILITY):
        if self.lane[pos].has_vehicle():
            return False
        if random.random() < prob:
            vehicle = Vehicle()
            self.lane[pos].set_vehicle(vehicle)

    def update_gaps(self):
        gap = 5 #allows cars at the end to leave freely
        for cell in reversed(self.lane):
            cell.set_gap(gap)
            if cell.has_obstruction():
                gap = 0
            else:
                gap += 1

    def look_back(self, loc):
        if loc >= self.length:
            raise ValueError("Out of bounds error, cannot check gap outside range of lane length.")
        count = -1
        while loc >= 0:
            if self.lane[loc].has_vehicle():
                return count
            count += 1
            loc -= 1
        return count

    def check_gap(self, loc):
        if loc >= self.length:
            raise ValueError("Out of bounds error, cannot check gap outside range of lane length.")
        return self.lane[loc].get_gap()

    def remove_vehicle(self, loc):
        if loc >= self.length:
            raise ValueError("Out of bounds error, cannot check gap outside range of lane length.")
        if not self.lane[loc].has_vehicle():
            raise ValueError("Lane at location {} does not have a vehicle to remove.".format(loc))
        return self.lane[loc].remove_vehicle()
        
    def add_vehicle(self, loc, vehicle):
        if loc >= self.length:
            raise ValueError("Out of bounds error, cannot check gap outside range of lane length.")
        if self.lane[loc].has_vehicle():
            raise ValueError("Cannot add vehicle where there is already another vehicle.")
        self.lane[loc].set_vehicle(vehicle)
    
    def get_vehicles(self):
        vehicles = {}
        for i in range(self.length):
            if self.lane[i].has_vehicle():
                vehicles.update({i: self.lane[i].get_vehicle()})
        return vehicles
    
    def update_vehicle_speeds(self):
        for cell in self.lane:
            if cell.has_vehicle():
                cell.get_vehicle().update_speed()

    def advance_vehicles(self):
        #TODO: could add a number of cars left the system and system time metric in this method
        vehicle_list = {}
        for i in range(self.length):
            if self.lane[i].has_vehicle():
                vehicle = self.lane[i].remove_vehicle()
                loc = i + vehicle.get_speed()
                vehicle_list.update({loc: vehicle})
        for loc, vehicle in vehicle_list.items():
            if loc < self.length:
                self.lane[loc].set_vehicle(vehicle)

    def timestep_stoplights(self):
        for i in range(self.length):
            if self.lane[i].has_stoplight():
                self.lane[i].get_stoplight().timestep()
                if not self.lane[i].get_stoplight().is_green:
                    self.add_car(i, self.lane[i].get_stoplight().get_input_prob())

    def __str__(self):
        s = ''
        for cell in self.lane:
            if cell.has_stoplight() and cell.has_vehicle():
                s += '|X|'
            elif cell.has_stoplight():
                s += '| |'
            elif cell.has_vehicle():
                s += 'X'
            else:
                s += '_'
        return s
