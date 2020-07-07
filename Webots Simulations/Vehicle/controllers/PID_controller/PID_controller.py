"""PID_controller."""
# This controller is compatible with 'vehicle_closedloop' world.

# CLOSED-LOOP PID CONTROLLED VEHICLE

"""
In this simulation, There is a disturbance between 2 and 3 seconds due to the wind.
The vehicle try to return the track.One of the purposes of this simulation is to understand PID-controller
effects on system's response. Besides, the differences between open and closed loop 
systems can be observed. Another purpose is to show the transient and steady-state
response of system.
"""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, GPS
import sys
from controller import Robot, Motor
from controller import GPS
import time
import numpy as np
import matplotlib.pyplot as plt
import math

TIME_STEP = 64  #timestep should be the same as in the WorldInfo
# create the Robot, GPS instance.
robot = Robot()
gps = GPS('global')
gps.enable(TIME_STEP)
# assign the motors to wheels.
wheels = []
wheelsNames = ['wheel1', 'wheel2', 'wheel3', 'wheel4']
for i in range(4):
    wheels.append(robot.getMotor(wheelsNames[i]))
    wheels[i].setPosition(float('inf')) #set position infinity not to restrict motion
    wheels[i].setVelocity(5.0) #set initial speed as 5.0 rad/s
   
   
time = 0
leftSpeed = 0.0
rightSpeed = 0.0
carSpeed = 5.0
windLeftSpeed = 0.0
windRightSpeed = 0.0
target_position= 0.0
controlled_velocity = 0.0
Kp = 2  #Proportional Gain
Ki = 0.01  #Integral Gain
Kd = 0.5  #Derivative Gain
gps_log = []
error_log = []
previous_error = 0
error = 0

def Controller(Kp,Ki,Kd,Error,cumulative_error,previous_error,TIME_STEP):  #PID-controller function
    controlled_velocity = (Error * Kp + cumulative_error * Ki + previous_error * Kd) / (2*math.pi)
    #controlled velocity which is converted to rad/s
    return controlled_velocity

while robot.step(TIME_STEP) != -1:  # Main loop:
# - perform simulation steps until Webots is stopping the controller
        
    time +=TIME_STEP    
    read_position= gps.getValues()
    previous_error = error 
    error = target_position-read_position[0]
    error_log.append(error)
    cumulative_error = np.sum(error_log)*(TIME_STEP*1e-3)
    gps_log.append(read_position[0])
    controlled_velocity = Controller(Kp,Ki,Kd,error,cumulative_error,previous_error,TIME_STEP)
        
    if error > 0:
        # error > 0 means the vehicle is in the left side of the road
        leftSpeed = carSpeed-controlled_velocity 
        rightSpeed = carSpeed+controlled_velocity
        if time>300000:
        # After 300 seconds the vehicle will stop
            leftSpeed = 0.0
            rightSpeed = 0.0 
    elif error < 0:
        # error < 0 means the vehicle is in the right side of the road
        leftSpeed = carSpeed-controlled_velocity
        rightSpeed = carSpeed+controlled_velocity  
        if time>300000:
        # After 300 seconds the vehicle will stop
            leftSpeed = 0.0
            rightSpeed = 0.0     
    else:
        # error = 0 means the vehicle is in the right track then
        # it will move on with initial speed
        leftSpeed = carSpeed
        rightSpeed = carSpeed  
    
    if time >= 2000 and time < 3000:
        windRightSpeed = 10.0
        windLeftSpeed = 0.0
    else:
        windRightSpeed = 0.0
        windLeftSpeed = 0.0    
        
    leftSpeed = leftSpeed + windLeftSpeed  
    rightSpeed = rightSpeed + windRightSpeed          
    # set velocity to wheels(motor) according to controlled speed
    wheels[0].setVelocity(leftSpeed)
    wheels[1].setVelocity(leftSpeed)
    wheels[2].setVelocity(rightSpeed)
    wheels[3].setVelocity(rightSpeed)
    
    if time>300000:  #After 300 s, simulation will stop and plot will be showed.
        x=np.arange(0, time, TIME_STEP).tolist()
        plt.plot(x,gps_log)      
        plt.ylabel('The Position of the Vehicle [m]')
        plt.xlabel('Time [ms]')
        plt.show()
        sys.exit(0)
   
    pass