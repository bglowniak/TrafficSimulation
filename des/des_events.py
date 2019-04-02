# des_events.py implements the various event objects

# subclass with events determined by conceptual model
import random
from des_engine import Event, schedule_event, simulation_time
from des_intersection import intersection_list, Intersections

class IntersectionArrival(Event):
    def __init__(self, timestamp, intersection_id, vehicle):
        self.timestamp = timestamp
        self.intersection_id = intersection_id
        self.vehicle = vehicle

    def execute(self):
        '''if self.intersection_id is Intersections.TENTH:
            # instantiate new vehicle and schedule next arrival based on distributions
            new_time = simulation_time() + 5 # fancy random number oooo
            new_arrival = Vehicle(new_time, Intersections.TENTH, Intersections.FOURTEENTH)
            schedule_event(new_time, IntersectionArrival(new_time, Intersections.TENTH, new_arrival))'''

        stoplight_state = intersection_list[self.intersection_id].get_state()

        self.result = "Vehicle " + str(self.vehicle.get_id()) + " has arrived at " + str(self.intersection_id) + " at time " + str(self.timestamp) + "."

        if stoplight_state:
            # schedule departure event for vehicle
            schedule_event(IntersectionDeparture(self.timestamp, self.intersection_id, self.vehicle))
            self.result += " The light is GREEN."
        else:
            # queue at intersection
            intersection_list[self.intersection_id].queue_vehicle(self.vehicle)
            self.result += " The light is RED and the vehicle is waiting."

class IntersectionDeparture(Event):
    def __init__(self, timestamp, intersection_id, vehicle):
        self.timestamp = timestamp
        self.intersection_id = intersection_id
        self.vehicle = vehicle

    def execute(self):
        if self.intersection_id is Intersections.FOURTEENTH:
            self.vehicle.set_exit_time(self.timestamp)
            self.result = "Vehicle " + str(self.vehicle.get_id()) + " has left the simulation at timestamp " + str(self.timestamp) + ". Duration: " + str(self.vehicle.calc_travel_time())
            end_sim()
        else:
            next_time = self.timestamp + 10 # 10 seconds between each intersection, will change this in the future
            next_intersection = intersection_list[self.intersection_id].next_intersection()
            schedule_event(IntersectionArrival(next_time, next_intersection, self.vehicle))
            self.result = "Vehicle " + str(self.vehicle.get_id()) + " has departed intersection " + str(self.intersection_id) + " at time " + str(self.timestamp) + "."

class StoplightChange(Event):
    def __init__(self, timestamp, intersection_id):
        self.timestamp = timestamp
        self.intersection_id = intersection_id

    def execute(self):
        current = intersection_list[self.intersection_id]
        if current.get_state():
            next_timestamp = simulation_time() + current.get_red_duration()
            schedule_event(StoplightChange(next_timestamp, self.intersection_id))
            self.result = "Stoplight at " + str(self.intersection_id) + " has changed to RED at time " + str(self.timestamp) + "."
        else:
            next_timestamp = simulation_time() + current.get_green_duration()
            schedule_event(StoplightChange(next_timestamp, self.intersection_id))
            num_cars = current.num_queueing()
            # dequeue all cars at current intersection and schedule intersection departure for each
            # assume that all cars leave a stoplight instantaneously for now (no delays while cars start to accelerate)
            while current.num_queueing() > 0:
                vehicle = current.dequeue_vehicle()
                schedule_event(IntersectionDeparture(self.timestamp, self.intersection_id, vehicle))

            self.result = "Stoplight at " + str(self.intersection_id) + " has changed to GREEN at time " + str(self.timestamp) + ". There were " + str(num_cars) + " waiting."

        #intersection_list[self.intersection_id].toggle()
        current.toggle()