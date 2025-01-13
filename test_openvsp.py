import openvsp as vsp

plots = 0
export_to_VSP = 1
if export_to_VSP ==1:
    # Create a new VSP model
    vsp.VSPRenew()
    fuse_length = 0.635
    tail_length = 1
    total_length = fuse_length + tail_length
    xsec_percent = fuse_length/total_length
    '''Fuselage'''
    fuseid = vsp.AddGeom( "FUSELAGE", "" )
    xsec_surf = vsp.GetXSecSurf( fuseid, 0 )
    sections = range(1,vsp.GetNumXSec( xsec_surf )-1)
    for x in sections:
        vsp.ChangeXSecShape( xsec_surf, x, vsp.XS_CIRCLE )
        xsec = vsp.GetXSec( xsec_surf, x)
        wid = vsp.GetXSecParm( xsec, "Circle_Diameter")
        vsp.SetParmVal( wid, 0.254)
    vsp.SetParmVal( fuseid, "Length", "Design", total_length)
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
    vsp.SetParmVal(wid, "X_Rel_Location", "XForm", total_length/2)# - 0.323/2)
    vsp.SetParmVal(wid, "Z_Rel_Location", "XForm", 0.254/2)
    vsp.CutXSec( wid, 1 )
    vsp.SetDriverGroup( wid, 1, vsp.AREA_WSECT_DRIVER, vsp.ROOTC_WSECT_DRIVER, vsp.TIPC_WSECT_DRIVER )
    vsp.SetParmVal( wid, "Root_Chord", "XSec_1", 0.254 )
    vsp.SetParmVal( wid, "Tip_Chord", "XSec_1", 0.254 )
    vsp.SetParmVal( wid, "Sweep", "XSec_1", 0)
    vsp.SetParmVal( wid, "TotalSpan", "WingGeom", 3 )

    '''Airfoil'''
    vsp.SetParmVal( wid, "Camber", "XSecCurve_0", 0.02 )
    vsp.SetParmVal( wid, "CamberLoc", "XSecCurve_0", 0.4 )
    vsp.SetParmVal( wid, "ThickChord", "XSecCurve_0", 0.12 )
    vsp.Update()
    
    '''Horizonal Stab'''
    wid = vsp.AddGeom( "WING", "" )
    vsp.InsertXSec( wid, 1, vsp.XS_FOUR_SERIES )
    vsp.SetParmVal(wid, "X_Rel_Location", "XForm", total_length/2)# - 0.323/2)
    vsp.SetParmVal(wid, "Z_Rel_Location", "XForm", 0.254/2)
    vsp.CutXSec( wid, 1 )
    vsp.SetDriverGroup( wid, 1, vsp.AREA_WSECT_DRIVER, vsp.ROOTC_WSECT_DRIVER, vsp.TIPC_WSECT_DRIVER )
    vsp.SetParmVal( wid, "Root_Chord", "XSec_1", 0.254 )
    vsp.SetParmVal( wid, "Tip_Chord", "XSec_1", 0.254 )
    vsp.SetParmVal( wid, "Sweep", "XSec_1", 0)
    vsp.SetParmVal( wid, "TotalSpan", "WingGeom", 3 )

    vsp.WriteVSPFile("genetic_alg.vsp3")
