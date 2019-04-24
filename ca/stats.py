from vehicle import Vehicle
import random
from simulation_input import spawn_vehicle
from welch_avg import analyze


class Stats():

    def __init__(self):
        self.sim_times = []
        self.vehicle_traversal_times = []
        self.vehicle_starts = []
        self.vehicle_ends = []

    def pick_lane(self):
        if random.random() < .5:
            return 0
        else:
            return 1

    def choose_max_speed(self):
        if random.random() < .15:
            return 2
        elif random.random() < .4:
            return 3
        else:
            return 4

    def generate_vehicle(self, sim_time, sf=1):
        inter_arrival, velocity, entrance, exit_point = spawn_vehicle(sf=sf)
        velocity = velocity//5
        if velocity > 4:
            velocity = 4
        return Vehicle(sim_time + inter_arrival, velocity, self.choose_max_speed(), entrance, exit_point, self.pick_lane())

    def exit_simulation(self, sim_time, vehicle):
        self.sim_times.append(sim_time)
        self.vehicle_traversal_times.append(
            sim_time - vehicle.get_enter_time())
        self.vehicle_starts.append(vehicle.get_source())
        self.vehicle_ends.append(vehicle.get_dest())

    def calculate_stats(self):
        analyze(self.sim_times, self.vehicle_traversal_times, self.vehicle_starts, self.vehicle_ends)
