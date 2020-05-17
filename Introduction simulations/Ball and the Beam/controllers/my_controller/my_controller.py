from controller import Robot, Motor, DistanceSensor
import sys
robot = Robot()
TIME_STEP = 8
sensor=robot.getDistanceSensor("sensor")
sensor.enable(TIME_STEP)
motor = robot.getMotor("servo")

while robot.step(TIME_STEP) != -1:
    sensor_value=sensor.getValue()
    error=sensor_value-477
    error_normalized=-error/500
    Kp=0.8
    target_position=error_normalized*Kp
    print(error)
    motor.setPosition(target_position)
    if abs(error)>500:
        print("Try again")
        sys.exit(0)
