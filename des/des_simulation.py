# des_simulation.py initializes the simulation, maintains state variables, defines the events of the simulation, and sets up the initial scheduling of events

import time
import random
from des_engine import *
from des_intersection import *
from des_vehicle import *

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

#################
# DEFINE EVENTS #
#################

class IntersectionArrival(Event):
    def __init__(self, timestamp, intersection_id, vehicle):
        self.timestamp = timestamp
        self.intersection_id = intersection_id
        self.vehicle = vehicle

    def execute(self):
        # see note on line 17 about global vars
        global num_events
        global vehicles_waiting
        global vehicles_entered

        num_events += 1

        if self.intersection_id is Intersections.TENTH and schedule_new_events:
            vehicles_entered += 1

            # instantiate new vehicle and schedule next arrival based on distributions
            arrival_time = simulation_time() + random.randint(10, 60) # fancy random number oooo between 10 and 60 seconds
            new_arrival = Vehicle(enter_time=arrival_time) # will travel full length of corridor by default (10th -> 14th)
            schedule_event(IntersectionArrival(arrival_time, Intersections.TENTH, new_arrival))

        stoplight_state = intersection_list[self.intersection_id].get_state()

        self.result = "Vehicle " + str(self.vehicle.get_id()) + " has arrived at " + str(self.intersection_id) + " at time " + str(self.timestamp) + "."

        if stoplight_state:
            # schedule departure event for vehicle
            if schedule_new_events:
                schedule_event(IntersectionDeparture(self.timestamp, self.intersection_id, self.vehicle))
            self.result += " The light is GREEN."
        else:
            # queue at intersection
            intersection_list[self.intersection_id].queue_vehicle(self.vehicle)
            self.result += " The light is RED and the vehicle is waiting."
            vehicles_waiting += 1

class IntersectionDeparture(Event):
    def __init__(self, timestamp, intersection_id, vehicle):
        self.timestamp = timestamp
        self.intersection_id = intersection_id
        self.vehicle = vehicle

    def execute(self):
        # temporary - see note on line 17 about global vars
        global num_events
        global vehicles_departed
        global MAX_DEPARTURES
        global schedule_new_events
        global final_departure_time

        num_events += 1

        if self.intersection_id is Intersections.FOURTEENTH:
            self.vehicle.set_exit_time(self.timestamp)
            self.result = "Vehicle " + str(self.vehicle.get_id()) + " has left the simulation at timestamp " + str(self.timestamp) + ". Duration: " + str(self.vehicle.calc_total_time())

            vehicles_departed += 1
            if vehicles_departed == MAX_DEPARTURES:
                final_departure_time = self.timestamp
                schedule_new_events = False
        else:
            self.result = "Vehicle " + str(self.vehicle.get_id()) + " has departed intersection " + str(self.intersection_id) + " at time " + str(self.timestamp) + "."

            if schedule_new_events:
                next_intersection = intersection_list[self.intersection_id].next_intersection()
                distance = intersection_list[self.intersection_id].get_distance_to_next()
                arrival_time = self.timestamp + self.vehicle.calc_travel_time(distance)
                schedule_event(IntersectionArrival(arrival_time, next_intersection, self.vehicle))

class StoplightChange(Event):
    def __init__(self, timestamp, intersection_id):
        self.timestamp = timestamp
        self.intersection_id = intersection_id

    def execute(self):
        # temporary - see note on line 17 about global vars
        global num_events
        global vehicles_waiting

        num_events += 1

        current = intersection_list[self.intersection_id]
        if current.get_state():
            if schedule_new_events:
                next_timestamp = simulation_time() + current.get_red_duration()
                schedule_event(StoplightChange(next_timestamp, self.intersection_id))

            if DEBUG:
                self.result = "Stoplight at " + str(self.intersection_id) + " has changed to RED at time " + str(self.timestamp) + "."
            else:
                self.result = ""
        else:
            num_cars = current.num_queueing()
            if schedule_new_events:
                next_timestamp = simulation_time() + current.get_green_duration()
                schedule_event(StoplightChange(next_timestamp, self.intersection_id))

                # dequeue all cars at current intersection and schedule intersection departure for each
                # assume that all cars leave a stoplight instantaneously for now (no delays while cars start to accelerate)
                while current.num_queueing() > 0:
                    # can add delay to next intersection based on order in queue
                    vehicle = current.dequeue_vehicle()
                    schedule_event(IntersectionDeparture(self.timestamp, self.intersection_id, vehicle))
                    vehicles_waiting -= 1

            if DEBUG:
                self.result = "Stoplight at " + str(self.intersection_id) + " has changed to GREEN at time " + str(self.timestamp) + ". There were " + str(num_cars) + " waiting."
            else:
                self.result = ""

        current.toggle()

####################
# BEGIN SIMULATION #
####################

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
print("Vehicles Departed: " + str(vehicles_departed))
