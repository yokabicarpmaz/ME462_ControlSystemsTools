from controller import Robot, Motor, Keyboard
import random
import math
from threading import Thread
import time

TIME_STEP = 64

class Propeller_Simulation:

    def __init__(self):
        self.motor_velocity = 1
        self.max_motor_velocity = 0.6
        start_thread = Thread(target = self.start_simulation, args = ())
        start_thread.start()
    
    def start_simulation(self):
        robot = Robot()
        keyboard = Keyboard()
        keyboard.enable(TIME_STEP)
        
        motor = robot.getMotor('motor')
        visual = robot.getMotor('visual')
        motor.setVelocity(0)
        motor.setPosition(float('inf'))
        visual.setVelocity(0)
        visual.setPosition(float('inf'))
        visual.setTorque(100)
       
        while robot.step(TIME_STEP) != -1:
            print(self.motor_velocity)
            motor.setVelocity(self.motor_velocity)
            visual.setVelocity(150*self.motor_velocity)
            

    def set_velocity(self, input):
        self.motor_velocity = sorted([-self.max_motor_velocity, input, self.max_motor_velocity])[1]
        