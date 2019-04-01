# des_events.py implements the various event objects

# subclass with events determined by conceptual model
from des_engine import Event, schedule_event, simulation_time
from des_intersection import intersection_list

class IntersectionArrival(Event):
    def __init__(self, timestamp, intersection_id, vehicle):
        self.timestamp = timestamp
        self.intersection_id = intersection_id
        self.vehicle = vehicle

    def execute(self):
        if self.intersection_id is Intersections.TENTH:
            # instantiate new vehicle and schedule next arrival based on distributions
            new_time = simulation_time() + 5 # fancy random number oooo
            new_arrival = Vehicle("placeholder", new_time, Intersections.TENTH, Intersections.FOURTEENTH)
            schedule_event(new_time, IntersectionArrival(new_time, Intersections.TENTH, new_arrival))

        stoplight_state = intersection_list[self.intersection_id].get_state()

        if stoplight_state:
            # schedule departure event for vehicle
            schedule_event(simulation_time(), IntersectionDeparture(simulation_time(), self.intersection_id, self.vehicle))
        else:
            # queue at intersection
            intersection_list[self.intersection_id].queue_vehicle(self.vehicle)

    def description(self):
        return "Vehicle " + self.vehicle.get_id() + " has arrived at intersection " + self.intersection_id + " at timestamp " + self.timestamp + "."

class IntersectionDeparture(Event):
    def __init__(self, timestamp, intersection_id, vehicle):
        self.timestamp = timestamp
        self.intersection_id = intersection_id

    def execute(self):
        pass

    def description(self):
        pass

class StoplightChange(Event):
    def __init__(self, timestamp, intersection_id):
        self.timestamp = timestamp
        self.intersection_id = intersection_id

    def execute(self):
        current = intersection_list[self.intersection_id]
        if current.get_state():
            next_timestamp = simulation_time() + current.get_red_duration()
            schedule_event(next_timestamp, StoplightChange(next_timestamp, self.intersection_id))
        else:
            next_timestamp = simulation_time() + current.get_green_duration()
            schedule_event(next_timestamp, StoplightChange(next_timestamp, self.intersection_id))

            # dequeue all cars at current intersection and schedule intersection arrival at next intersection for each

        #intersection_list[self.intersection_id].toggle()
        current.toggle()

    def description(self):
        return "Intersection " + str(self.intersection_id) + " stoplight changed at timestamp " + str(self.timestamp) + "!"