from controller import Robot, Motor
import math
import numpy as np
from threading import Thread
import matplotlib.pyplot as plt

class MSD:

    def __init__(self, excitation_frequency, exciatation_amplitude, duration = 50):
        self.excitation_frequency = excitation_frequency
        self.exciatation_amplitude = exciatation_amplitude
        self.duration = duration
        self.done = False
        self.position_history = []
        
        start_thread = Thread(target = self.start_simulation, args = ())
        start_thread.start()
        
    def start_simulation(self):
        robot = Robot()
        
        self.TIME_STEP = int(robot.getBasicTimeStep())

        motor = robot.getMotor('motor')
        motor.setForce(0)
        motor.setPosition(float('inf'))
        ps = robot.getPositionSensor('sensor')
        ps.enable(self.TIME_STEP)

        t = 0
        while robot.step(self.TIME_STEP) != -1 and t < self.duration:
            force = self.exciatation_amplitude*math.sin(self.excitation_frequency*t)
            motor.setForce(force)
            self.position_history.append(ps.getValue())
            t += self.TIME_STEP*1e-3
            pass
        self.done = True

    def get_position_history(self):
        return self.position_history

def get_phase_magnitude(time_signal, duration, timestep):
    t_samples = np.linspace(0, duration, len(time_signal))
    freq_response = np.abs(np.fft.fft(time_signal))[:round(len(t_samples)/2)]
    freq_x = np.linspace(0, 1e3*2*np.pi/(2*timestep), len(freq_response))
    dominant_freq = freq_x[np.argmax(freq_response)]
    
    A = np.trapz(np.multiply(time_signal, [np.sin(dominant_freq*t) for t in t_samples]))
    B = np.trapz(np.multiply(time_signal, [np.cos(dominant_freq*t) for t in t_samples]))
    
    steady_portion = time_signal[int(len(time_signal)*9/10):]
    return [np.arctan2(B, A), np.max(steady_portion) - np.min(steady_portion)]
