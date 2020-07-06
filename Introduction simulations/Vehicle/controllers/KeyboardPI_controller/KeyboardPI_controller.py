"""keyboardPI_controller."""

# CLOSED-LOOP PI CONTROLLED VEHICLE
# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
import sys
from controller import Robot, Motor, Keyboard
from controller import PositionSensor, GPS
import time
import numpy as np
import matplotlib.pyplot as plt
import math

TIME_STEP = 64  #timestep should be the same as in the WorldInfo
# create the Robot, Keyboard, GPS instance.
robot = Robot()
keyboard = Keyboard()
keyboard.enable(TIME_STEP)
gps = GPS('global')
gps.enable(TIME_STEP)
# assign the motors to wheels.
wheels = []
wheelsNames = ['wheel1', 'wheel2', 'wheel3', 'wheel4']
for i in range(4):
    wheels.append(robot.getMotor(wheelsNames[i]))
    wheels[i].setPosition(float('inf')) #set position infinity not to restrict motion
    wheels[i].setVelocity(5.0) #set initial speed as 5.0 rad/s
    
print('Click the simulation window before the keyboard command!')
print('Press [D] or [d] to give right input')
print('Press [A] or [a] to give left input')  
   
time = 0
leftSpeed = 0.0
rightSpeed = 0.0
carSpeed = 5.0
buttonLeftSpeed = 0.0
buttonRightSpeed = 0.0
target_position= 0.0
controlled_velocity = 0.0
Kp = 3  #Proportional Gain
Ki = 0.01  #Integral Gain
gps_log = []
error_log = []

def Controller(Kp,Ki,Error,cumulative_error,TIME_STEP):
    controlled_velocity = (Error * Kp + cumulative_error * Ki) / (2*math.pi)
    #controlled velocity which is converted to rad/s
    return controlled_velocity

while robot.step(TIME_STEP) != -1:
    key = keyboard.getKey()  #allow to get keyboard command
    if key == ord('D') or key == ord('d'):
        #set leftwheel speed as 10.0 rad/s to turn right
        buttonLeftSpeed = 10.0
        buttonRightSpeed = 0.0 
        print("ehehe")
    elif key == ord('A') or key == ord('a'):
        #set rightwheel speed as 10.0 rad/s to turn left
        buttonLeftSpeed = 0.0
        buttonRightSpeed = 10.0       
    else:
        #if there is no keyboard command, vehicle will stop
        buttonLeftSpeed = 0.0
        buttonRightSpeed = 0.0      
        
    time +=TIME_STEP    
    read_position= gps.getValues() 
    error = target_position-read_position[0]
    error_log.append(error)
    cumulative_error = np.sum(error_log)*(TIME_STEP*1e-3)
    gps_log.append(read_position[0])
    controlled_velocity = Controller(Kp,Ki,error,cumulative_error,TIME_STEP)
        
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
    
        
    leftSpeed = leftSpeed + buttonLeftSpeed  
    rightSpeed = rightSpeed + buttonRightSpeed
    # set velocity to wheels(motor) according to controlled speed          
    
    wheels[0].setVelocity(leftSpeed)
    wheels[1].setVelocity(leftSpeed)
    wheels[2].setVelocity(rightSpeed)
    wheels[3].setVelocity(rightSpeed)
    
    if time>300000: #After 300 s, simulation will stop and plot will be showed.
        x=np.arange(0, time, TIME_STEP).tolist()
        plt.plot(x,gps_log)
        plt.ylabel('The Position of the Vehicle [m]')
        plt.xlabel('Time [ms]')
        plt.show() 
        sys.exit(0)
   
    pass

# Enter here exit cleanup code.
