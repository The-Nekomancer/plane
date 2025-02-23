'''
PURPOSE: This file plots data of the GA, before its passed to OpenVSP
THIS FILE IS NO LONGER NEEDED, but theres no harm in leaving it in, might be useful later
'''

import matplotlib.pyplot as plt
from Plane_Class import Plane
import numpy as np

def performance_plotter(CL,CD,LD,Alpha,final):
    
    '''CL VS Alpha'''
    fig = plt.figure(1)
    plt.plot(Alpha[0:61],CL[0:61])
    plt.title("CL and Alpha")
    plt.xlabel("Alpha")
    plt.ylabel("CL")
    plt.grid()
    plt.show()
    
    '''CL VS Alpha'''
    fig = plt.figure(2)
    plt.plot(Alpha[0:61],CD[0:61])
    plt.title("CD and Alpha")
    plt.xlabel("Alpha")
    plt.ylabel("CD")
    plt.grid()
    plt.show()
    
    
    '''CL VS Alpha'''
    fig = plt.figure(3)
    plt.plot(Alpha[0:61],LD[0:61])
    plt.title("L/D and Alpha")
    plt.xlabel("Alpha")
    plt.ylabel("L/D")
    plt.grid()
    plt.show()

    '''Power Required Curve'''
    thrust = []
    velocities = []
    power = []
    for k in range(15):
        final.alpha = k
        for i in range(len(final.motor)):
            thrust.append(Plane.motors[final.motor_num].loc[i,'Thrust (kg)'])
            power.append(Plane.motors[final.motor_num].loc[i,'Inputpower (W)'])
            final.throttle = i
            final.calc_velocity()
            velocities.append(final.cruise_velocity)
    
    print("Thrust (kg): " + str(thrust))
    print("Power (W): " + str(power))
    fig = plt.figure(4)
    plt.plot(velocities,power)
    plt.title("Power Required Curve")
    plt.xlabel("Velocity (m/s)")
    plt.ylabel("Power (W)")
    plt.grid()
    plt.show()