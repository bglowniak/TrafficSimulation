# des_engine.py maintains the priority queue (future event list) and keeps track of simulation time

from queue import PriorityQueue
from abc import ABC, abstractmethod

num_events = 5

# define an abstract base class for events
class Event(ABC):
    def __init__(self, timestamp):
        self.timestamp = timestamp
        self.result = None

    def get_timestamp(self):
        return self.timestamp

    @abstractmethod
    def execute(self):
        pass

    def get_result(self):
        if self.result == None:
            return "Event has not yet been executed."
        else:
            return self.result

    def __lt__(self, other):
        return self.timestamp < other.timestamp

future_event_list = PriorityQueue()
current_time = 0.0

def simulation_time():
    return current_time

def schedule_event(event):
    future_event_list.put(event)

def run_simulation():
    global current_time
    events_processed = 0
    while not future_event_list.empty(): #and events_processed < num_events:
        current = future_event_list.get()
        current_time = current.get_timestamp()
        current.execute()
        print(current.get_result())
        events_processed += 1
