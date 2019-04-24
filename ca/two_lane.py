from stoplight import Stoplight
from vehicle import Vehicle
from stats import Stats
from cell import Cell

from queue import Queue
import random

### Model Parameters

BACK_GAP = 2
LANE_CHANGE_PROB = .5
SCALE_FACTOR = .7
Q_SIZE = 5

class Two_Lane():

    '''
    Class describing behavior of a two lane road

    Attributes:
        length: integer length of the road
        sim_time: integer simulation time
        lanes: array of length 2 containing an array for each of the right lane (index 0) and left lane (index 1)
        queues: dictionary mapping location to a list of queues for cars, index 0 is right lane, index 1 is left lane
        stoplights: dictionary mapping location to stoplight objects
        stats: a Stats() class object recording statistics for the simulation
    '''

    def __init__(self, length, stoplights):
        self.sim_time = 0
        self.length = length
        self.lanes = []
        self.lanes.append(self._make_lane(length))
        self.lanes.append(self._make_lane(length))
        self.stoplights = stoplights
        self._add_stoplights(stoplights)
        self._make_input_queues(stoplights)
        self._set_exits(stoplights)
        self.stats = Stats()

    ### Setup Methods

    def _make_lane(self, length):
        lane = []
        for _ in range(self.length):
            lane.append(Cell())
        return lane

    def _add_stoplights(self, stoplights):
        #stoplights is a dictionary mapping locations to stoplights
        for loc in stoplights.keys():
            self._add_light(loc, stoplights[loc])
    
    def _add_light(self, loc, light):
        if self.lanes[0][loc].has_stoplight():
            raise ValueError('Failed to add stoplight; cell is already has stoplight.')
        for i in [0,1]:
            self.lanes[i][loc].set_stoplight(light)

    def _make_input_queues(self, stoplights):
        #make input queues at beginning and for each stoplight
        #list index indicates which stoplight
        self.queues = []
        self.queues.append([Queue(), Queue(), 0])
        for loc in self.stoplights.keys():
            self.queues.append([Queue(), Queue(), loc])

    def _set_exits(self, stoplights):
        self.exits = []
        for loc in self.stoplights.keys():
            self.exits.append(loc)
        self.exits.append(self.length-1)

    ### Car Generation Methods

    def _spawn_vehicles(self):
        if self.sim_time == 0:
            self.next_vehicle = self.stats.generate_vehicle(self.sim_time, sf=SCALE_FACTOR)
        while self.next_vehicle.get_enter_time() <= self.sim_time:

            ### Choose This for no queueing

            #self._place_vehicle_qless(self.next_vehicle)

            ### Choose this for queueing
            
            #if self.next_vehicle.get_source() == 0:
            #    self._place_vehicle_qless(self.next_vehicle)
            #else:
            self._enqueue_vehicle(self.next_vehicle)
            
            
            self.next_vehicle = self.stats.generate_vehicle(self.sim_time, sf=SCALE_FACTOR)

    def _enqueue_vehicle(self, vehicle):
        intersection_num = vehicle.get_source()
        lane = vehicle.get_source_lane()
        if self.queues[intersection_num][lane].qsize() <= Q_SIZE:
            self.queues[intersection_num][lane].put(vehicle)

    def _place_vehicles(self):
        #queues is a dict with key loc, value list, index 0 is right lane queue, index 1 is left lane queue
        for queue_list in self.queues:
            for i in [0,1]:
                self._place_vehicle(queue_list[2], i, queue_list[i])

    def _place_vehicle(self, loc, lane, car_queue):
        #takes a location, lane, and queue. If the spot is empty, dequeues one car and puts it there
        if not self.lanes[lane][loc].has_vehicle() and not self.lanes[lane][loc].has_green_stoplight():
            if not car_queue.empty():
                car = car_queue.get()
                self.lanes[lane][loc].set_vehicle(car)
    
    def _place_vehicle_qless(self, vehicle):
        lane = vehicle.get_source_lane()
        loc = vehicle.get_source()
        if not self.lanes[lane][loc].has_vehicle():
            self.lanes[lane][loc].set_vehicle(vehicle)

    ### Vehicle and Cell Gaps

    def _update_gaps(self):
        gap = 5 #allows cars at the end to leave freely
        for lane in self.lanes:
            for cell in reversed(lane):
                cell.set_gap(gap)
                if cell.has_obstruction():
                    gap = 0
                else:
                    gap += 1
    
    def _look_back(self, lane, loc):
        #calculates backward gap at a location
        if loc >= self.length:
            raise ValueError("Out of bounds error, cannot check gap outside range of lane length.")
        count = -1
        while loc >= 0:
            if self.lanes[lane][loc].has_vehicle():
                return count
            count += 1
            loc -= 1
        return count

    ### Lane Changing

    def _change_lanes(self):
        for loc in range(self.length):
            #lane 0
            for i in [0,1]:
                if self.lanes[i][loc].has_vehicle():
                    other_lane = (i+1)%2
                    other_lane_gap = self.lanes[other_lane][loc].get_gap()
                    other_lane_back_gap = self._look_back(other_lane, loc)
                    if other_lane_gap > self.lanes[i][loc].get_gap() and other_lane_back_gap >= BACK_GAP and random.random() < LANE_CHANGE_PROB:
                        self._switch_lanes(i, loc)

    def _switch_lanes(self, lane, loc):
        vehicle = self.lanes[lane][loc].remove_vehicle()
        self.lanes[(lane + 1) % 2][loc].set_vehicle(vehicle)

    ### Vehicle Movement
    
    def _update_vehicle_speeds(self):
        for lane in self.lanes:
            for cell in lane:
                if cell.has_vehicle():
                    cell.get_vehicle().update_speed()

    def _advance_vehicles(self):
        for lane in [0,1]:
            vehicle_list = {}
            for i in range(self.length):
                if self.lanes[lane][i].has_vehicle():
                    vehicle = self.lanes[lane][i].remove_vehicle()
                    loc = i + vehicle.get_speed()
                    vehicle_list.update({loc: vehicle})
            for loc, vehicle in vehicle_list.items():
                if loc >= self.exits[vehicle.get_dest() - 1] - 1:
                    self.stats.exit_simulation(self.sim_time, vehicle)
                elif loc < self.length:
                    self.lanes[lane][loc].set_vehicle(vehicle)
                else:
                    self.stats.exit_simulation(self.sim_time, vehicle)

    ### advance time

    def _timestep(self):
        '''
        Controlls one timestep of the simulation. ORDER MATTERS!!!
        '''
        self._spawn_vehicles()
        self._place_vehicles()
        self._update_gaps()
        self._change_lanes()
        self._update_gaps()
        self._update_vehicle_speeds()
        self._advance_vehicles()
        self._timestep_stoplights()
        self.sim_time += 1
        

    def _timestep_stoplights(self):
        for i in range(self.length):
            if self.lanes[0][i].has_stoplight():
                self.lanes[0][i].get_stoplight().timestep()

    ### Simulation Controller

    def simulate(self, steps, skips=1, vis=True):
        if vis:
            print(self)
            for i in range(steps):
                self._timestep()
                if i % skips == 0:
                    print("")
                    print(self)
        else:
            for i in range(steps):
                self._timestep()
        
        self.stats.calculate_stats()

    ### Miscellaneous

    def __str__(self):
        s = ''
        for i in [1,0]:
            for cell in self.lanes[i]:
                if cell.has_stoplight() and cell.has_vehicle():
                    s += '|X|'
                elif cell.has_stoplight():
                    s += '| |'
                elif cell.has_vehicle():
                    s += 'X'
                else:
                    s += '_'
            s += '\n'
        return s
