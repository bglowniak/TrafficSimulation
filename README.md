# Peachtree St NE Traffic Simulation

This project was built by Brian Glowniak and Joel Katz for CX 4230/CSE 6730 Computer Simulation at GT.

The goal was to follow the steps of the modeling and simulation life cycle to develop and analyze multiple simulations of traffic traversing a section of Peachtree St NE in Atlanta (from 10th St to 14th St). We devised a conceptual model, performed input analysis, programmed our simulation models, completed verification and validation on the models, and finally did output analysis on the results. The full project is summarized in ProjectReport.pdf.

We built two models, each following a different paradigm - one using Cellular Automata, and the other using Discrete Event Simulation.

## Cellular Automata (developed by Joel Katz)
1) navigate to the ca folder in command prompt
2) If you are running from command line (see below for PACE instructions):
     python driver.py
3) Adjust parameters in driver.py like stoplight locations and timers, or length of road and initial # of cars

## Discrete Event Simulation (developed by Brian Glowniak)
1) navigate to des folder
     * *des_engine.py* contains the simulation engine. This is independent of the traffic simulation.
     * *des_simulation.py* contains the simulation executive. This defines (most) state variables and events.
     * *des_intersection.py* contains all code related to intersections
     * *des_vehicle.py* contains the vehicle class

2) If you are running from the command line, execute: *python des_simulation.py* to run the simulation (see below for PACE instructions). State variables can be modified within this file in the instantiation of SimulationState.

## Input Analysis
The InputAnalysis folder contains the Jupyter notebook used to generate empirical distributions of variables such as vehicle velocity, vehicle interarrival time, and vehicle entrance and exit points. We used the NGSIM data set, a public archive, to perform this analysis (more info on this set is outlined in the resource docs within that folder).

## Common Files (these are present in both directories so each sim can use them)
1) *simulation_input.py* defines the distributions and vehicle generation functions
2) *welch_avg.py* defines a function that can be used to compute Welch's moving average on a simulation run

## Running on PACE
1) Using an FTP service (we used WinSCP on Windows), connect to PACE using username@coc-ice.pace.gatech.edu and your GT password. Move the repository onto PACE.
2) Use PUTTY and the same login credentials to ssh into the PACE cluster. Run *ls* to confirm that the repository is present.
3) Schedule a job on a compute node using *qsub -I -q coc-ice -l nodes=1 -l walltime=00:05:00*. Wait for the node to load.
4) Once the node has loaded, run *module load anaconda3* to gather the required Python 3 libraries.
5) To run the DES sim, run *cd des* and then *python des_simulation.py*. Parameters must be modified in this file.
6) To run the CA sim, rund *cd ca* and then *python driver.py*. Parameters must be modified in this file.
