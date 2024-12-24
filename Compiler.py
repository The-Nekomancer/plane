# -*- coding: utf-8 -*-

from Plane_Class import Plane
import fuse_equations
# import numpy as np



obj = Plane(payload_mass = 3.5, priority = "Lift")
i = 1
old_mass = obj.mass
mass_index = [obj.mass]
wingspan = [obj.wingspan]
chord = [obj.chord_length]
vel = [obj.cruise_velocity]
e = 1
while e > 0.01:
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
    new_mass = obj.mass
    mass_index.append(obj.mass)
    old_mass = mass_index[i-1]
    e = abs((old_mass - new_mass)/old_mass)
    i = i + 1
    
    wingspan.append(obj.wingspan)
    vel.append(obj.cruise_velocity)
    chord.append(obj.chord_length)
    
# S = chord * wingspan

#fuse_equations.fuse_equations(fuse_diam,fuse_length,wing_chord_length,wingspan)