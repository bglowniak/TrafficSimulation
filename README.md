# CX 4230 Project 2

## Cellular Automata (developed by Joel Katz)
1) navigate to ca folder in command prompt
2) Execute:
     python driver.py
3) Adjust parameters in driver.py like stoplight locations and timers, or length of road and initial # of cars

## Discrete Event Simulation (developed by Brian Glowniak)
1) navigate to des folder
     * *des_engine.py* contains the simulation engine. This is independent of the traffic simulation.
     * *des_simulation.py* contains the simulation executive. This defines (most) state variables and events.
     * *des_intersection.py* contains all code related to intersections
     * *des_vehicle.py* contains the vehicle class

2) Execute: *python des_simulation.py* to run the simulation. State variables can be modified within this file. The simulation currently runs until five vehicles have departed beyond the 14th Street intersection.
