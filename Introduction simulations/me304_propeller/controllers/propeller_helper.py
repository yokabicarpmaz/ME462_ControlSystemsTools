from controller import Robot, Motor, Keyboard
import random
import math
from threading import Thread
import time

TIME_STEP = 32

class Propeller_Simulation:

    def __init__(self, disturbance = 0, initial_position = 0, noise = 0):
        self.noise = noise
        self.started = False
        self.current_angle = 0
        self.initial_position = initial_position + math.pi/2
        self.disturbance = disturbance
        self.motor_velocity = 1
        self.length = 0.3
        self.max_motor_velocity = 0.6
        start_thread = Thread(target = self.start_simulation, args = ())
        start_thread.start()
    
    def start_simulation(self):
        robot = Robot()
        keyboard = Keyboard()
        keyboard.enable(TIME_STEP)
        
        motor = robot.getMotor('propeller')
        visual = robot.getMotor('visual')
        sensor = robot.getPositionSensor('sensor')
        sensor.enable(TIME_STEP)
        motor.setVelocity(100)
        motor.setPosition(self.initial_position)
        
        visual.setVelocity(0)
        visual.setPosition(float('inf'))
        visual.setTorque(100)
        
       
        while robot.step(TIME_STEP) != -1:
            if not self.initial_position_reached(sensor):
                continue
            else:
                motor.setVelocity(0)
                motor.setPosition(float('inf'))
            self.current_angle = sensor.getValue()
            motor.setTorque(self.motor_velocity*self.length + self.disturbance * (random.random()-0.5))
            visual.setVelocity(150*self.motor_velocity)
            

    def set_velocity(self, input):
        self.motor_velocity = sorted([-self.max_motor_velocity, input, self.max_motor_velocity])[1]
        
    def initial_position_reached(self, sensor):
        if abs(sensor.getValue() - self.initial_position) < 1e-3:
            self.started = True
        return self.started
    
    def get_current_angle(self):
        return self.current_angle + math.pi/2 + self.noise*(random.random() - 0.5)