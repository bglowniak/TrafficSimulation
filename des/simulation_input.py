import math
import random


# ======= CONTINUOUS DISTRIBUTIONS =======

# see Input Analysis.ipynb for explanation of how these distributions are generated
# each distribution is formatted as (y_i, F(y_i)), where y_i is the edge of each bin, and F(y_i) is the cdf.
interarrival_emp_dist = [(0.0, 0), (1746.1538461538462, 0.5222929936305732), (3492.3076923076924, 0.7579617834394905), (5238.461538461539, 0.8471337579617835), (6984.615384615385, 0.89171974522293), (8730.76923076923, 0.9171974522292994), (10476.923076923078, 0.9490445859872612), (12223.076923076924, 0.9681528662420382), (13969.23076923077, 0.9681528662420382), (15715.384615384615, 0.9808917197452229), (17461.53846153846, 0.9872611464968153), (19207.69230769231, 0.9872611464968153), (20953.846153846156, 0.9936305732484076), (22700.0, 1.0)]

interarrival_mean = 2895.541401273885

vel_emp_dist = [(0.0, 0), (4.095384615384615, 0.01910828025477707), (8.19076923076923, 0.01910828025477707), (12.286153846153846, 0.01910828025477707), (16.38153846153846, 0.07643312101910828), (20.47692307692308, 0.19745222929936307), (24.572307692307692, 0.30573248407643316), (28.667692307692306, 0.3694267515923567), (32.76307692307692, 0.4140127388535032), (36.85846153846154, 0.4394904458598726), (40.95384615384616, 0.5222929936305732), (45.04923076923077, 0.6624203821656051), (49.144615384615385, 0.7770700636942675), (53.24, 1.0)]

# compute x given two points and a y value
def interpolate(point1, point2, y):
    x_0 = point1[0]
    y_0 = point1[1]
    x_1 = point2[0]
    y_1 = point2[1]

    return x_0 + ((y - y_0) * (x_1 - x_0)) / (y_1 - y_0)

def compute_from_emp_dist(emp_dist):
    rand = random.uniform(0, 1)

    # find correct bin
    idx = 0
    while idx < len(emp_dist) and rand > emp_dist[idx][1]:
        idx += 1

    return interpolate(emp_dist[idx - 1], emp_dist[idx], rand)

def compute_from_exp(mean):
    rand = random.uniform(0, 1)

    if rand == 1: return 0

    return -mean * math.log(1 - rand)

# returns interarrival in seconds
def compute_interarrival(exp=False, sf=1):
    if sf == 0:
        raise ValueError("Scale Factor cannot be Zero!!")
    if exp:
        val = compute_from_exp(interarrival_mean)
    else:
        val = compute_from_emp_dist(interarrival_emp_dist)

    val = val * sf

    return round(val / 1000)

# returns velocity in mph
def compute_vehicle_velocity():
    value = compute_from_emp_dist(vel_emp_dist)
    while value < 1:
        value = compute_from_emp_dist(vel_emp_dist)

    mph = round(value * (3600 / 5280)) # convert ft/s to mph
    if mph < 10:
        mph += 15

    return mph


# ======= DISCRETE DISTRIBUTIONS =======

enter_dist = [0.4590, 0.7377, 0.7787, 0.8033, 1.0] # maps 0-4

exit_dist = [0.1592, 0.2038, 0.2166, 0.2420, 0.3439, 1.0] # maps 1-6

def generate_entrance_point():
    rand = random.uniform(0, 1)

    idx = 0
    while idx < len(enter_dist) and rand > enter_dist[idx]:
        idx += 1

    return idx

def generate_exit_point():
    rand = random.uniform(0, 1)

    idx = 0
    while idx < len(exit_dist) and rand > exit_dist[idx]:
        idx += 1

    return (idx + 1)

# ======= GENERATE VEHICLE ========

def spawn_vehicle(exp=False):
    ia = compute_interarrival(exp)
    vel = compute_vehicle_velocity()

    entrance = generate_entrance_point()
    exit = generate_exit_point()

    while exit <= entrance:
        exit = generate_exit_point()

    if random.uniform(0, 1) < 0.5:
        lane = True
    else:
        lane = False

    return (ia, vel, entrance, exit, lane)