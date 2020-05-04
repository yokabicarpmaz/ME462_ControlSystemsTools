"""solar_open_loop controller."""

# This simulation is prepared in order to demonstrate an example of an open loop controller.
# The controller will output the desired motor torque aimilar to the previous example where the user used his/her keyboard.
# The controller is supposed to give an output which is not based on the position of the sun.
# However, controller output can still vary with respect to time.

import sys, os
sys.path.append(os.path.abspath(os.path.join('..')))
from solar_helper import Solar_Simulation, TIME_STEP

# solar_keyboard_helper.py file has a Solar_Simulation class in order to make the code simpler.
from controller import Keyboard
import time
from control import tf, impulse_response
import numpy as np
from scipy import signal


# Mass of the panel is 0.25 kg.
# The mass can also assumed as lumped 2 meters away from rotating axis.
# Damping coefficient b, of the rotating axis is 0.1 N*s/rad.
m = 0.25
r = 2
b = 0.1

# Moment of inertia can be calculated as such
J = m*r**2

# Now using the previous examples, the transfer function of the plant can be calculated
num = [1]
den = [J, b, 0]
tf_plant = tf(num, den)

# The output signal we would like to have is the angle of Sun which is a ramp signal.
# Ramp signal's Laplace transform is a/s^2, where a is the amplitude.
# In our case, the angular velocity of Sun is 0.3rad/s.
tf_output = tf([0.3], [1, 0, 0])

# Finally we should have an idea of what the input to our controller is.
# Let's say, the controller will have a step input representing it's supposed to work.
tf_input = tf([1], [1, 0])

# Finally, we can represent the controller output as tf_output = tf_input*tf_controller*tf_plant
# Then tf_controller can be calculated as tf_controller = tf_output/(tf_input*tf_plant)
tf_controller = tf_output/(tf_input*tf_plant)
print(f"Controller transfer function is {tf_controller}")

# As printed, the numerator of tf_controller has a higher order than its denominator.
# This controller is not realizable.
# However, if we multiply tf_controller by 1/s, and observe the resulting transfer function;
# we can observe that the output is realizable.

tf_output = tf_controller*tf([1], [1, 0])
print(f"Output transfer function is {tf_output}")

# It is expected to observe an impulse and a step function as the inverse transform of the controller output.
duration = 14
t = np.linspace(0, 5, num = int(duration/(TIME_STEP*1e-3)))
t, output = impulse_response(tf_output, t)

# Let's check if the output is as expected by printing the first 10 values.
print(f"First 10 values of output: {output[:10]}")

# It looks like the step function is there but the impulse is missing. (There should be a warning by the library.)
# We can add the impulse manually.
impulse_length = 14 # Impulse must be added to a small finite length
impulse_magnitude = 0.3
for i in range(impulse_length):
    output[i] += impulse_magnitude/(impulse_length*TIME_STEP*1e-3)


sim = Solar_Simulation(disturbance = 0) # The simulation is initiated.
# Now you can play with the disturbance parameter and observe the change in the performance of the open loop controller.
# For this example, disturbance adds a random torque to the plant input. This could be the effent of wind in real life.
# If the disturbance has a bad effect on the performance, how could you overcome this problem?

for o in output:
    sim.set_torque(o)
    time.sleep(TIME_STEP*1e-3)