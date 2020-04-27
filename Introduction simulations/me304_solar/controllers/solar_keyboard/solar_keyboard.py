"""solar_keyboard controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor


from solar_keyboard_helper import Solar_Simulation, TIME_STEP
from controller import Keyboard
import time

keyboard = Keyboard()
keyboard.enable(TIME_STEP)

sim = Solar_Simulation(True)

while True:
    key = keyboard.getKey()
    if key == ord('A'):
        sim.set_torque(1)
    elif key == ord('D'):
        sim.set_torque(-1)
    else:
        sim.set_torque(0)
        
    time.sleep(1/TIME_STEP)