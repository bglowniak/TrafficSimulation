from stoplight import Stoplight
from lane import Lane

'''
create a lane with some cars
creates the lane with some stoplights (modified to match real Peachtree street)
'''

s10 = Stoplight(True, 36, 50)
s11 = Stoplight(True, 42, 56)
s12 = Stoplight(True, 62, 36)
s14 = Stoplight(True, 36, 48)

lane1 = Lane(201)
lights = {30: s10, 90: s11, 150: s12, 200: s14}
lane1.add_stoplights(lights)

print(lane1)
for i in range(500):
    lane1.timestep()
    if i > 100 and i%2 == 0:
        print(lane1)
