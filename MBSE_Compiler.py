# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 09:38:38 2025

@author: briggs

PURPOSE: This is the master file that runs all other programs
"""
from GA import GA
from Plane_Class import Plane
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import pandas as pd
import numpy as np
from stl import mesh
from fuse_equations import fuse_equations
import time
from performance_plotter import performance_plotter
import pickle as pkl

'''TO DO LIST
- battery selection
- Export to SolidWorks automatically
- Taper ratio (elliptical wing)
- Variable aspect ratio
- VTOL

'''

'''Fitness Function Weights'''
velocity = 2
stall = 3
endurance = 2
total_range = 1

'''sizing'''
max_bat = 4
max_wing = 3 # meters
max_motors = 3
battery_size = 1
payload_weight = 2 # kg

'''Objective Scores'''
vel_obj = 12 #m/s
stall_obj = 8 #m/s
end_obj = 0.8 #hours
range_obj = 50 #km

'''Exports'''
GA_plots = False
export_to_VSP = True
visualization = True
export_to_solidworks = True

'''Optimization'''
# The 'i' for loop runs the whole GA multiple times and picks the best result of all trials, 25 is optimal
# the 'p' for loop is to confirm the results of the 'i' loop, is not needed other than testing, set to 2
true_finals = []
true_errors = []
for p in range(1,2):
    scores = []
    errors = []
    finals = []
    for i in range(1,2):
        print(f"Set: {str(p)}")
        print(f"Iteration: {str(i)}")
        final, record, objects, final_error = GA(payload_weight,max_wing,max_bat,max_motors,velocity,endurance,total_range,stall,GA_plots,vel_obj,end_obj,range_obj,stall_obj,battery_size)
        scores.append(final.score) #These are really only for easy comparison when tweaking GA parameters
        errors.append(round(final_error,5)) #^
        finals.append(final)                #^

    true_finals.append(finals[errors.index(round(min(errors),5))])
    true_errors.append(round(min(errors),5))
true_final = true_finals[true_errors.index(round(min(true_errors),5))]
#The true_final is the very best instance ever created by GA that gets passed to user

'''Pickle the Final result for testing purposes'''
with open("final_pickle.pkl","wb") as f:
    pkl.dump(true_final,f)

"""Export to OpenVSP"""
if export_to_VSP == True:
    import openvsp as vsp
    from vsp_geom_creator import vsp_geom_creator
    from vsp_results_viewer import vsp_results_viewer
    vsp_geom_creator(true_final)
    time.sleep(5)
    #CL,CD,LD,Alpha = vsp_results_viewer()
    #performance_plotter(CL,CD,LD,Alpha,final)

"""Visualization"""
if export_to_VSP and visualization == True:
    '''create .igs file'''
    vsp.ExportFile("genetic_algorithm_model.stl", vsp.SET_ALL, vsp.EXPORT_STL) 
elif visualization ==True:
    print("Biscuits")

"""Export to SolidWorks"""
if export_to_solidworks == True:
    fuse_equations(true_final)

'''Print data'''
# The following is just an easy readout to confirm the results
print(f"Fuselage diameter: {str(final.fuse_diam)}" + " m")
print(f"Fuselage length: {str(final.fuse_length)}"+ " m")
print(f"Chord length: {str(final.chord_length)}"+ " m")
print(f"Wingspan: {str(final.wingspan)}"+ " m")
print(f"Number of Batteries: {str(final.batteries)}")
print("Motor throttle: "  + str(Plane.motors[final.motor_num].at[(final.throttle), 'Throttle'])+ " %")
print(f"Motor: {str(final.motor_num)}")
print(f"Number of motors: {str(final.motors)}")
print(f"Velocity: {str(round(final.cruise_velocity,3))}"+ " m/s")
print(f"Stall Speed: {str(round(final.stall_speed,2))}"+ " m/s")
print(f"Score: {str(round(final.score,2))}")
print(f"Lift: {str(round(final.lift,2))}"+ " kg")
print(f"Mass: {str(round(final.mass,2))}"+ " kg")
print(f"Alpha: {str(final.alpha)}"+ " degrees")
print(f"Endurance: {str(round(final.endurance,2))}"+ " hours")
print(f"Range: {str(round(final.range,2))}"+ " km")
print("Current draw: "+ str(Plane.motors[final.motor_num].at[(final.throttle), 'Current (A)']*final.motors)+ " A")
print(f"airfoil: {str(final.airfoil_num)}")
# print(f"final mass: {str(final.mass)}")
print(f"Fuselage mass: {str(final.fuse_mass)}"+ " kg")
print(f"Wing mass: {str(final.wing_mass)}"+ " kg")
print(f"Tail mass: {str(final.tail_mass)}"+ " kg")
print(f"Tail length: {str(final.tail_length)}"+ " m")
# print(f"vtail length: {str(final.vtail_length)}")
print(f"Ruddervator mass: {str(final.vtail_mass)}"+ " kg")
print(f"Payload mass: {str(final.payload_mass)}"+ " kg")

# Create a new plot
figure = plt.figure()
axes = figure.add_subplot(projection='3d')

# Load the STL files and add the vectors to the plot
your_mesh = mesh.Mesh.from_file('genetic_algorithm_model.stl')
axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))

# Auto scale to the mesh size
scale = your_mesh.points.flatten()
axes.auto_scale_xyz(scale, scale, scale)

# Show the plot to the screen
plt.show()