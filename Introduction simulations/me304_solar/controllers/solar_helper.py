from controller import Robot, Motor, Keyboard
import random
import math
from threading import Thread

TIME_STEP = 32

class Solar_Simulation:

    def __init__(self, moving_sun = True, noise = 0, disturbance = 0, controller_output = []):
        self.controller_output = controller_output
        self.noise = noise
        self.moving_sun = moving_sun
        self.motor_torque = 0
        self.max_motor_torque = 10
        #self.max_power = 1
        self.time_limit = 5
        self.max_sun_position = 1.57
        self.sun_velocity = 0.3
        self.sun_position = -1.57
        self.panel_position = -1.57
        self.disturbance = disturbance
        start_thread = Thread(target = self.start_simulation, args = ())
        start_thread.start()
    
    def start_simulation(self):
        self.total_energy = 0
        robot = Robot()
        keyboard = Keyboard()
        keyboard.enable(TIME_STEP)
        
        #camera = robot.getCamera('view')
        #camera.enable(TIME_STEP)
        motor = robot.getMotor('motor')
        sun_motor = robot.getMotor('sun_motor')
        panel_sensor = robot.getPositionSensor('panel_sensor')
        sun_sensor = robot.getPositionSensor('sun_sensor')
        panel_sensor.enable(TIME_STEP)
        sun_sensor.enable(TIME_STEP)

        
        if self.moving_sun:
            sun_motor.setVelocity(self.sun_velocity)
            sun_motor.setPosition(self.max_sun_position)
        else:
            sun_motor.setVelocity(10)
            random_pos = random.random()*math.pi - math.pi/2
            sun_motor.setPosition(0)
            while(abs(sun_sensor.getValue() - random_pos) > 1e-2):
                time.sleep(0.1)
        
        printed = False
        t = 0
        i = 0
        while robot.step(TIME_STEP) != -1:
            sun_position = sun_sensor.getValue()
            panel_position = panel_sensor.getValue()
            self.sun_position = sun_position
            self.panel_position = panel_position
            
            if list(self.controller_output):
                self.set_torque(self.controller_output[i])
            
            if (self.moving_sun and abs(sun_position - self.max_sun_position) < 1e-1):
                if not printed:
                    print(f"Energy harvested: {self.total_energy} J")
                printed = True
                continue
            
            motor.setTorque(self.motor_torque + self.disturbance * (random.random()-0.5))
            self.total_energy += max([0, 1 - abs(panel_position-sun_position)])*TIME_STEP
            t += TIME_STEP*1e-3
            i += 1
    
    def set_torque(self, input):
        self.motor_torque = sorted([-self.max_motor_torque, input, self.max_motor_torque])[1]
        
    def get_sun_angle(self):
        return self.sun_position + (self.noise*(random.random()-0.5))
    
    def get_panel_angle(self):
        return self.panel_position + (self.noise*(random.random()-0.5))