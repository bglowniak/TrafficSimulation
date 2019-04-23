# des_simulation.py initializes the simulation, maintains state variables, defines the events of the simulation, and sets up the initial scheduling of events
import time
import random
from des_engine import *
from des_intersection import *
from des_vehicle import *
from simulation_input import spawn_vehicle

####################
# DEFINE VARIABLES #
####################

# SimulationState keeps track of the various state variables and the progress of the simulation
class SimulationState():
    def __init__(self, debug_flag=False, max_departures=10):

        self.DEBUG = debug_flag # how many vehicles exit the simulation before it stops scheduling event
        self.MAX_DEPARTURES = max_departures # whether or not to include print statements for all events
        self.num_events = 0
        self.vehicles_entered = 0
        self.vehicles_departed = 0
        self.travel_times = []
        self.final_departure_time = 0.0
        self.schedule_new_events = True

        # CURRENTLY UNUSED
        self.vehicles_waiting = 0
        self.total_waiting_time = 0

    def sim_still_running(self):
        return self.schedule_new_events

    def stop_sim(self):
        self.schedule_new_events = False

    def add_travel_time(self, time):
        self.travel_times.append(time)

    def increment_events(self):
        self.num_events += 1

    def increment_entered(self):
        self.vehicles_entered += 1

    def increment_departed(self, timestamp):
        self.vehicles_departed += 1
        if self.vehicles_departed == self.MAX_DEPARTURES:
            self.stop_sim()
            self.final_departure_time = timestamp

    def debug_flag(self):
        return self.DEBUG

    def compute_stats(self, wallclock_start, wallclock_end):
        print("Statistics: ")
        print("Total Runtime: " + str(wallclock_end - wallclock_start) + " seconds")
        print("Total Time for " + str(self.MAX_DEPARTURES) + " vehicles to exit the system: " + str(self.final_departure_time) + " seconds")
        print("Total Duration (Simulation Time): " + str(simulation_time()) + " seconds")
        print("Number of Events: " + str(self.num_events))
        print("Vehicles Entered: " + str(self.vehicles_entered))
        print("Vehicles Departed: " + str(self.vehicles_departed))

        print("Travel Times: " + str(self.travel_times))

state = SimulationState()

#################
# DEFINE EVENTS #
#################

class SimulationArrival(Event):
    def __init__(self, timestamp, vehicle):
        self.timestamp = timestamp
        self.vehicle = vehicle

    def execute(self):
        global state
        self.result = ""

        if not state.sim_still_running():
            return

        if self.vehicle.entrance == 0:
            intersection = Intersections.TENTH
        else:
            intersection = Intersections(self.vehicle.entrance)

        if state.debug_flag():
            self.result = str(self.vehicle) + " has entered the simulation."

        vehicle_data = spawn_vehicle()
        new_vehicle = Vehicle(enter_time=self.timestamp + vehicle_data[0],
                velocity=vehicle_data[1],
                enter_location=vehicle_data[2],
                exit_location=vehicle_data[3],
                direction=(vehicle_data[2] == 0),
                lane=vehicle_data[4])

        schedule_event(IntersectionArrival(self.timestamp, intersection, self.vehicle))
        schedule_event(SimulationArrival(new_vehicle.enter_time, new_vehicle))
        state.increment_entered()
        state.increment_events()

class SimulationExit(Event):
    def __init__(self, timestamp, vehicle):
        self.timestamp = timestamp
        self.vehicle = vehicle

    def execute(self):
        global state
        self.result = ""

        if not state.sim_still_running():
            return

        if state.debug_flag():
            self.result = "Vehicle " + str(self.vehicle.get_id()) + " has left the simulation."

        self.vehicle.set_exit_time(self.timestamp)

        state.add_travel_time(self.vehicle.calc_total_time())
        state.increment_events()
        state.increment_departed(self.timestamp)

class IntersectionArrival(Event):
    def __init__(self, timestamp, intersection_id, vehicle):
        self.timestamp = timestamp
        self.intersection_id = intersection_id
        self.intersection = intersection_list[self.intersection_id]
        self.vehicle = vehicle

    def execute(self):
        global state
        self.result = ""

        if not state.sim_still_running():
            return

        if state.debug_flag():
            self.result = "Vehicle " + str(self.vehicle.get_id()) + " has arrived at " + str(self.intersection_id) + "."

        stoplight_state = self.intersection.get_state()
        veh_dir = self.vehicle.direction

        if (stoplight_state and veh_dir) or not (stoplight_state or veh_dir) or self.intersection_id is Intersections.THIRTEENTH:
            # stoplight is GREEN and direction is NORTH --> travel through
            # stoplight is RED and direction is E/W --> travel through/enter the corridor
            self.intersection_clear()
        elif (not stoplight_state and veh_dir) or (stoplight_state and not veh_dir):
            # stoplight is RED and direction is NORTH --> Queue
            # stoplight is GREEN and direction is E/W --> Queue
            self.queue_vehicle()

        state.increment_events()

    def queue_vehicle(self):
        # queue at intersection
        self.intersection.queue_vehicle(self.vehicle, self.vehicle.lane, self.vehicle.direction)
        if state.debug_flag():
            self.result += " The vehicle is waiting."

    def intersection_clear(self):
        # schedule departure event for vehicle
        schedule_event(IntersectionDeparture(self.timestamp, self.intersection_id, self.vehicle))
        if state.debug_flag():
            self.result += " The vehicle will pass through."

class IntersectionDeparture(Event):
    def __init__(self, timestamp, intersection_id, vehicle):
        self.timestamp = timestamp
        self.intersection_id = intersection_id
        self.intersection = intersection_list[self.intersection_id]
        self.vehicle = vehicle

    def execute(self):
        global state
        self.result = ""

        if not state.sim_still_running():
            return

        if self.intersection_id.value == self.vehicle.exit or self.intersection_id is Intersections.FOURTEENTH:
            if state.debug_flag():
                self.result = "Vehicle " + str(self.vehicle.get_id()) + " has departed " + str(self.intersection_id) + " (Exit Point)."
            schedule_event(SimulationExit(self.timestamp, self.vehicle))
        else:
            if state.debug_flag():
                self.result = "Vehicle " + str(self.vehicle.get_id()) + " has departed " + str(self.intersection_id) + "."

            self.vehicle.turn_north()
            next_intersection = self.intersection.next_intersection()
            distance = self.intersection.get_distance_to_next()
            arrival_time = self.timestamp + self.vehicle.calc_travel_time(distance)
            schedule_event(IntersectionArrival(arrival_time, next_intersection, self.vehicle))

        state.increment_events()

class StoplightChange(Event):
    def __init__(self, timestamp, intersection_id):
        self.timestamp = timestamp
        self.intersection_id = intersection_id
        self.intersection = intersection_list[self.intersection_id]

    def execute(self):
        global state
        self.result = ""

        if not state.sim_still_running():
            return

        if self.intersection.get_state():
            next = "RED"
            next_timestamp = simulation_time() + self.intersection.get_red_duration()
            direction = Directions.EW.value # allow any EW cars queuing to travel into the corridor
        else:
            next = "GREEN"
            next_timestamp = simulation_time() + self.intersection.get_green_duration()
            direction = Directions.NORTH.value # allow any north cars queuing to travel through or off the corridor

        schedule_event(StoplightChange(next_timestamp, self.intersection_id))

        left_cars = self.intersection.num_queueing(Lanes.LEFT.value, direction)
        right_cars = self.intersection.num_queueing(Lanes.RIGHT.value, direction)
        total_cars_queueing = left_cars + right_cars

        # dequeue all cars at current intersection and schedule intersection departure for each
        # assume that all cars leave a stoplight instantaneously for now (no delays while cars start to accelerate)
        while left_cars > 0 or right_cars > 0:
            # can add delay to next intersection based on order in queue
            if left_cars > 0:
                left_vehicle = self.intersection.dequeue_vehicle(Lanes.LEFT.value, direction)
                if left_vehicle is not None:
                    schedule_event(IntersectionDeparture(self.timestamp, self.intersection_id, left_vehicle))
                    left_cars -= 1


            if right_cars > 0:
                right_vehicle = self.intersection.dequeue_vehicle(Lanes.RIGHT.value, direction)
                if right_vehicle is not None:
                    schedule_event(IntersectionDeparture(self.timestamp, self.intersection_id, right_vehicle))
                    right_cars -= 1

        self.intersection.toggle()
        state.increment_events()

        if state.debug_flag():
            self.result = "Stoplight at " + str(self.intersection_id) + " has changed to " + next + ". There were " + str(total_cars_queueing) + " waiting."

####################
# BEGIN SIMULATION #
####################

vehicle_data = spawn_vehicle()
#first_vehicle = Vehicle()

first_vehicle = Vehicle(enter_time=vehicle_data[0],
                velocity=vehicle_data[1],
                enter_location=vehicle_data[2],
                exit_location=vehicle_data[3],
                direction=(vehicle_data[2] == 0),
                lane=vehicle_data[4])

schedule_event(SimulationArrival(first_vehicle.enter_time, first_vehicle))

# schedule stoplight changes (13th has no stoplight). All stoplights start as RED.
schedule_event(StoplightChange(simulation_time(), Intersections.TENTH))
schedule_event(StoplightChange(simulation_time(), Intersections.ELEVENTH))
schedule_event(StoplightChange(simulation_time(), Intersections.TWELFTH))
schedule_event(StoplightChange(simulation_time(), Intersections.FOURTEENTH))

start_time = time.time()
run_simulation()
end_time = time.time()

state.compute_stats(start_time, end_time)
