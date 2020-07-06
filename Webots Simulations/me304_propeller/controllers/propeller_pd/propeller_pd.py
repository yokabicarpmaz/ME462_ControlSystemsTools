"""propeller_p controller."""

# This simulation is prepared in order to demonstrate a working closed loop controller.
# This example will include a pd controller.
# The purpose of the controller is to keep the blue objet horizontal as in the initial position.

import sys, os
sys.path.append(os.path.abspath(os.path.join('..')))

from propeller_helper import Propeller_Simulation, TIME_STEP
import time
from control import tf, impulse_response
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import math

# We can start with the same mathematical model from the open loop example.
# This time, let's set the initial angle to 0 so initial condition calculations will not be necessary.

m = 0.1
L = 0.3
g = 9.81
b = 0.1
J = L*m**2/2

# J*a = T_p + m*g*sin(x)*L/2 + b*v
# Around the desired working point sin(x) is approximately x.

num = [1]
den = [J, b, m*g*L/2]
tf_plant = tf(num, den)

# For simplicity, proportionality constant will be constant for this example,
# and the effect of varying integral constant will be shown.
# Plot the expected output for different K_i values.

target_position = math.pi/2
K_p = 3
for K_d in [0.01, 0.5, 5, 50]:
    tf_controller = tf([K_d, K_p], [1])
    
    # Assume reference input is Sun's angle which is a step function.
    tf_reference = tf([target_position], [1, 0])
    # Closed loop transfer function and output can be calculated.
    tf_closed_loop = (tf_plant*tf_controller)/(1+tf_plant*tf_controller)
    tf_output = tf_reference*tf_closed_loop
    
    # Now by finding output transfer function's impulse reponse, we can see it's behaviour in time domain.
    duration = 5
    # Output will be computed for this many seconds.
    t = np.linspace(0, duration, num = int(duration/(TIME_STEP*1e-3)))
    t, output = impulse_response(tf_output, t)

    # Let's plot the panel's expected angle vs time.
    plt.plot(t, output)
    plt.plot(t, target_position*np.ones(len(t)))
    plt.ylabel(f'Expected Angle for K_d = {K_d} (rad)')
    plt.xlabel('Time (s)')
    plt.show()

# Does the angle of the arm converge to the desired point according to the plots?
# Compare your answer to pi controller example.
# Considering the plots, can pd perform better in terms of overshoot or settling time compared to p controller?

# Controller function is defined.
def get_controller_output(K_p, K_d, errors):
    return (K_p*errors[-1] + K_d*np.gradient(errors)[-1]/(TIME_STEP*1e-3))
    # Gradient function is used in order to compute the numerical derivative of the error.

sim = Propeller_Simulation(initial_position = 0, disturbance = 0, noise = 0)

K_p = 3
K_d = 1
errors = [0] # Initial error is set.
# Having to set an initial error shows that perfect d controller is not realizable.

while True:
    # At each time step, control output is given to the plant as input.
    error = target_position - sim.get_current_angle() # Error is computed.
    errors.append(error) # Errors are kept in a list in order to compute the derivative.
    controller_output = get_controller_output(K_p, K_d, errors)
    sim.set_velocity(controller_output)

    time.sleep(TIME_STEP*1e-3)

# Add some noise and disturbance to see the effects on the result.
# Are the negative effects of noise and disturbance amplified by the pd controller?
# Compare the answer to pi controller