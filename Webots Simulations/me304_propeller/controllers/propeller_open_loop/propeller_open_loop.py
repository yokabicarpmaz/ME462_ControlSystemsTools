# The objective of this example is to demonstrate the design of a very simple open loop controller.
# By adding disturbance,the shortcoming of an open loop controller can also be observed.
# The purpose of the controller is to keep the blue objet horizontal as in the initial position.

import sys, os
sys.path.append(os.path.abspath(os.path.join('..')))

from propeller_helper import Propeller_Simulation, TIME_STEP
import time
import math

# Firstly, the model of the system can be represented as
# J*a = T_p + m*g*sin(x)*L/2 + b*v
# Where J is the moment of inertia of the arm,
# a is the angular acceleration,
# T_p is the torque caused by the propeller,
# m is the mass of the arm,
# g is gravitational acceleration,
# x is the angular position of the arm (initially -90 degrees),
# L is the length of the arm,
# b is the damping coefficient of the revolute joint,
# v is the angular velocity of the arm.
# Assuming the system will always be around the desired situation,
# some simplifications can be made.
#     -Firstly, v will be around 0 since the arm is supposed to be stationary.
#     -Secondly, a will be around 0 since v is constant and 0.
#     -Lastly, x will be around -90 degrees since the arm is supposed to stay horizontal.
# Note that these assumptions could help us linearize the system if a more complicated design was considered.
# But in this case, we will assume static equilibrium and constant, x, v, a.

# T_p can be represented as F_p*L where F_p is the force induced by the propeller.
# Therefore the final equation becomes F_p = -m*g/2
# Assuming F_p = v_p

m = 0.1
L = 0.3
g = 9.81

v_p = -m*g/2

sim = Propeller_Simulation(disturbance = 0, initial_position = -math.pi/2)
sim.set_velocity(v_p)

# Now by playing with the disturbance, one can observe that the results are not nearly as good.
# How does the open loop controller work for different initial angular positions?
