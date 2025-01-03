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
    naca_0012 = {"cl": -0.1034, "alpha": -1, "cd": 0.0064,"cm": -0.0032, "CLmax": 1.2363 }
    naca_2412 = {"cl": 0.8030, "alpha": 5, "cd": 0.0092,"cm": -0.0512, "CLmax": 1.407 }
    
    v602_kv180_50p = {"name": "v602_kv180_50p", "mass": 0.345, "thrust": 3.527, "amps": 8.77, "efficiency": 8.45, "prop length": 22}
    v602_kv180_70p = {"name": "v602_kv180_70p", "mass": 0.345, "thrust": 5.737, "amps": 18.02, "efficiency": 6.73, "prop length": 22}
    
    V10L_KV170_50p = {"name": "V10L_KV170_50p", "mass": 0.445, "thrust": 10.802, "amps": 37.81, "efficiency": 6.07, "prop length": 30}
    V10L_KV170_70p = {"name": "V10L_KV170_70p", "mass": 0.445, "thrust": 18.57, "amps": 82.55, "efficiency": 4.88, "prop length": 30}
    
    motors = ([v602_kv180_50p, v602_kv180_70p, V10L_KV170_50p, V10L_KV170_70p])
    bat_8000_6s = {"capacity": 8000, "mass": 1.136, "length": 0.165, "width": 0.0635, "height": 0.051}
    
    # priority = {"Low Speed", "High Speed", "Range", "Lift", "Endurance"}
    priority = [1,2,3,4,5]
    def __init__(self, name = "test plane",
                 wingspan = 2.540,
                 airfoil = naca_2412,
                 payload_mass = 4,
                 cruise_velocity = 15.24,
                 priority = priority[0],
                 motor = motors[0],
                 fuse_diam = .254,
                 fuse_length = .635,
                 bat = bat_8000_6s,
                 batteries = 2,
                 payload_skid_width = .1,
                 payload_skid_length = .15,
                 vtail_chord = 0.04):
        self.name = name
        self.wingspan = wingspan
        self.chord_length = wingspan/9
        self.airfoil = airfoil
        self.payload_mass = payload_mass
        self.cruise_velocity =  cruise_velocity
        self.mass = payload_mass*3
        self.priority = priority
        self.motor  = motor
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
        self.max_chord = self.wingspan/12
        self.min_chord = self.wingspan/3
        
        """
        CALCULATION METHODS
        """
        #########CALCULATION METHODS###########################################
    def calc_mass(self):
        bat_skid_mass = self.batteries * self.bat["mass"]
        elec_skid_mass = 0.3
        # Surface area calculated is equal to the surface area of a clyinder with one end being a sphere
        self.fuse_surf_area = 2*np.pi*(self.fuse_diam/2) + self.fuse_length + np.pi*(self.fuse_diam/2)**2 + 2*np.pi*(self.fuse_diam/2)**2
        self.fuse_mass = self.fuse_surf_area * 0.2
        self.wing_mass = self.wingspan * self.chord_length * 2 *.2
        self.tail_mass = 0.004 * 3 * self.tail_length * .2
        self.vtail_mass = 2 * self.vtail_length * 0.2
        self.mass = bat_skid_mass + self.payload_mass + self.fuse_mass + self.wing_mass + self.tail_mass + self.vtail_mass + elec_skid_mass
        
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
        self.moment = (Plane.air_desnsity * 0.5 * (self.cruise_velocity**2) * self.airfoil["cm"] * self.wingspan * self.chord_length)
    
    def calc_vtail_lift(self):
        CL = Plane.naca_0012["cl"]
        self.vtail_lift = (np.sqrt(2)/2)*(Plane.air_desnsity * 0.5 * (self.cruise_velocity**2) * CL * self.vtail_length * self.vtail_chord)
        self.vtail_moment = self.vtail_lift * self.tail_length
    
    def calc_drag(self):
        self.CD = self.airfoil["cd"]
        self.drag = (Plane.air_desnsity * 0.5 * (self.cruise_velocity**2) * (self.CD + 0.2) * self.wingspan * self.chord_length)/9.81
    
    def calc_velocity(self):
        Plane.calc_mass(self)
        self.stall_speed = np.sqrt(2*9.81*self.mass/(Plane.air_desnsity * self.airfoil["CLmax"] * self.wingspan * self.chord_length))
        self.calc_drag()
        while self.drag < self.motor["thrust"]: # if thrust from the motor is greater drag at velocity 'x'
            self.cruise_velocity = self.cruise_velocity * 1.001
            self.calc_drag()
                
        """
        SYSTEM DESIGN METHODS
        """
        #################SYSTEM DESIGN METHODS#################################
    def fusealge_sizing(self):
        if (self.batteries % 2) == 0:
            self.bat_skid_width = self.bat["width"] * 2
        else:
            self.bat_skid_width = self.bat["width"]
        if self.bat_skid_width > self.payload_skid_width:
            fuse_width = self.bat_skid_width
        else: 
            fuse_width = self.payload_skid_width
        self.fuse_diam = 2 * fuse_width / np.sqrt(2)
        if self.batteries >2:
            self.bat_skid_length = self.bat["length"] * 2
        else:
            self.bat_skid_length = self.bat["length"]
        ###OUTPUTS###
        self.fuse_diam = 2 * fuse_width / np.sqrt(2)
        self.fuse_length = self.payload_skid_length + self.bat_skid_length
        self.nose_cone_length = self.fuse_length * 0.25
        Plane.calc_mass(self)
        
    def motor_sizing(self):
        Plane.calc_drag(self)
        Plane.calc_velocity(self)
        if self.stall_speed > self.cruise_velocity:
            motor_index = Plane.motors.index((self.motor))
            self.motor = Plane.motors[motor_index + 1]
        
    def wing_sizing(self):
        Plane.calc_lift(self)
        Plane.calc_mass(self)
        Plane.calc_velocity(self)
        self.weight = self.mass * 1 #lift is calculated in kg
        if self.priority == 2:
            while self.weight < self.lift:
                if self.wingspan < self.min_wingspan:
                    break
                else:
                    self.wingspan = self.wingspan * 0.999
                    self.chord_length = self.chord_length * 0.999
                    Plane.calc_lift(self)
        if self.priority == 1:
            while self.cruise_velocity > self.max_vel:
                if self.max_wingspan < self.wingspan:
                    break
                else:
                    self.wingspan = self.wingspan * 1.001
                    self.chord_length = self.chord_length * 1.001
                    Plane.calc_lift(self)
                    Plane.calc_velocity(self)
    
    def tail_sizing(self):
        Plane.calc_lift(self)
        Plane.calc_vtail_lift(self)
        while self.vtail_moment > self.moment:
            self.tail_length = self.tail_length * 1.01
            Plane.calc_vtail_lift(self)
            
    def vel_setting(self):
        if self.priority == 1:
            while self.mass < self.lift:
                self.cruise_velocity = self.cruise_velocity * 0.99
                Plane.calc_lift(self)
                