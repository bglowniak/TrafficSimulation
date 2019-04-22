from random import random

MAX_SPEED = 5
RANDOM_SLOWDOWN = .1

class Vehicle():
    '''
    Class implementing a vehicle (may subclass this later, not sure)

    @attribute enter_time: the simulation time this vehicle entered the simulation
    @attribute speed: how fast the vehicle is currently going
    @attribute max_speed: The maximum speed of this vehicle
    @attribute gap: The gap between this vehicle and the one in front of it
    @attribute source: The source intersection
    @attribute dest: The destination intersection
    '''
    
    def __init__(self, time, speed=0, source=None, dest=None, source_lane=None):
        self.enter_time = time
        self.speed = speed
        self.max_speed = MAX_SPEED
        self.gap = 1
        self.source = source
        self.source_lane = source_lane
        self.dest = dest

    def get_speed(self):
        return self.speed

    def update_speed(self):
        if self.speed < self.max_speed:
            self.speed += 1
        if self.speed > self.gap:
            self.speed = self.gap
        if self.speed > 0 and random() < RANDOM_SLOWDOWN:
            self.speed -= 1
        
    def set_gap(self, gap):
        self.gap = gap

    def get_gap(self):
        return self.gap

    def get_source(self):
        return self.source

    def get_dest(self):
        return self.dest

    def get_enter_time(self):
        return self.enter_time

    def get_source_lane(self):
        return self.source_lane