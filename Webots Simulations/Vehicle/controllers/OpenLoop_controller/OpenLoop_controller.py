"""OpenLoop_controller."""
# This controller is compatible with 'vehicle.wbt' world

# OPEN-LOOP VEHICLE

"""
In this simulation, The vehicle has an open-loop system.
The purpose of this simulation is to understand 
the difference between open and closed-loop systems.
"""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, Keyboard
from controller import Robot, Motor
import time


TIME_STEP = 64  #timestep should be the same as in the WorldInfo
# create the Robot and Keyboard instance.
robot = Robot()
# assign the motors to wheels.
wheels = []
wheelsNames = ['wheel1', 'wheel2', 'wheel3', 'wheel4']
for i in range(4):
    wheels.append(robot.getMotor(wheelsNames[i]))
    wheels[i].setPosition(float('inf'))  #set position infinity not to restrict motion 
    wheels[i].setVelocity(0.0)  #set initial speed as 0 
   

leftSpeed = 0.0
rightSpeed = 0.0
time = 0

while robot.step(TIME_STEP) != -1:
    time += TIME_STEP

    if time < (TIME_STEP*205):
        leftSpeed = 20.0
        rightSpeed = 20.0
    elif time >= (TIME_STEP*205) and time < (TIME_STEP*245):
        leftSpeed = 20.0
        rightSpeed = 15.0
    elif time >= (TIME_STEP*245) and time < (TIME_STEP*262):
        leftSpeed = 20.0
        rightSpeed = 19.6
    elif time >= (TIME_STEP*262) and time < (TIME_STEP*605):
        leftSpeed = 20.0
        rightSpeed = 20.0
    elif time >= (TIME_STEP*605) and time < (TIME_STEP*644):
        leftSpeed = 20.0
        rightSpeed = 15.0
    elif time >= (TIME_STEP*644) and time < (TIME_STEP*650):
        leftSpeed = 20.0
        rightSpeed = 19.6
    elif time >= (TIME_STEP*650) and time < (TIME_STEP*820):
        leftSpeed = 20.0
        rightSpeed = 20.0
    elif time >= (TIME_STEP*820) and time < (TIME_STEP*862):
        leftSpeed = 20.0
        rightSpeed = 15.0
    elif time >= (TIME_STEP*862) and time < (TIME_STEP*880):
        leftSpeed = 20.0
        rightSpeed = 19.6
    elif time >= (TIME_STEP*880) and time < (TIME_STEP*1200):
        leftSpeed = 20.0
        rightSpeed = 20.0
    elif time >= (TIME_STEP*1200) and time < (TIME_STEP*1310):
        leftSpeed = 10.0
        rightSpeed = 10.0
    else: 
        leftSpeed = 0.0
        rightSpeed = 0.0
        
        
    # set velocity to wheels(motor) according to keyboard command
    wheels[0].setVelocity(leftSpeed)
    wheels[1].setVelocity(leftSpeed)
    wheels[2].setVelocity(rightSpeed)
    wheels[3].setVelocity(rightSpeed)
    
    pass


