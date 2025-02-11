# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 11:43:04 2025

@author: mjb7tf
"""
import pickle as pkl
from vsp_results_viewer import vsp_results_viewer
from performance_plotter import performance_plotter
from Plane_Class import Plane
import numpy as np


with open("final_pickle.pkl", "rb") as f:
    final = pkl.load(f)

CL,CD,LD,Alpha = vsp_results_viewer()
performance_plotter(CL,CD,LD,Alpha,final)

print(f"fuselage diameter: {str(final.fuse_diam)}")
print(f"fuselage length: {str(final.fuse_length)}")
print(f"chord length: {str(final.chord_length)}")
print(f"Wingspan: {str(final.wingspan)}")
print("Motor throttle: "  + str(Plane.motors[final.motor_num].at[(final.throttle), 'Throttle (%)']))
print(f"Motor: {str(final.motor_num)}")
print(f"Velocity: {str(final.cruise_velocity)}")
print(f"Stall Speed: {str(final.stall_speed)}")
print(f"final score: {str(final.score)}")
print(f"final lift: {str(final.lift)}")
print(f"final mass: {str(final.mass)}")
print(f"final alpha: {str(final.alpha)}")
print(f"final endurance: {str(final.endurance)}")
print(f"final range: {str(final.range)}")
print("final current draw: "+ str(Plane.motors[final.motor_num].at[(final.throttle), 'Current (A)']))
print(f"airfoil: {str(final.airfoil_num)}")