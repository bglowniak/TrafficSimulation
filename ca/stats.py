from vehicle import Vehicle
import random

class Stats():

    def __init__(self):
        self.seed = 0
        self.vehicle_exit_times = []

    def get_interarrival(self):
        return 37

    def get_source(self):
        '''r = random.random()
        if r < .5:
            return 0
        elif r < .7:
            return 1
        elif r < .8:
            return 2
        elif r < .9:
            return 3
        else:
            return 4'''
        return 0

    def generate_vehicle(self, sim_time):
        time = sim_time + self.get_interarrival()
        speed = 1
        source = self.get_source()
        dest = 6
        source_lane = 0
        return Vehicle(time, speed, source, dest, source_lane)

    def exit_simulation(self, sim_time, vehicle):
        if sim_time < 500:
            return
        self.vehicle_exit_times.append(sim_time - vehicle.get_enter_time())

    def calculate_stats(self):
        return sum(self.vehicle_exit_times)/ len(self.vehicle_exit_times)
