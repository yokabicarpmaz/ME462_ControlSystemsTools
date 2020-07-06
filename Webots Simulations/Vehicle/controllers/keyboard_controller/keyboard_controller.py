"""keyboard_controller."""

#OPEN-LOOP KEYBOARD CONTROLLED VEHICLE

"""
In this simulation, The vehicle gets input from user's keyboard command and acts accordingly.
The purpose of this simulation is to understand open-loop system's response. 
Besides, it can be used to see the differences between open and closed loop 
systems with following simulations.
"""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, Keyboard
from controller import Robot, Motor, Keyboard
import time


TIME_STEP = 64  #timestep should be the same as in the WorldInfo
# create the Robot and Keyboard instance.
robot = Robot()
keyboard = Keyboard()
keyboard.enable(TIME_STEP)
# assign the motors to wheels.
wheels = []
wheelsNames = ['wheel1', 'wheel2', 'wheel3', 'wheel4']
for i in range(4):
    wheels.append(robot.getMotor(wheelsNames[i]))
    wheels[i].setPosition(float('inf'))  #set position infinity not to restrict motion 
    wheels[i].setVelocity(0.0)  #set initial speed as 0 
   

leftSpeed = 0.0
rightSpeed = 0.0

print('Click the simulation window before the keyboard command!')
print('Press [W] or [w] to move forward')
print('Press [S] or [s] to move backward')
print('Press [D] or [d] to turn right')
print('Press [A] or [a] to turn left')

while robot.step(TIME_STEP) != -1:
    key = keyboard.getKey()  #allow to get keyboard command
    if key == ord('W') or key == ord('w'):
        #set forward speed as 15 rad/s
        leftSpeed = 15.0 
        rightSpeed = 15.0  
    elif key == ord('S') or key == ord('s'): 
        #set backward speed as 15 rad/s
        leftSpeed = -15.0
        rightSpeed = -15.0 
    elif key == ord('D') or key == ord('d'):
        #set leftwheel speed as 15 rad/s to turn right
        leftSpeed = 15.0
        rightSpeed = 0.0 
    elif key == ord('A') or key == ord('a'):
        #set rightwheel speed as 15 rad/s to turn left
        leftSpeed = 0.0
        rightSpeed = 15.0         
    else:
        #if there is no keyboard command, vehicle will stop
        leftSpeed = 0.0
        rightSpeed = 0.0
    # set velocity to wheels(motor) according to keyboard command
    wheels[0].setVelocity(leftSpeed)
    wheels[1].setVelocity(leftSpeed)
    wheels[2].setVelocity(rightSpeed)
    wheels[3].setVelocity(rightSpeed)
    
    pass


