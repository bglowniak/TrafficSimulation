from vehicle import Vehicle
import random
from simulation_input import spawn_vehicle

class Stats():

    def __init__(self):
        self.seed = 0
        self.vehicle_exit_times = []
        self.vehicle_starts = []
        self.vehicle_ends = []

    def pick_lane(self):
        if random.random() < .5:
            return 0
        else:
            return 1

    def generate_vehicle(self, sim_time, sf=1):
        inter_arrival, velocity, entrance, exit_point = spawn_vehicle(sf=sf)
        velocity = velocity//5
        if velocity > 5:
            velocity = 5
        return Vehicle(sim_time + inter_arrival, velocity, entrance, exit_point, self.pick_lane())

    def exit_simulation(self, sim_time, vehicle):
        if sim_time < 100:
            return
        self.vehicle_exit_times.append(sim_time - vehicle.get_enter_time())
        self.vehicle_starts.append(vehicle.get_source())
        self.vehicle_ends.append(vehicle.get_dest())

    def calculate_stats(self):
        avg = sum(self.vehicle_exit_times)/ len(self.vehicle_exit_times)
        print('average: {:.2f}'.format(avg))
        return
