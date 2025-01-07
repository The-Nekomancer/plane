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
vsp.SetParmVal(fuse_id, "Length", "Geom", final.fuse_length)
vsp.SetParmVal(fuse_id, "Diameter", "Geom", final.fuse_diam)

# Add a wing
wing_id = vsp.AddGeom("WING")
vsp.SetParmVal(wing_id, "Span", "Xsec", final.wingspan)
vsp.SetParmVal(wing_id, "Root_Chord", "Xsec", final.chord_length)
vsp.SetParmVal(wing_id, "Tip_Chord", "Xsec", final.chord_length)

# Write the VSP file
vsp.WriteVSPFile("genetic_alg.vsp3")

print("fuselage diameter: "  + str(final.fuse_diam))
print("fuselage length: "  + str(final.fuse_length))
print("chord length: "  + str(final.chord_length))
print("Wingspan: "  + str(final.wingspan))