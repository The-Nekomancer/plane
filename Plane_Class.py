# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 16:57:00 2024

@author: mjb7tf
"""
import numpy as np
# All measurements are in inch, pounds, seconds

class Plane:
    air_desnsity = 1.225 #kg per m cubed
    
    airfoils = (["naca_0012", "naca_2412"])
    naca_0012 = {"cl": 0.8892, "alpha": 8.5, "cd": 0.01167, "L/D": 40 }
    naca_2412 = {"cl": 1.0581, "alpha": 7, "cd": 0.02483, "L/D": 28 }
    
    v602_kv180_50p = {"mass": 0.345, "thrust": 3.527, "amps": 8.77, "efficiency": 8.45, "prop length": 22}
    v602_kv180_70p = {"mass": 0.345, "thrust": 5.737, "amps": 18.02, "efficiency": 6.73, "prop length": 22}
    
    V10L_KV170_50p = {"mass": 0.445, "thrust": 10.802, "amps": 37.81, "efficiency": 6.07, "prop length": 30}
    V10L_KV170_70p = {"mass": 0.445, "thrust": 18.57, "amps": 82.55, "efficiency": 4.88, "prop length": 30}
    
    bat_8000_6s = {"capacity": 8000, "mass": 1.136, "length": 0.165, "width": 0.0635, "height": 0.051}
    
    priority = {"Lift", "High Speed", "Range", "Low Speed"}
    def __init__(self, name = "test plane",
                 wingspan = 2.540, 
                 chord_length = .127,
                 airfoil = naca_2412,
                 payload_mass = 4,
                 cruise_velocity = 15.24,
                 priority = "Lift",
                 motor = v602_kv180_50p,
                 fuse_diam = .254,
                 fuse_length = .635,
                 bat = bat_8000_6s,
                 batteries = 2,
                 payload_skid_width = .205):
        self.name = name
        self.wingspan = wingspan
        self.chord_length = chord_length
        self.airfoil = airfoil
        self.payload_mass = payload_mass
        self.cruise_velocity =  cruise_velocity
        self.weight = payload_mass*3
        self.priority = priority
        self.motor  = motor
        self.fuse_diam = fuse_diam
        self.fuse_length = fuse_length
        self.bat = bat
        self.batteries = batteries
        self.payload_skid_width = payload_skid_width
        self.tail_length = fuse_length + .2
        self.vtail_length = self.tail_length - 0.2
        
        
        """
        CALCULATION METHODS
        """
        #########CALCULATION METHODS###########################################
    def calc_fuse_size(self):    
        self.fuse_diam = 2 * self.payload_skid_width / np.sqrt(2)
        
    def calc_mass(self):
        bat_mass = self.batteries * self.bat["mass"]
        # Surface area calculated is equal to the surface area of a clyinder with one end being a sphere
        self.fuse_surf_area = 2*np.pi*(self.fuse_diam/2) + self.fuse_length + np.pi*(self.fuse_diam/2)**2 + 2*np.pi*(self.fuse_diam/2)**2
        self.fuse_mass = self.fuse_surf_area * 0.2
        self.wing_mass = self.wingspan * self.chord_length * 2 *.2
        self.tail_mass = 0.004 * 3 * self.tail_length * .2
        self.vtail_mass = 2 * self.vtail_length * 0.2
        self.mass = bat_mass + self.payload_mass + self.motor["mass"] + self.fuse_mass + self.wing_mass + self.tail_mass + self.vtail_mass
        
    def calc_endurance(self):
        self.capacity = self.bat["capacity"] * self.batteries / 1000
        self.endurance = self.capacity/self.motor["amps"]
        #defined in hours
        
    def calc_range(self):
        self.calc_endurance()
        self.calc_velocity()
        self.range = self.endurance * self.cruise_velocity * 60**2
    
    def calc_lift(self):
        self.CL = self.airfoil["cl"]
        self.lift = (Plane.air_desnsity * 0.5 * (self.cruise_velocity**2) * self.CL * self.wingspan * self.chord_length)/9.81
        # air density in kg/m3         (m/s)                     no unit       m                mm  convert to Kg
    
    def calc_drag(self):
        self.CD = self.airfoil["cd"]
        self.drag = (Plane.air_desnsity * 0.5 * (self.cruise_velocity**2) * (self.CD + 0.2) * self.wingspan * self.chord_length)/9.81
    
    def calc_velocity(self):
        self.calc_drag()
        while self.drag < self.motor["thrust"]: # if thrust from the motor is greater drag at velocity 'x'
            self.cruise_velocity = self.cruise_velocity * 1.01
            self.calc_drag()

        while self.motor["thrust"] < self.drag:
            self.cruise_velocity = self.cruise_velocity * 0.99
            self.calc_drag()
            
        """
        SYSTEM DESIGN METHODS
        """
        #################SYSTEM DESIGN METHODS#################################
            
   
    
   
    
   
    
   
    # def decrease_velocity(self):
    #     pass

    #     return self.cruise_velocity
            
    # def change_lift(self):
    #     self.calc_lift()
    #     while self.weight > self.lift:
    #         self.wingspan = self.wingspan * 1.01
    #         self.chord_length = self.chord_length * 1.01
    #         self.calc_lift()
    #     self.wingspan = np.ceil(self.wingspan)
    #     self.chord_length = np.ceil(self.chord_length)
    # def change_drag(self):
    #     L = self.calc_lift()
    #     while self.weight < L:
    #         self.wingspan = self.wingspan * 0.99
    #         self.chord_length = self.chord_length * 0.99
    #         L = self.calc_lift()
    #     self.wingspan = np.ceil(self.wingspan)
    #     self.chord_length = np.ceil(self.chord_length)
    
    # def determine_wing_properties(self):
    #     print("weight: " + str(self.weight))
    #     if self.priority == "Lift":
    #         self.change_lift()
    #         self.cal_max_velocity()
    #         self.change_drag()
            
    #     if self.priority == "High Speed":
    #         self.cal_max_velocity()
            
    #     if self.priority == "Range":
    #         self.change_drag()
            