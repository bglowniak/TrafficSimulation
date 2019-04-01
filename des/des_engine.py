# des_engine.py maintains the priority queue (future event list) and keeps track of simulation time

from queue import PriorityQueue
from abc import ABC, abstractmethod

# define an abstract base class for events
class Event(ABC):
    def __init__(self, timestamp):
        self.timestamp = timestamp

    def get_timestamp(self):
        return timestamp

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def description(self):
        pass

future_event_list = PriorityQueue()
current_time = 0.0

def current_time():
    return current_time

def schedule_event(timestamp, event):
    future_event_list.put(timestamp, event)

def run_simulation():
    while not future_event_list.empty():
        current = future_event_list.get()
        current_time = current.get_timestamp()
        print(current.description())
        current.execute()
