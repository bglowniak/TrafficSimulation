from stoplight import Stoplight
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
'''
road1 = Two_Lane(151)
road1.add_stoplights(lights)
road1.simulate(100, 1)'''
'''
s1 = Stoplight(True, 10, 5)
road2 = Two_Lane(15)
road2.add_light(10, s1)
road2.simulate(15, 1)'''

road3 = Two_Lane(40, {20: Stoplight()})
road3.simulate(50)

#lane1 = Lane(151)
#lane1.add_stoplights(lights)
#lane1.simulate(500,2)