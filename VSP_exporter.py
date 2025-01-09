# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 09:38:38 2025

@author: briggs
"""

import openvsp as vsp
from GA import GA
priority = "low speed"
#priority = "high speed"

'''Fitness Function Weights'''
mass = 4
l_over_d = 4
velocity = 10
wingspan = 3
endurance = 6
total_range = 3

q1= 150 #pop
q2= 250 #generations
q3= 0.05 #keepers
q4= 2 #mutation rate

'''Do you want plots? (1), (0)'''
plots = 1
export_to_VSP = 1
final = GA(priority, mass,l_over_d,velocity,wingspan,endurance,total_range, plots,q1,q2,q3,q4)

if export_to_VSP ==0:
    # Create a new VSP model
    vsp.VSPRenew()

    '''Fuselage'''
    fuseid = vsp.AddGeom( "FUSELAGE", "" )
    xsec_surf = vsp.GetXSecSurf( fuseid, 0 )
    sections = range(1,vsp.GetNumXSec( xsec_surf )-1)
    for x in sections:
        vsp.ChangeXSecShape( xsec_surf, x, vsp.XS_CIRCLE )
        xsec = vsp.GetXSec( xsec_surf, x)
        wid = vsp.GetXSecParm( xsec, "Circle_Diameter" )
        vsp.SetParmVal( wid, final.fuse_diam )
    vsp.SetParmVal( fuseid, "Length", "Design", final.fuse_length )

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
    vsp.SetParmVal( wid, "Span", "XSec_1", final.wingspan )

    '''Airfoil'''
    vsp.SetParmVal( wid, "Camber", "XSecCurve_0", 0.02 )
    vsp.SetParmVal( wid, "CamberLoc", "XSecCurve_0", 0.4 )
    vsp.SetParmVal( wid, "ThickChord", "XSecCurve_0", 0.12 )
    vsp.Update()

    vsp.WriteVSPFile("genetic_alg.vsp3")

'''Print data'''
print("fuselage diameter: "  + str(final.fuse_diam))
print("fuselage length: "  + str(final.fuse_length))
print("chord length: "  + str(final.chord_length))
print("Wingspan: "  + str(final.wingspan))
print("Motor throttle: "  + str(final.throttle))
print("Length of motor array "  + str(len(final.motor)))

print("Velocity: "  + str(final.cruise_velocity))
print("Stall Speed: "  + str(final.stall_speed))
print("Motor: "  + str(final.motor))