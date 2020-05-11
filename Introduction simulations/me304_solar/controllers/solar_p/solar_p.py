"""solar_proportional controller."""

# This simulation is prepared in order to demonstrate a working closed loop controller.
# As a start, this controller will include a proportional controller.
# The effects of noise and disturbance on a pd controller can be observed.
# The main purpose of the controller is to face Sun as "well" as possible when Sun is fixed in a position.

import sys, os
sys.path.append(os.path.abspath(os.path.join('..')))
from solar_helper import Solar_Simulation, TIME_STEP

# solar_keyboard_helper.py file has a Solar_Simulation class in order to make the code simpler.
from controller import Keyboard
import time
from control import tf, impulse_response
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import math

# We can start with the same mathematical model.

m = 0.25
r = 2
b = 0.2
J = m*r**2

num = [1]
den = [J, b, 0]
tf_plant = tf(num, den)

# The controller output is supposed to be proportional to the error, which is equal to target angle - current angle
# Then a proportionality constant is required.
# Plot the expected output for different K values.
sun_position = math.pi/2
for K in [0.001,0.1,10]:
    tf_controller = tf([K], [1])
    
    # Assume reference input is Sun's angle which is a step function.
    tf_reference = tf([sun_position], [1, 0])
    # Closed loop transfer function and output can be calculated.
    tf_closed_loop = (tf_plant*tf_controller)/(1+tf_plant*tf_controller)
    tf_output = tf_reference*tf_closed_loop
    
    # Now by finding output transfer function's impulse reponse, we can see it's behaviour in time domain.
    duration = 500 # Output will be computed for this many seconds.
    t = np.linspace(0, duration, num = int(duration/(TIME_STEP*1e-3)))
    t, output = impulse_response(tf_output, t)

    # Let's plot the panel's expected angle vs time.
    plt.plot(t, output)
    plt.plot(t, sun_position*np.ones(len(t)))
    plt.ylabel(f'Expected Panel Angle for K = {K} (rad)')
    plt.xlabel('Time (s)')
    plt.show()

# Plots suggest that it takes a long time to come to a steady state if overshoot is prevented with very low K values.
# Even though increasing K slightly decreases the settling time, it introduces other problems.
# Firstly, increasing K increases overshoot. Even though there are limitations to the hinge angle,
# higher overshoot means the panel will hit the ground faster in the simulation, causing it to bounce back and oscillate.
# Secondly, increasing K increases the frequency of osciallations, which causes higher forces on the body and more energy usage.
# Then, could the controller be improved to solve these problems?

# Controller function is defined.
def get_controller_output(K, error):
    return K*error

sim = Solar_Simulation(noise = 0, disturbance = 0, moving_sun = False) # Simulation is started with some disturbance.

K = 0.1
while True:
    # At each time step, control output is given to the plant as input.
    error = sim.get_sun_angle() - sim.get_panel_angle()
    controller_output = get_controller_output(K, error)
    sim.set_torque(controller_output)

    time.sleep(TIME_STEP*1e-3)

# Add some noise and disturbance to see the effects on the result.