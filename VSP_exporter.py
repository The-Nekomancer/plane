# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 09:38:38 2025

@author: brigg
"""

import openvsp as vsp
from GA import GA

final = GA()
# Create a new VSP model
vsp.VSPRenew()

# Add a fuselage
fuse_id = vsp.AddGeom("FUSELAGE")
vsp.SetParmVal(fuse_id, "Length", "Design", final.fuse_length)
vsp.SetParmVal(fuse_id, "Diameter", "Design", final.fuse_diam)

# Add a wing
wing_id = vsp.AddGeom("WING")
vsp.SetParmVal(wing_id, "Span", "Design", final.wingspan)
vsp.SetParmVal(wing_id, "Root_Chord", "Design", final.chord_length)
vsp.SetParmVal(wing_id, "Tip_Chord", "Design", final.chord_length)

# Write the VSP file
vsp.WriteVSPFile("genetic_alg.vsp3")

print(final.lift)
print(final.mass)
print(final.cruise_velocity)
print(final.wingspan)