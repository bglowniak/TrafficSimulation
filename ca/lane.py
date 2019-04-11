from cell import Cell
from vehicle import Vehicle
from stoplight import Stoplight
import random

NEW_CAR_PROBABILITY = .80

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
        #TODO: remove for if has obstruction, and just make it another stoplight
        if self.lane[loc].has_obstruction():
            raise ValueError('Failed to add stoplight; cell is already occupied.')
        self.lane[loc].set_stoplight(light)

    def timestep(self):
        self.add_car()
        self.update_gaps()
        self.change_lanes()
        self.update_vehicle_speeds()
        self.advance_vehicles()
        self.timestep_stoplights()
        
    def add_car(self):
        if random.random() < NEW_CAR_PROBABILITY:
            vehicle = Vehicle()
            self.lane[0].set_vehicle(vehicle)

    def update_gaps(self):
        gap = 5 #allows cars at the end to leave freely
        for cell in reversed(self.lane):
            cell.set_gap(gap)
            if cell.has_obstruction():
                gap = 0
            else:
                gap += 1

    def change_lanes(self):
        pass
    
    def update_vehicle_speeds(self):
        for cell in self.lane:
            if cell.has_vehicle():
                cell.get_vehicle().update_speed()

    def advance_vehicles(self):
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
        for cell in self.lane:
            if cell.has_stoplight():
                cell.get_stoplight().timestep()

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
