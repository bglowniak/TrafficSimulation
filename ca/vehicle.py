from random import random

MAX_SPEED = 5
RANDOM_SLOWDOWN = .1

class Vehicle():
    '''
    Class implementing a vehicle (may subclass this later, not sure)

    @attribute speed: how fast the vehicle is currently going
    @attribute max_speed: The maximum speed of this vehicle
    @attribute gap: The gap between this vehicle and the one in front of it
    '''
    
    def __init__(self):
        self.speed = 0
        self.max_speed = MAX_SPEED
        self.gap = 1

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
