# The objective of this example is to demonstrate the aim of the controller in a physical system.
# The user can set the angular velocity of the propeller by pressing A and D buttons.

import sys, os
sys.path.append(os.path.abspath(os.path.join('..')))

from propeller_helper import Propeller_Simulation, TIME_STEP
from controller import Keyboard
import time

keyboard = Keyboard()
keyboard.enable(TIME_STEP)


sim = Propeller_Simulation()
while True:
    key = keyboard.getKey()
    if key == ord('A'):
        sim.set_velocity(0.6)
    elif key == ord('D'):
        sim.set_velocity(-0.6)
    else:
        sim.set_velocity(0)
        
    time.sleep(TIME_STEP*1e-3)