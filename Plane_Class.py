# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 16:57:00 2024

@author: mjb7tf
"""
import numpy as np
import math

# All measurements are in inch, pounds, seconds

class Plane:
    air_desnsity = 0.00004335 #lbs per inch cubed
    airfoils = (["naca_0012", "naca_2412"])
    naca_0012 = {"cl": 0.8892, "alpha": 8.5, "cd": 0.01167, "L/D": 40 }
    naca_2412 = {"cl": 1.0581, "alpha": 7, "cd": 0.02483, "L/D": 28 }
    priority = {"Lift", "Speed", "Range"}
    def __init__(self, name = "test plane",
                 wingspan = 84, 
                 chord_length = 12.0,
                 airfoil = naca_2412,
                 payload = 10.0,
                 cruise_velocity = 540,
                 priority = "Lift",
                 motor = 10.0):
        self.name = name
        self.wingspan = wingspan
        self.chord_length = chord_length
        self.airfoil = airfoil
        self.payload = payload
        self.cruise_velocity =  cruise_velocity
        self.weight = payload*3
        self.priority = priority
        self.motor  = motor
        
    def calc_lift(self):
        self.CL = self.airfoil["cl"]
        L = (Plane.air_desnsity * 0.5 * (self.cruise_velocity**2) * self.CL * self.wingspan * self.chord_length)/144
        # air density in lb/in3         (in/s)                     no unit       in                in   convert to lbf
        return L
    
    def calc_drag(self):
        self.CD = self.airfoil["cd"]
        D = (Plane.air_desnsity * 0.5 * (self.cruise_velocity**2) * self.CD * self.wingspan * self.chord_length)/144
        return D
    
    def determine_wing_properties(self):
        L = self.calc_lift()
        if self.priority == "Lift":
            while self.weight > L:
                self.wingspan = self.wingspan * 1.01
                self.chord_length = self.chord_length * 1.01
                L = self.calc_lift()
                self.wingspan = np.ceil(self.wingspan)
                self.chord_length = np.ceil(self.chord_length)
         
        if self.priority == "Speed":
            while self.weight > L:
                self.cruise_velocity = self.cruise_velocity*1.01
                L = self.calc_lift()
                self.cruise_velocity = np.ceil(self.cruise_velocity)
             
        if self.priority == "Range":
            self.airfoil = self.naca_0012
            L = self.calc_lift()
            while self.weight > L:
                self.payload = self.payload * 0.99
                self.weight = self.payload*3
                 
        return L

    def calc_vel(self):
        D = self.calc_drag()
        while D < self.motor:
            self.cruise_velocity = self.cruise_velocity * 1.01
            D = self.calc_drag()

        while self.motor < D:
            self.cruise_velocity = self.cruise_velocity * 0.99
            D = self.calc_drag()

        return self.cruise_velocity