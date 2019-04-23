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

# des_intersections.py contains all signal timings and distances between intersections

# many of these state variables are unused for the checkpoint/are subject to change

# defining variables here means needing "global" to access them within the events. Really not a fan of having to do this, but for interest of time for the checkpoint due date we'll go with it for now.
# may create a container object that keeps track of all these vars that is passed into events so that they don't have to access global vars - defined as SimulationState

MAX_DEPARTURES = 5 # how many vehicles exit the simulation before it stops scheduling events
DEBUG = False # whether or not to include print statements for all events

num_events = 0
vehicles_entered = 0
vehicles_departed = 0
vehicles_waiting = 0
total_waiting_time = 0
level_of_traffic = 0 # UNUSED, will be used once we create a distribution
last_event_time = 0.0

schedule_new_events = True

final_departure_time = 0.0
test_val = 0
max_val = 10
#################
# DEFINE EVENTS #
#################

class SimulationArrival(Event):
    def __init__(self, timestamp, vehicle):
        self.timestamp = timestamp
        self.vehicle = vehicle

    def execute(self):
        if self.vehicle.entrance == 0:
            intersection = Intersections.TENTH
        else:
            intersection = Intersections(self.vehicle.entrance)

        self.result = "Vehicle " + str(self.vehicle.get_id()) + " has entered the simulation."

        # schedule intersection this vehicle will first approach
        #schedule_event(IntersectionArrival(self.timestamp, intersection, self.vehicle))

        # schedule simulation arrival for new vehicle
        vehicle_data = spawn_vehicle()

        direction = (vehicle_data[2] == 0) # if arriving before 10th, NB. Otherwise, E/W

        new_vehicle = Vehicle(enter_time=self.timestamp + vehicle_data[0],
                velocity=vehicle_data[1],
                enter_location=vehicle_data[2],
                exit_location=vehicle_data[3],
                direction=direction,
                lane=vehicle_data[4])

        schedule_event(SimulationArrival(new_vehicle.enter_time, new_vehicle))

class SimulationExit(Event):
    def __init__(self, timestamp, vehicle):
        self.timestamp = timestamp
        self.vehicle = vehicle

    def execute(self):
        # compute statistics
        self.result = "Vehicle " + (self.vehicle.get_id()) + " has left the simulation. Statistics: (not yet implemented)."

class IntersectionArrival(Event):
    def __init__(self, timestamp, intersection_id, vehicle):
        self.timestamp = timestamp
        self.intersection_id = intersection_id
        self.intersection = intersection_list[self.intersection_id]
        self.vehicle = vehicle

    def execute(self):
        stoplight_state = self.intersection.get_state()

        self.result = "Vehicle " + str(self.vehicle.get_id()) + " has arrived at " + str(self.intersection_id) + "."

        veh_dir = self.vehicle.direction

        if (stoplight_state and veh_dir) or not (stoplight_state or veh_dir):
            # stoplight is GREEN and direction is NORTH --> travel through
            # stoplight is RED and direction is E/W --> travel through/enter the corridor
            self.intersection_clear()
        elif (not stoplight_state and veh_dir) or (stoplight_state and not veh_dir):
            # stoplight is RED and direction is NORTH --> Queue
            # stoplight is GREEN and direction is E/W --> Queue
            self.queue_vehicle()

    def queue_vehicle(self):
        # queue at intersection
        self.intersection.queue_vehicle(self.vehicle, self.vehicle.lane, self.vehicle.direction)
        self.result += " The light is RED and the vehicle is waiting."

    def intersection_clear(self):
        # schedule departure event for vehicle
        schedule_event(IntersectionDeparture(self.timestamp, self.intersection_id, self.vehicle))
        self.result += " The light is GREEN."

class IntersectionDeparture(Event):
    def __init__(self, timestamp, intersection_id, vehicle):
        self.timestamp = timestamp
        self.intersection_id = intersection_id
        self.intersection = intersection_list[self.intersection_id]
        self.vehicle = vehicle

    def execute(self):
        if self.intersection_id is self.vehicle.exit:
            self.vehicle.set_exit_time(self.timestamp)
            self.result = "Vehicle " + str(self.vehicle.get_id()) + " has departed " + str(self.intersection_id) + " (Exit Point)."
        else:
            self.result = "Vehicle " + str(self.vehicle.get_id()) + " has departed " + str(self.intersection_id) + "."

            self.vehicle.turn_north()

            next_intersection = self.intersection.next_intersection()
            distance = self.intersection.get_distance_to_next()
            arrival_time = self.timestamp + self.vehicle.calc_travel_time(distance)
            schedule_event(IntersectionArrival(arrival_time, next_intersection, self.vehicle))

class StoplightChange(Event):
    def __init__(self, timestamp, intersection_id):
        self.timestamp = timestamp
        self.intersection_id = intersection_id
        self.intersection = intersection_list[self.intersection_id]
        self.current_state = self.intersection.get_state()

    def execute(self):
        global DEBUG
        self.result = ""

        if self.current_state:
            next_timestamp = simulation_time() + current.get_red_duration()
            schedule_event(StoplightChange(next_timestamp, self.intersection_id))

            if DEBUG:
                self.result = "Stoplight at " + str(self.intersection_id) + " has changed to RED."
        else:
            next_timestamp = simulation_time() + current.get_green_duration()
            schedule_event(StoplightChange(next_timestamp, self.intersection_id))


            num_cars = current.num_queueing()

            # dequeue all cars at current intersection and schedule intersection departure for each
            # assume that all cars leave a stoplight instantaneously for now (no delays while cars start to accelerate)
            while current.num_queueing() > 0:
                # can add delay to next intersection based on order in queue
                vehicle = current.dequeue_vehicle()
                schedule_event(IntersectionDeparture(self.timestamp, self.intersection_id, vehicle))
                vehicles_waiting -= 1

            if DEBUG:
                self.result = "Stoplight at " + str(self.intersection_id) + " has changed to GREEN. There were " + str(num_cars) + " waiting."

        current.toggle()

####################
# BEGIN SIMULATION #
####################

vehicle_data = spawn_vehicle()
new_vehicle = Vehicle(enter_time=0.0,
                      velocity=vehicle_data[1],
                      enter_location=vehicle_data[2],
                      exit_location=vehicle_data[3],
                      direction=(vehicle_data[2] == 0),
                      lane=vehicle_data[4])

schedule_event(SimulationArrival(0.0, new_vehicle))

run_simulation()
'''
#schedule stoplight changes (13th has no stoplight). All stoplights start as RED.
schedule_event(StoplightChange(simulation_time(), Intersections.TENTH))
schedule_event(StoplightChange(simulation_time(), Intersections.ELEVENTH))
schedule_event(StoplightChange(simulation_time(), Intersections.TWELFTH))
schedule_event(StoplightChange(simulation_time(), Intersections.FOURTEENTH))

# first vehicle starts at 10th St and will depart at 14th St at time 0.0
first_vehicle = Vehicle(enter_time=simulation_time())
schedule_event(IntersectionArrival(simulation_time(), Intersections.TENTH, first_vehicle))

start_time = time.time()
run_simulation()
end_time = time.time()

print("Statistics: ")
print("Total Runtime: " + str(end_time - start_time) + " seconds")
print("Total Time for " + str(MAX_DEPARTURES) + " vehicles to exit the system: " + str(final_departure_time) + " seconds")
print("Total Duration (Simulation Time): " + str(simulation_time()) + " seconds")
print("Number of Events: " + str(num_events))
print("Vehicles Entered: " + str(vehicles_entered))
print("Vehicles Departed: " + str(vehicles_departed))'''
