# des_events.py implements the various event objects

# subclass with events determined by conceptual model
from des_engine import Event

class IntersectionArrival(Event):
    def __init__(self, timestamp, intersection_id):
        self.timestamp = timestamp
        self.intersection_id = intersection_id

    def execute(self):
        pass

    def description(self):
        pass

class IntersectionDeparture(Event):
    def __init__(self, timestamp, intersection_id):
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
        # schedule next timestamp change based on
        pass

    def description(self):
        pass