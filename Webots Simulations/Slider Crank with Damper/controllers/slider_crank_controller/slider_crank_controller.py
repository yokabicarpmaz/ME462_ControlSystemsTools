#In this simulation, the same slider crank mechanism
#is considered with a damper attached to the slider
#from the base. resulting rpm from the first minute of
#simulation is calculated.
#The damping coefficient can be changed from
#jointParameters of SLIDER_JOINT which is attached
#to the slider.

from controller import Robot, Motor, PositionSensor
import sys
from control import tf,impulse_response
import numpy as np

timestep = 4

robot = Robot()
motor = robot.getMotor("servo")
sensor=robot.getPositionSensor("sensor")
sensor.enable(timestep)

steps_passed=0

#motor parameters
Kf=0.1
Lf=1
Rf=1
V=5

#motor transfer function
#transient effects are considered
num=[Kf]
den=[Lf, Rf]
plant=tf(num,den)

#voltage input to the motor is a step input
input=tf([V],[1, 0])

#resulting torque output of the motor
output=input*plant

#duration of the simulation
duration=60
t = np.linspace(0, duration, num = int(duration/(timestep*1e-3)))
t, output = impulse_response(output, t)

steps_passed=0
sensor_read=0
while robot.step(timestep) != -1:
    motor.setTorque(output[steps_passed])
    steps_passed=steps_passed+1
    if steps_passed>duration*1000/timestep-1:
        sensor_value=sensor.getValue()
        rpm=sensor_value/3.14/2
        print("Revolutions per minute: %8.2f "%(sensor_value))
        sys.exit()
        

