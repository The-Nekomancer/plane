# -*- coding: utf-8 -*-

from Plane_Class import Plane
import fuse_equations
# import numpy as np
import matplotlib.pyplot as plt


obj = Plane(payload_mass = 2, priority = Plane.priority[0])
i = 1
old_mass = obj.mass
mass_index = [obj.mass]
wingspan = [obj.wingspan]
chord = [obj.chord_length]
vel = [obj.cruise_velocity]
S = [obj.chord_length * obj.wingspan]
endurence = []
rang = []
stall_speed = []
x = [i]
t = []

e = 1
while e > 0.000001:
    obj.calc_mass()
    obj.calc_endurance()
    obj.calc_range()
    obj.calc_lift()
    obj.calc_vtail_lift()
    obj.calc_drag()
    obj.calc_velocity()
    obj.fusealge_sizing()
    obj.motor_sizing()
    obj.wing_sizing()
    obj.tail_sizing()
    obj.vel_setting()
    
    
    
    
    new_mass = obj.mass
    mass_index.append(obj.mass)
    old_mass = mass_index[i-1]
    e = abs((new_mass - old_mass)/new_mass)
    i = i + 1
    x.append(i)
    t.append(i)
    
    wingspan.append(obj.wingspan)
    vel.append(obj.cruise_velocity)
    chord.append(obj.chord_length)
    rang.append(obj.range/1000)
    endurence.append(obj.endurance)
    S.append(obj.chord_length * obj.wingspan)
    stall_speed.append(obj.stall_speed)

plt.subplot(2,1,1)
plt.plot(x,mass_index)
plt.ylabel('Mass (Kg)')
plt.title('Convergance of Values')

plt.subplot(2,1,2)
plt.plot(x,vel)
plt.ylabel('Velocity (m/s)')
plt.xlabel('# of Iterations')
plt.show()

plt.subplot(2,1,1)
plt.plot(x,S)
plt.ylabel('Wing Surface Area (m^2)')

plt.subplot(2,1,2)
plt.plot(t,rang)
plt.ylabel('Range (km)')
plt.xlabel('# of Iterations')
plt.show()

#fuse_equations.fuse_equations(fuse_diam,fuse_length,wing_chord_length,wingspan)