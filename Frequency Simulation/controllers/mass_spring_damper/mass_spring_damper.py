"""mass_spring_damper controller."""

# This simulation is designed to demonstrate a physical example of Bode plots.
# The Bode plot of a mass spring damper system will be shown.
# The plot will be verified with different excitations to the system.
import sys, os
sys.path.append(os.path.abspath(os.path.join('..')))
from mass_spring_damper_helper import MSD, get_phase_magnitude

from controller import Robot, Motor
import time
import math
import matplotlib.pyplot as plt
import numpy as np
from control import tf, bode_plot

sim_duration = 100
sim = MSD(excitation_frequency = 8, exciatation_amplitude = 1, duration = sim_duration)
# Create the simulation with excitation parameters and duration

TIME_STEP = sim.TIME_STEP # Time step of the simulation will be necessary for frequency analysis

while not sim.done: # Wait until the simulation is done
    time.sleep(1e-2)

position_history = sim.get_position_history() # Get the position readings for the given duration with the given timestep

phase, magnitude = get_phase_magnitude(position_history, sim_duration, TIME_STEP)
print(f"Phase: {phase*180/np.pi} degrees, magnitude: {magnitude}")

# Now, let's see if the results are expected by modeling the system
m = 1
k = 10
b = 0.1

system_tf = tf([1], [m, b, k])


b_magnitude, b_phase, b_freq = bode_plot([system_tf], np.linspace(0.1, 100, int(1e4), endpoint = True) , Plot = True)
plt.plot(np.linspace(0, sim_duration, len(position_history)), position_history)
plt.show()
