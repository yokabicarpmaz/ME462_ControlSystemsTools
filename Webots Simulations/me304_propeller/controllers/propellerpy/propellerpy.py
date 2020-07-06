from propeller_keyboard_helper import Propeller_Simulation, TIME_STEP
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
        
    time.sleep(1/TIME_STEP)