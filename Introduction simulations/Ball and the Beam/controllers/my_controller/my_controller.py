from controller import Robot, Motor, DistanceSensor
import sys
import matplotlib.pyplot as plt
import numpy as np
robot = Robot()
TIME_STEP = 8
error=0
cumulative_error=0
error_log=[]
total_time=0
sensor=robot.getDistanceSensor("sensor")
sensor.enable(TIME_STEP)
motor = robot.getMotor("servo")

Kp=0.6
Ki=0.05
Kd=0.1

def Controller(Kp,Ki,Kd, error,previous_error, cumulative_error, TIME_STEP):
    target_position=error*Kp+Ki*cumulative_error+(error-previous_error)/(TIME_STEP/1000)*Kd
    motor.setPosition(target_position)
    if abs(error)>500:
        print("Try again")
        sys.exit(0)

def normalizeError(sensor_value):
    error=sensor_value-477
    error_normalized=-error/500
    return error_normalized


while robot.step(TIME_STEP) != -1:
    previous_error=error
    error=normalizeError(sensor.getValue())
    error_log.append(error)
    cumulative_error += (TIME_STEP/1000)*(error+previous_error)/2
    Controller(Kp,Ki,Kd,error, previous_error, cumulative_error, TIME_STEP)
    total_time+=TIME_STEP
    if total_time>10000:
        x=np.arange(0, total_time, TIME_STEP).tolist()
        plt.plot(x,error_log)
        plt.show() 
        sys.exit(0)
        


    
    