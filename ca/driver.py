from stoplight import Stoplight
from lane import Lane
from two_lane import Two_Lane

'''
create a lane with some cars
creates the lane with some stoplights (modified to match real Peachtree street)
'''

s10 = Stoplight(True, 36, 50)
s11 = Stoplight(True, 42, 56)
s12 = Stoplight(True, 62, 36)
s14 = Stoplight(True, 36, 48)
lights = {40: s10, 80: s11, 110: s12, 150: s14}

#road1 = Two_Lane(151)
#road1.add_stoplights(lights)
#road1.simulate(500, 4)

lane1 = Lane(151)
lane1.add_stoplights(lights)
lane1.simulate(500,2)