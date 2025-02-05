# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 09:38:38 2025

@author: briggs
"""
import openvsp as vsp
from GA import GA
from Plane_Class import Plane
import matplotlib.pyplot as plt
import numpy as np
from fuse_equations import fuse_equations
from vsp_geom_creator import vsp_geom_creator
from vsp_results_viewer import vsp_results_viewer
import time
from performance_plotter import performance_plotter

priority = "low speed"
#priority = "high speed"

'''Fitness Function Weights'''
mass = 1
l_over_d = 1
velocity = 1
wingspan = 1
endurance = 1
total_range = 1

'''Min/Max sizes'''
min_bat = 1
max_bat = 4
min_wing = 1
max_wing = 3

'''Objective Scores'''
mass_obj = 10 #meassured in kg
ld_obj = 50 #ratio
vel_obj = 20 #m/s
wingspan_obj = 2.75 #meters
end_obj = 2 #hours
range_obj = 200 #km

'''GA TWEAKING'''
q1= 100 #pop
q2= 100 #generations
q3= 0.05 #keepers
q4= 2 #mutation rate

'''Do you want plots? (1), (0)'''
plots = 0
export_to_VSP = 1
export_to_flight_stream = 0
export_to_solidworks = 1

'''Optimization'''
true_finals = []
true_errors = []
for p in range(1,2):
    scores = []
    errors = []
    finals = []
    for i in range(1,25):
        print(f"Set: {str(p)}")
        print(f"Iteration: {str(i)}")
        final, record, objects, final_error = GA(min_wing,max_wing,min_bat,max_bat, mass,l_over_d,velocity,wingspan,endurance,total_range, plots,q1,q2,q3,q4,mass_obj,ld_obj,vel_obj,wingspan_obj,end_obj,range_obj)
        scores.append(final.score)
        errors.append(round(final_error,5))
        finals.append(final)

    true_finals.append(finals[errors.index(round(min(errors),5))])
    true_errors.append(round(min(errors),5))

true_final = true_finals[true_errors.index(round(min(true_errors),5))]

"""Export to OpenVSP"""
if export_to_VSP ==1:
    vsp_geom_creator(true_final)
    time.sleep(5)
    CL,CD,LD,Alpha = vsp_results_viewer()
    performance_plotter(CL,CD,LD,Alpha)
"""Export to FlightStream"""
if export_to_VSP & export_to_flight_stream ==1:
    '''create .igs file'''
    vsp.ExportFile("genetic_algorithm_model.igs", vsp.SET_ALL, vsp.EXPORT_IGES) 
elif export_to_flight_stream ==1:
    print("Biscuits")

"""Export to SolidWorks"""
if export_to_solidworks == 1:
    fuse_equations(final.fuse_diam,final.fuse_length,final.chord_length,final.wingspan,final.wing_pos,final.airfoil,final.airfoil_num,final.motor_num,final.alpha,final.batteries,final.bat)

'''Print data'''
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