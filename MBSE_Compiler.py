# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 09:38:38 2025

@author: briggs

PURPOSE: This is the master file that runs all other programs
"""
from GA import GA
from Plane_Class import Plane
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from fuse_equations import fuse_equations
import time
from performance_plotter import performance_plotter
import pickle as pkl

priority = "low speed"
#priority = "high speed"

'''Fitness Function Weights'''
mass = 1
l_over_d = 1 # this might not be used  anymore?
velocity = 10
wingspan = 1 # this might not be used  anymore?
endurance = 1
total_range = 1
#Total range is only used because 'range' is a reseved word in python

'''Min/Max sizes'''
min_bat = 1
max_bat = 2
min_wing = 0.75
max_wing = 0.85
battery_size = 4

'''Objective Scores'''
mass_obj = 1.5 #meassured in kg
ld_obj = 50 #NOT USED but will break GA if removed
vel_obj = 25 #m/s
wingspan_obj = 1.5 #NOT USED but will break GA if removed
end_obj = 1 #hours
range_obj = 25 #km

'''GA TWEAKING'''
q1= 100 #population size
q2= 100 #generations
q3= 0.05 #keepers
q4= 2 #mutation rate

'''Exports (1), (0)'''
GA_plots = False
export_to_VSP = False
export_to_flight_stream = False
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
        final, record, objects, final_error = GA(min_wing,max_wing,min_bat,max_bat, mass,l_over_d,velocity,wingspan,endurance,total_range, GA_plots,q1,q2,q3,q4,mass_obj,ld_obj,vel_obj,wingspan_obj,end_obj,range_obj,battery_size)
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
    CL,CD,LD,Alpha = vsp_results_viewer()
    performance_plotter(CL,CD,LD,Alpha,final)

"""Export to FlightStream"""
if export_to_VSP and export_to_flight_stream == True:
    '''create .igs file'''
    #vsp.ExportFile("genetic_algorithm_model.igs", vsp.SET_ALL, vsp.EXPORT_IGES) 
elif export_to_flight_stream ==True:
    print("Biscuits")

"""Export to SolidWorks"""
if export_to_solidworks == True:
    fuse_equations(true_final)

'''Print data'''
# The following is just an easy readout to confirm the results
print(f"fuselage diameter: {str(final.fuse_diam)}")
print(f"fuselage length: {str(final.fuse_length)}")
print(f"chord length: {str(final.chord_length)}")
print(f"Wingspan: {str(final.wingspan)}")
print(f"Number of Batteries: {str(final.batteries)}")
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