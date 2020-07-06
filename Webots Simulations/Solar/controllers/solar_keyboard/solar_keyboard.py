"""solar_keyboard controller."""

# This simulation is prepared in order to demonstrate the job of a controller.
# The user can apply torque on the solar panel by pressing 'A' and 'D' keys.
# The purpose is to constantly keep the solar panel towards Sun.
# Based on the success of the run, the energy harvested will be printed at the end of the simulation.
# The user uses his/her eyes as a sensor in order to observe the angle of the panel.
# Similarly, angle of the Sun is taken as a reference input by the user.
# Then by making the decision of pressing either 'A' or 'D', the user performs the job of a controller.

# During ME304, you will learn different control methods which can be used in order to decide
# the direction and magnitude of the torque which should be applied.

import sys, os
sys.path.append(os.path.abspath(os.path.join('..')))
from solar_helper import Solar_Simulation, TIME_STEP
# solar_keyboard_helper.py file has a Solar_Simulation class in order to make the code simpler.
from controller import Keyboard
import time

keyboard = Keyboard()
keyboard.enable(TIME_STEP)

sim = Solar_Simulation(moving_sun = True)
# The simulation is initiated.
# moving_sun parameter can be set True or False in order to set the behaviour of the Sun.

# In the below loop, the key press is checked and the corresponding torque is applied.
while True:
    key = keyboard.getKey()
    if key == ord('A'):
        sim.set_torque(1)
    elif key == ord('D'):
        sim.set_torque(-1)
    else:
        sim.set_torque(0)

    time.sleep(TIME_STEP*1e-3)