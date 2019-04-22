from vehicle import Vehicle

class Cell():
    '''
    Class defining a cell, an atomic unit of a lane

    @attribute vehicle: the vehicle this cell contains, may be None
    @attribute stoplight: the stoplight this cell contains, may be None
    '''
    
    def __init__(self):
        self.vehicle = None
        self.stoplight = None
        self.gap = 0

    def has_vehicle(self):
        return self.vehicle is not None
    
    def has_stoplight(self):
        return self.stoplight is not None

    def has_red_stoplight(self):
        if self.stoplight is not None:
            return not self.stoplight.is_green

    def has_green_stoplight(self):
        if self.stoplight is not None:
            return self.stoplight.is_green
        return False

    def has_obstruction(self):
        return self.has_vehicle() or self.has_red_stoplight()

    def has_side_obstruction(self):
        #for a sidestreet checking if it can go
        return self.has_vehicle() or self.has_green_stoplight()

    def set_vehicle(self, v):
        if not isinstance(v, Vehicle):
            raise ValueError('Attempt to set a vehicle to a non-vehicle object')
        self.vehicle = v

    def get_vehicle(self):
        return self.vehicle

    def remove_vehicle(self):
        temp = self.vehicle
        self.vehicle = None
        return temp
    
    def set_stoplight(self, stoplight):
        self.stoplight = stoplight

    def get_stoplight(self):
        return self.stoplight

    def get_gap(self):
        return self.gap
    
    def set_gap(self, gap):
        if gap < 0:
            raise ValueError('Gap must be 0 or more.')
        self.gap = gap
        if self.has_vehicle():
            self.vehicle.set_gap(gap)
