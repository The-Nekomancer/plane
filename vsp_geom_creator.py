import openvsp as vsp
from vsp_sim import vsp_sim
from Plane_Class import Plane

#Fix hardocded values
def parse_naca_airfoil(code):
    if len(code) != 4 or not code.isdigit():
        raise ValueError(f"Invalid NACA code: {code}")
    m = int(code[0])/100.0 # 2 -> 0.02
    p = int(code[1])/10.0 # 4 -> 0.4
    t = int(code[2:4])/100.0 # 12 -> 0.12
    return m, p, t

# Function to create the geometry in VSP
def vsp_geom_creator(final):
    # Create a new VSP model
    vsp.VSPRenew()

    '''Fuselage'''
    total_length = final.fuse_length + (final.wingspan*0.33)
    xsec_percent = final.fuse_length/total_length
    fuseid = vsp.AddGeom( "FUSELAGE", "" )
    xsec_surf = vsp.GetXSecSurf( fuseid, 0 )
    sections = range(1,vsp.GetNumXSec( xsec_surf )-1)
    tail_diam = final.fuse_diam/2
    for x in sections:
        vsp.ChangeXSecShape( xsec_surf, x, vsp.XS_CIRCLE )
        xsec = vsp.GetXSec( xsec_surf, x)
        wid = vsp.GetXSecParm( xsec, "Circle_Diameter" )
        vsp.SetParmVal( wid, final.fuse_diam )
    vsp.SetParmVal( fuseid, "Length", "Design", total_length )
    vsp.InsertXSec( fuseid, 1, vsp.XS_CIRCLE )
    vsp.SetParmVal( fuseid, "XLocPercent","XSec_2", xsec_percent)
    vsp.SetParmVal( fuseid, "XLocPercent","XSec_1", 0.1)
    vsp.SetParmVal( fuseid, "Circle_Diameter","XSecCurve_3", tail_diam)

    vsp.SetParmVal( fuseid, "ZLocPercent","XSec_3", -0.02)
    vsp.SetParmVal( fuseid, "ZLocPercent","XSec_4", -0.02)
    vsp.SetParmVal( fuseid, "ZLocPercent","XSec_5", -0.02)
    vsp.SetParmVal( fuseid, "Circle_Diameter","XSecCurve_4", tail_diam)
    vsp.SetParmVal( fuseid, "XLocPercent","XSec_4", 0.95)

    '''Wing'''
    wid = vsp.AddGeom( "WING", "" )
    vsp.InsertXSec( wid, 1, vsp.XS_FOUR_SERIES )
    vsp.SetParmVal(wid, "X_Rel_Location", "XForm", final.fuse_length - final.chord_length)
    vsp.SetParmVal(wid, "Z_Rel_Location", "XForm", final.fuse_diam/2)
    vsp.CutXSec( wid, 1 )
    vsp.SetDriverGroup( wid, 1, vsp.AREA_WSECT_DRIVER, vsp.ROOTC_WSECT_DRIVER, vsp.TIPC_WSECT_DRIVER )
    vsp.SetParmVal( wid, "Root_Chord", "XSec_1", final.chord_length )
    vsp.SetParmVal( wid, "Tip_Chord", "XSec_1", final.chord_length )
    vsp.SetParmVal( wid, "Sweep", "XSec_1", 0)
    vsp.SetParmVal( wid, "TotalSpan", "WingGeom", final.wingspan )
    # vsp.AddSubSurf(wid, "SS_CONT_0")

    '''Airfoil'''
    #vsp.SetParmVal( wid, "Camber", "XSecCurve_0", 0.02 )
    #vsp.SetParmVal( wid, "CamberLoc", "XSecCurve_0", 0.4 )
    #vsp.SetParmVal( wid, "ThickChord", "XSecCurve_0", 0.12 )
    #vsp.Update()
    code_str = Plane.airfoil_codes[final.airfoil_num]
    m, p, t = parse_naca_airfoil(code_str)
    vsp.SetParmVal( wid, "Camber", "XSecCurve_0", m )
    vsp.SetParmVal( wid, "CamberLoc", "XSecCurve_0", p )
    vsp.SetParmVal( wid, "ThickChord", "XSecCurve_0", t )
    vsp.Update()

    '''Vtail Stab'''
    hs = vsp.AddGeom( "WING", "" )
    vsp.InsertXSec( hs, 1, vsp.XS_FOUR_SERIES )
    vsp.SetParmVal(hs, "X_Rel_Location", "XForm", total_length*0.95)
    vsp.SetParmVal(hs, "Z_Rel_Location", "XForm", -final.fuse_diam/6)
    vsp.CutXSec( hs, 1 )
    vsp.SetDriverGroup( hs, 1, vsp.AREA_WSECT_DRIVER, vsp.ROOTC_WSECT_DRIVER, vsp.TIPC_WSECT_DRIVER )
    vsp.SetParmVal( hs, "Root_Chord", "XSec_1", tail_diam)
    vsp.SetParmVal( hs, "Tip_Chord", "XSec_1", tail_diam)
    vsp.SetParmVal( hs, "Sweep", "XSec_1", 0)
    vsp.SetParmVal( hs, "TotalSpan", "WingGeom", final.wingspan/2 )
    vsp.SetParmVal( hs, "Dihedral", "XSec_1", 45 )

    vsp.SetParmVal( hs, "Camber", "XSecCurve_0", 0.0 )
    vsp.SetParmVal( hs, "CamberLoc", "XSecCurve_0", 0.0 )
    vsp.SetParmVal( hs, "ThickChord", "XSecCurve_0", 0.12 )
    
    # vsp.AddSubSurf(hs, "SS_CONT_0")

    '''prop'''
    prop = vsp.AddGeom( "PROP", "" )
    vsp.SetParmVal(prop, "X_Rel_Location", "XForm", total_length)
    vsp.SetParmVal(prop, "Z_Rel_Location", "XForm", -final.fuse_diam/6)
    vsp.SetParmVal(prop, "Diameter", "Design", 0.3 )
    vsp.Update()

    vsp.WriteVSPFile("genetic_alg.vsp3")
    vsp_sim(final)
