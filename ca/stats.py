from vehicle import Vehicle
import random

class Stats():

    def __init__(self):
        self.seed = 0
        self.vehicle_exit_times = []

    def get_interarrival(self):
        return 5

    def get_source(self):
        if random.random() < .8:
            return 0
        else:
            return 1

    def generate_vehicle(self, sim_time):
        time = sim_time + self.get_interarrival()
        speed = 1
        source = self.get_source()
        dest = 6
        source_lane = 0
        return Vehicle(time, speed, source, dest, source_lane)

    def exit_simulation(self, sim_time, vehicle):
        self.vehicle_exit_times.append(sim_time)