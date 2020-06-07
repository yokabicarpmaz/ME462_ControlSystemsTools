# IF YOU ENCOUNTER ANY IRREGULARITIES IN THE PHYSICS
# OF THE MODEL, CLOSE WITHOUT SAVING AND REOPEN.

from controller import Robot, Motor, DistanceSensor
import sys
import matplotlib.pyplot as plt
import numpy as np
robot = Robot()
total_time=0 

#frequency at which control commands will be given, in milliseconds
TIME_STEP = 8 

#initial conditions of error variables
error=0        
cumulative_error=0

#array in which error history will be stored
error_log=[]
   
  

#defining distance sensor which will generate feedback signal for the system
#sensor can be seen at the left end of the beam
sensor=robot.getDistanceSensor("sensor")
#frequency that sensor scans the distance is the same as control frequency 
sensor.enable(TIME_STEP)

#defining the motor that drive the gear at the bottom left
motor = robot.getMotor("servo")

##INPUT HERE## PID parameters
Kp=0.9
Ki=0.05
Kd=0.1
##INPUT HERE##

#function that calculates required position of the motor and sends command to the motor
def Controller(Kp,Ki,Kd, error,previous_error, cumulative_error, TIME_STEP):
    target_position=error*Kp+Ki*cumulative_error+(error-previous_error)/(TIME_STEP/1000)*Kd
    motor.setPosition(target_position)
    if abs(error)>500:
        print("Try again")
        sys.exit(0)

#since distance input is taken with respect to the left end of the beam
#it should be calibrated to the middle first and then normalized
#to make pid parameters more formal
def normalizeError(sensor_value):
    error=sensor_value-477
    error_normalized=-error/500
    return error_normalized


#main loop of the controller
while robot.step(TIME_STEP) != -1: 
    previous_error=error
    error=normalizeError(sensor.getValue())
    error_log.append(error)
    cumulative_error += (TIME_STEP/1000)*(error+previous_error)/2
    Controller(Kp,Ki,Kd,error, previous_error, cumulative_error, TIME_STEP)
    total_time+=TIME_STEP
    if total_time>10000:  #simulation will be running for 10 seconds
        x=np.arange(0, total_time, TIME_STEP).tolist()
        plt.plot(x,error_log)
        plt.show() 
        sys.exit(0)
        


    
    