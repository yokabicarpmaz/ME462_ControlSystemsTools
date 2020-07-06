from controller import Robot, Motor, PositionSensor
import sys

timestep = 16

robot = Robot()
motor = robot.getMotor("servo")
sensor=robot.getPositionSensor("sensor")
sensor.enable(timestep)

steps_passed=0

desired_angle=3.14  #in radians

while robot.step(timestep) != -1:
    motor.setPosition(desired_angle)
    steps_passed=steps_passed+1
    if steps_passed>150:
        sensor_value=sensor.getValue()*1000
        print("Displacement of the slider: %8.2f mm "%(sensor_value))
        sys.exit()
        

