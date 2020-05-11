"""solar_pd controller."""

# This simulation is prepared in order to demonstrate a working closed loop controller.
# In this example, a proportional derivate controller will be used.
# The effects of noise and disturbance on a pd controller can be observed.
# The main purpose of the controller is to face Sun as "well" as possible when Sun is fixed in a position.

import sys, os
sys.path.append(os.path.abspath(os.path.join('..')))
from solar_helper import Solar_Simulation, TIME_STEP

# solar_keyboard_helper.py file has a Solar_Simulation class in order to make the code simpler.
from controller import Keyboard
import time
from control import tf, step_response
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
sun_position = 1
K_p = 1 # Let's fix K_p and see what happens with changing K_d.
for K_d in [0.1,0.5,1,10]:

    tf_controller = tf([K_d, K_p], [1])
    
    # Closed loop transfer function and output can be calculated.
    tf_closed_loop = (tf_plant*tf_controller)/(1+tf_plant*tf_controller)
    
    # Now by finding output transfer function's impulse reponse, we can see it's behaviour in time domain.
    duration = 10 # Output will be computed for this many seconds.
    t = np.linspace(0, duration, num = int(duration/(TIME_STEP*1e-3)))
    t, output = step_response(tf_closed_loop, t)

    # Let's plot the panel's angle.
    plt.plot(t, output)
    plt.plot(t, sun_position*np.ones(len(t)))
    plt.ylabel(f'Expected Panel Angle/Sun Angle for K_d = {K_d} (rad)')
    plt.xlabel('Time (s)')
    plt.show()


# Controller function is defined.
def get_controller_output(K_p, K_d, errors):
    return (K_p*errors[-1] + K_d*np.gradient(errors)[-1]/(TIME_STEP*1e-3))
    # Gradient function is used in order to compute the numerical derivative of the error.

sim = Solar_Simulation(noise = 0, disturbance = 0, moving_sun = False) # Simulation is started with some disturbance.

K_d = 1
errors = [math.pi/2]
while True:
    # At each time step, control output is given to the plant as input.
    error = sim.get_sun_angle() - sim.get_panel_angle() # Error is computed.
    errors.append(error) # Errors are kept in a list in order to compute the derivative.
    controller_output = get_controller_output(K_p, K_d, errors)
    sim.set_torque(controller_output)
    time.sleep(TIME_STEP*1e-3)

# Add some noise and disturbance to see the effects on the result.
# What is the effect of noise compared to the proportional controller case?