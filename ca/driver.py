from stoplight import Stoplight
from two_lane import Two_Lane

'''
create a lane with some cars
creates the lane with some stoplights (modified to match real Peachtree street)
'''

s10 = Stoplight(True, 36, 50)
s11 = Stoplight(True, 42, 56)
s12 = Stoplight(True, 62, 36)
s13 = Stoplight(True, 20, 5)
s14 = Stoplight(True, 36, 48)
lights = {20: s10, 40: s11, 80: s12, 110: s13, 140: s14}

road1 = Two_Lane(150, lights)
road1.simulate(1000, 5)

#lane1 = Lane(151)
#lane1.add_stoplights(lights)
#lane1.simulate(500,2)