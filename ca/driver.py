from stoplight import Stoplight
from two_lane import Two_Lane

'''
create a lane with some cars
creates the lane with some stoplights (modified to match real Peachtree street)
'''

def simulation():
    s10 = Stoplight(True, 36, 50)
    s11 = Stoplight(True, 42, 56)
    s12 = Stoplight(True, 62, 36)
    s13 = Stoplight(True, 20, 3)
    s14 = Stoplight(True, 36, 48)
    lights = {10: s10, 35: s11, 61: s12, 81: s13, 101: s14}



    road1 = Two_Lane(111, lights)
    road1.simulate(2000, 100, False)
    return road1.stats.vehicle_traversal_times

if __name__ == '__main__':
    simulation()
