from stoplight import Stoplight
from lane import Lane

'''
create a lane with some cars


'''
s10 = Stoplight(True, 36, 50)
s11 = Stoplight(True, 42, 56)
s12 = Stoplight(True, 62, 36)
s14 = Stoplight(True, 36, 48)
'''
s10 = Stoplight(True)
s11 = Stoplight(True)
s12 = Stoplight(True)
s14 = Stoplight(True)'''
lane1 = Lane(201, 30, {30: s10, 90: s11, 150: s12, 200: s14})
print(lane1)
for i in range(500):
    lane1.timestep()
    if i > 100 and i%2 == 0:
        print(lane1)