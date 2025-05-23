# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 16:57:00 2024

@author: mjb7tf

PURPOSE: This file defines what a plane is, and how a plane can calculate its own charecteristics
"""
import numpy as np
import pandas as pd
# All measurements are in kg, meters, seconds

class Plane:
    air_desnsity = 1.225 #kg per m cubed
    
    '''Airfoils'''
    naca2412 = pd.read_csv('naca2412.csv')
    naca4412 = pd.read_csv('naca4412.csv')
    
    airfoils = ([naca2412,naca4412]) # List of airfoils that the GA chooses from
    airfoil_codes = ["2412", "4412"] # List of airfoil codes that the GA chooses from

    PERC_JOUKOVSKY = pd.read_csv('12PERC JOUKOVSKY.csv')
    A_18_original = pd.read_csv('A-18 original.csv')
    A_18_smoothed = pd.read_csv('A-18 smoothed.csv')
    B_29_TIP = pd.read_csv('B-29 TIP.csv')
    B_29 = pd.read_csv('B-29.csv')
    DAE_11 = pd.read_csv('DAE-11.csv')
    DEFIANT_CANARD = pd.read_csv('DEFIANT CANARD.csv')
    e169 = pd.read_csv('e169.csv')
    EPPLER_1211 = pd.read_csv('EPPLER 1211.csv')
    FAGEANDCOLLINS = pd.read_csv('FAGEANDCOLLINS.csv')
    GIII = pd.read_csv('GIII.csv')
    GM15 = pd.read_csv('GM15.csv')
    GRUMMAN = pd.read_csv('GRUMMAN.csv')
    HUGHES = pd.read_csv('HUGHES.csv')
    ISA = pd.read_csv('ISA.csv')
    JOUKOVSKY = pd.read_csv('JOUKOVSKY.csv')
    K3311 = pd.read_csv('K3311.csv')
    LOCKHEED_C_5 = pd.read_csv('LOCKHEED C-5.csv')
    LOCKHEED_C_141 = pd.read_csv('LOCKHEED C-141.csv')
    OA213 = pd.read_csv('OA213.csv')
    ONERA = pd.read_csv('ONERA.csv')
    PSU = pd.read_csv('PSU.csv')
    
    # airfoils = ([naca2412,naca4412,PERC_JOUKOVSKY,A_18_original,B_29,B_29_TIP,DAE_11,DEFIANT_CANARD,e169,EPPLER_1211,FAGEANDCOLLINS,GIII,GM15,GRUMMAN,HUGHES,ISA,JOUKOVSKY,K3311,LOCKHEED_C_5,LOCKHEED_C_141,OA213,ONERA,PSU])
    #airfoils = ([naca2412,naca4412,A_18_original,B_29,B_29_TIP,DAE_11,DEFIANT_CANARD,e169,EPPLER_1211,FAGEANDCOLLINS,GM15,GRUMMAN,HUGHES,ISA,JOUKOVSKY,K3311,LOCKHEED_C_5,LOCKHEED_C_141,PSU])
    # airfoils = ([naca2412,naca4412,A_18_original,B_29,B_29_TIP,DAE_11,DEFIANT_CANARD,e169,EPPLER_1211,FAGEANDCOLLINS,GIII,GM15,GRUMMAN,HUGHES,ISA,JOUKOVSKY,K3311,LOCKHEED_C_5,LOCKHEED_C_141,OA213,ONERA,PSU])
    
    naca_0012 = {"cl": -0.1034, "alpha": -1, "cd": 0.0064,"cm": -0.0032, "CLmax": 1.2363 }
    naca_2412 = {"cl": 0.8030, "alpha": 5, "cd": 0.0092,"cm": -0.0512, "CLmax": 1.407 }
    # ^These are relics that break the GA if you comment them out, need to eventually remove
    
    '''Motors'''
    v602_kv180 = pd.read_csv('V602_KV180.csv')
    v10l_kv170 = pd.read_csv('V10L_KV170.csv')
    U8II = pd.read_csv('U8II.csv')
    f60pro4 = pd.read_csv('f60pro4.csv')
    # motors = ([v602_kv180, v10l_kv170, f60pro4])
    motors = ([f60pro4])
    '''Batteries'''
    bat_8000_6s = {"cells": 6,"capacity": 8000, "mass": 1.136, "length": 0.165, "width": 0.0635, "height": 0.051}
    bat_2200_4s = {"cells": 4,"capacity": 2200, "mass": 0.1786, "length": 0.1016, "width": 0.04572, "height": 0.04572}
    bat_1350_6s = {"cells": 6,"capacity": 1350, "mass": 0.259, "length": 0.076, "width": 0.034, "height": 0.051}
    batts = ([bat_8000_6s,bat_2200_4s,bat_1350_6s])

    def __init__(self, name = "test plane",
                wingspan = 2.540,
                airfoil = naca2412, 
                airfoil_num = 0,
                payload_mass = 0.286,
                cruise_velocity = 15.24,
                motor = motors[0],
                motors = 1,
                bat = batts[0],
                batteries = 2,
                fuse_diam = 0.11,
                fuse_length = .25,
                payload_skid_width = .1,
                payload_skid_length = .15,
                vtail_chord = 0.04,
                alpha = 5,
                throttle = 3,
                motor_num = 0,
                config = 'VTail',
                taper = 0.4,
                score = 0):
        self.name = name
        self.wingspan = wingspan
        self.chord_length = wingspan/6
        self.airfoil = airfoil
        self.airfoil_num = airfoil_num
        self.payload_mass = payload_mass
        self.cruise_velocity =  cruise_velocity
        self.mass = payload_mass*3
        self.motor  = motor #The actaul motor used
        self.motors = motors #The number of motors used
        self.fuse_diam = fuse_diam
        self.fuse_length = fuse_length
        self.bat = bat
        self.batteries = batteries
        self.payload_skid_width = payload_skid_width
        self.payload_skid_length = payload_skid_length
        self.tail_length = fuse_length + .2
        self.vtail_length = self.tail_length - 0.2
        self.vtail_chord = vtail_chord
        self.max_vel = 14
        self.max_wingspan = 3
        self.min_wingspan = 1
        self.max_chord = self.wingspan/3
        self.min_chord = self.wingspan/12
        self.alpha = alpha
        self.throttle = throttle
        self.motor_num = motor_num
        self.taper = taper
        self.score = score
        
        """
        CALCULATION METHODS
        """
        #########CALCULATION METHODS###########################################
    def calc_mass(self):
        self.bat_skid_mass = self.batteries * self.bat["mass"]
        self.elec_skid_mass = 0.13
        # Surface area calculated is equal to the surface area of a clyinder with one end being a sphere
        self.fuse_surf_area = 2*np.pi*(self.fuse_diam/2) + self.fuse_length + np.pi*(self.fuse_diam/2)**2 + 2*np.pi*(self.fuse_diam/2)**2
        self.fuse_mass = round(self.fuse_surf_area * 0.002 * 250,4)
        self.wing_mass = round(self.wingspan * self.chord_length *0.002 * 550,4)
        self.tail_mass = round(self.tail_length * 0.001 * 100,4)
        self.vtail_mass = round(2 * self.vtail_length * self.vtail_chord * 0.002 * 3000,4)
        motor_mass = Plane.motors[self.motor_num].loc[2, 'mass'] * self.motors
        self.mass = round(self.bat_skid_mass + self.payload_mass + self.fuse_mass + self.wing_mass + self.tail_mass + self.vtail_mass + self.elec_skid_mass + motor_mass,4)
        self.center_of_gravity = round(self.fuse_length * 0.33,2) #<---------- This is shouldn't be calculated this way, must change later
        self.wing_pos = (self.fuse_diam/2) - self.fuse_diam*0.2 #Vertical position relative to fuselage

    def cg_checker(self):
        self.calc_mass()
        '''Front of Plane'''
        fuse_moment = self.fuse_mass*(self.fuse_length-self.chord_length)/2 
        payload_moment = self.payload_mass * (self.fuse_length-self.chord_length)
        forward_moment = fuse_moment + payload_moment
        '''Motor'''
        if self.motors % 2 == 1:
            motor_moment = 0.034*self.tail_length
        else:
            motor_moment = 0
        '''Rear of Plane'''
        rudder_moment = self.vtail_mass * self.tail_length
        rear_moment = motor_moment + rudder_moment
        '''Battery Moments'''
        if rear_moment > forward_moment*1.1:
            if (rear_moment < (forward_moment + self.bat_skid_mass*((self.fuse_length-self.chord_length)/2 ))*1.1):
                self.cg_check = True
            else:
                self.cg_check = False
                self.cg_correction = 'tail heavy'
        else:
            self.cg_check = False
            self.cg_correction = 'nose heavy'
        
    def calc_endurance(self):
        amps = Plane.motors[self.motor_num].loc[(self.throttle), 'Current (A)'] * self.motors
        self.capacity = self.bat["capacity"] * self.batteries / 1000
        self.endurance = self.capacity/amps
        #defined in hours
        
    def calc_range(self):
        self.calc_endurance()
        self.calc_velocity()
        self.range = self.endurance * self.cruise_velocity * 60**2/1000 # km
    
    def calc_lift(self):
        self.CL = Plane.airfoils[self.airfoil_num].loc[4*self.alpha, 'CL'] # airfoil data is always deliniated in 0.25 degrees of alpha so it's multiplied by 4 for loacation of data
        self.lift = (Plane.air_desnsity * 0.5 * (self.cruise_velocity**2) * self.CL * self.wingspan * self.chord_length)/9.81 # Lift is in kg because it's always compared to mass
        # air density in kg/m3         (m/s)                     no unit       m                mm  convert to Kg
        self.moment = (Plane.air_desnsity * 0.5 * (self.cruise_velocity**2) * Plane.airfoils[self.airfoil_num].loc[4*self.alpha, 'CM'] * self.wingspan * self.chord_length) #<--- HAS NEVER BEEN ACCURATE
    
    def calc_vtail_lift(self):
        CL = Plane.naca_0012["cl"]
        self.vtail_lift = (np.sqrt(2)/2)*(Plane.air_desnsity * 0.5 * (self.cruise_velocity**2) * CL * self.vtail_length * self.vtail_chord)
        self.vtail_moment = self.vtail_lift * self.tail_length
    
    def calc_drag(self):
        self.CD = Plane.airfoils[self.airfoil_num].loc[1+4*self.alpha, 'CD']
        self.drag = (Plane.air_desnsity * 0.5 * (self.cruise_velocity**2) * (self.CD + 0.2) * self.wingspan * self.chord_length)/9.81
    
    def calc_velocity(self):
        # The velocity is calculated by balencing the force produced by the motor(s) and balencing 
        # that with the force created by drag, when equal, you have trimmed and level flight
        Plane.calc_mass(self)
        self.stall_speed = np.sqrt(2*9.81*self.mass/(Plane.air_desnsity * Plane.airfoils[self.airfoil_num].loc[66, 'CL'] * self.wingspan * self.chord_length))
        self.calc_drag()
        thrust = Plane.motors[self.motor_num].at[(self.throttle), 'Thrust (kg)'] * self.motors
        while self.drag < thrust: # if thrust from the motor is greater drag at velocity 'x'
            self.cruise_velocity = self.cruise_velocity * 1.001
            self.calc_drag()
