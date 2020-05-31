from controller import Robot, Motor, PositionSensor
import sys
import numpy as np

desired_angle=180  #give input from here
                   #desired angle of green link, with respect to ground
timestep = 8
robot = Robot()
sensor=robot.getPositionSensor("sensor")
sensor.enable(timestep)
motor = robot.getMotor("servo1")
step=0
angle_in_deg=desired_angle-90
angle_in_rad=angle_in_deg*np.pi/180

while robot.step(timestep) != -1:
    motor.setPosition(angle_in_rad)
    step=step+1 
    if (step>375):
        change_in_radians=sensor.getValue()
        change_in_degrees=change_in_radians*180/np.pi
        initial_in_degrees=60.7
        final_angle=initial_in_degrees-change_in_degrees
        print("Angle of the yellow link with respect to the ground:",end=" ")
        print(final_angle)
        print("Pause and reset the simulation to try another angle")
        sys.exit()
    
    pass