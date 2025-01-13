# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 09:38:38 2025

@author: briggs
"""
import openvsp as vsp
from GA import GA
from Plane_Class import Plane
priority = "low speed"
#priority = "high speed"

'''Fitness Function Weights'''
mass = 1
l_over_d = 1
velocity = 1
wingspan = 1
endurance = 1
total_range = 1

'''Objective Scores'''
mass_obj = 10 #meassured in kg
ld_obj = 10 #ratio
vel_obj = 20 #m/s
wingspan_obj = 3 #meters
end_obj = 2 #hours
range_obj = 200 #km

q1= 100 #pop
q2= 100 #generations
q3= 0.05 #keepers
q4= 2 #mutation rate

'''Do you want plots? (1), (0)'''
plots = 0
export_to_VSP = 1
final, record, objects = GA(priority, mass,l_over_d,velocity,wingspan,endurance,total_range, plots,q1,q2,q3,q4,mass_obj,ld_obj,vel_obj,wingspan_obj,end_obj,range_obj)

if export_to_VSP ==1:
    # Create a new VSP model
    vsp.VSPRenew()

    '''Fuselage'''
    total_length = final.fuse_length + 1
    xsec_percent = final.fuse_length/total_length
    fuseid = vsp.AddGeom( "FUSELAGE", "" )
    xsec_surf = vsp.GetXSecSurf( fuseid, 0 )
    sections = range(1,vsp.GetNumXSec( xsec_surf )-1)
    for x in sections:
        vsp.ChangeXSecShape( xsec_surf, x, vsp.XS_CIRCLE )
        xsec = vsp.GetXSec( xsec_surf, x)
        wid = vsp.GetXSecParm( xsec, "Circle_Diameter" )
        vsp.SetParmVal( wid, final.fuse_diam )
    vsp.SetParmVal( fuseid, "Length", "Design", total_length )
    vsp.InsertXSec( fuseid, 1, vsp.XS_CIRCLE )
    vsp.SetParmVal( fuseid, "XLocPercent","XSec_2", xsec_percent)
    vsp.SetParmVal( fuseid, "XLocPercent","XSec_1", 0.1)
    vsp.SetParmVal( fuseid, "Circle_Diameter","XSecCurve_3", 0.1)
    
    vsp.SetParmVal( fuseid, "ZLocPercent","XSec_3", -0.03)
    vsp.SetParmVal( fuseid, "ZLocPercent","XSec_4", -0.03)
    vsp.SetParmVal( fuseid, "ZLocPercent","XSec_5", -0.03)
    vsp.SetParmVal( fuseid, "Circle_Diameter","XSecCurve_4", 0.1)
    vsp.SetParmVal( fuseid, "XLocPercent","XSec_4", 0.95)

    '''Wing'''
    wid = vsp.AddGeom( "WING", "" )
    vsp.InsertXSec( wid, 1, vsp.XS_FOUR_SERIES )
    vsp.SetParmVal(wid, "X_Rel_Location", "XForm", final.fuse_length/2 - final.chord_length/2)
    vsp.SetParmVal(wid, "Z_Rel_Location", "XForm", final.fuse_diam/2)
    vsp.CutXSec( wid, 1 )
    vsp.SetDriverGroup( wid, 1, vsp.AREA_WSECT_DRIVER, vsp.ROOTC_WSECT_DRIVER, vsp.TIPC_WSECT_DRIVER )
    vsp.SetParmVal( wid, "Root_Chord", "XSec_1", final.chord_length )
    vsp.SetParmVal( wid, "Tip_Chord", "XSec_1", final.chord_length )
    vsp.SetParmVal( wid, "Sweep", "XSec_1", 0)
    vsp.SetParmVal( wid, "TotalSpan", "WingGeom", final.wingspan )

    '''Airfoil'''
    vsp.SetParmVal( wid, "Camber", "XSecCurve_0", 0.02 )
    vsp.SetParmVal( wid, "CamberLoc", "XSecCurve_0", 0.4 )
    vsp.SetParmVal( wid, "ThickChord", "XSecCurve_0", 0.12 )
    vsp.Update()

    '''Horizontal Stab'''
    hs = vsp.AddGeom( "WING", "" )
    vsp.InsertXSec( hs, 1, vsp.XS_FOUR_SERIES )
    vsp.SetParmVal(hs, "X_Rel_Location", "XForm", total_length*0.85)
    vsp.SetParmVal(hs, "Z_Rel_Location", "XForm", -final.fuse_diam/6)
    vsp.CutXSec( hs, 1 )
    vsp.SetDriverGroup( hs, 1, vsp.AREA_WSECT_DRIVER, vsp.ROOTC_WSECT_DRIVER, vsp.TIPC_WSECT_DRIVER )
    vsp.SetParmVal( hs, "Root_Chord", "XSec_1", 0.1)
    vsp.SetParmVal( hs, "Tip_Chord", "XSec_1", 0.1 )
    vsp.SetParmVal( hs, "Sweep", "XSec_1", 0)
    vsp.SetParmVal( hs, "TotalSpan", "WingGeom", final.wingspan/2 )
    vsp.SetParmVal( hs, "Dihedral", "XSec_1", 45 )
    
    vsp.SetParmVal( hs, "Camber", "XSecCurve_0", 0.0 )
    vsp.SetParmVal( hs, "CamberLoc", "XSecCurve_0", 0.0 )
    vsp.SetParmVal( hs, "ThickChord", "XSecCurve_0", 0.12 )
    
    prop = vsp.AddGeom( "PROP", "" )
    vsp.SetParmVal(prop, "X_Rel_Location", "XForm", total_length)
    vsp.SetParmVal(prop, "Z_Rel_Location", "XForm", -final.fuse_diam/6)
    vsp.SetParmVal(prop, "Diameter", "Design", 0.3 )
    vsp.Update()

    vsp.WriteVSPFile("genetic_alg.vsp3")

'''Print data'''
print("fuselage diameter: "  + str(final.fuse_diam))
print("fuselage length: "  + str(final.fuse_length))
print("chord length: "  + str(final.chord_length))
print("Wingspan: "  + str(final.wingspan))
print("Motor throttle: "  + str(Plane.motors[final.motor_num].at[(final.throttle), 'Throttle (%)']))
print("Motor: "  + str(final.motor_num))
print("Velocity: "  + str(final.cruise_velocity))
print("Stall Speed: "  + str(final.stall_speed))
print("final score: " + str(final.score))
print("final lift: " + str(final.lift))
print("final mass: " + str(final.mass))
print("final alpha: " + str(final.alpha))
print("final endurance: " + str(final.endurance))
print("final range: " + str(final.range))
print("final current draw: "+ str(Plane.motors[final.motor_num].at[(final.throttle), 'Current (A)']))