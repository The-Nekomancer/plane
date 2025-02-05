import openvsp as vsp
def vsp_sim(final):
    print("-> Begin TestVSPAeroComputeGeom" )
    print( "" )
    
    #open the file created in GenerateGeom
    vsp.ReadVSPFile("genetic_alg.vsp3");  # Sets VSP3 file name
    
    #==== Analysis: VSPAero Compute Geometry ====//
    analysis_name = "VSPAEROSweep"
    print( analysis_name )
    
    # Set defaults
    vsp.SetAnalysisInputDefaults( analysis_name )
    # Analysis method
    analysis_method = vsp.GetIntAnalysisInput( analysis_name, "AnalysisMethod" )
    print("analysis")
    
    # analysis_method[0] = vsp.VORTEX_LATTICE
    # analysis_method[0] = 0
    vsp.SetIntAnalysisInput( analysis_name, "AnalysisMethod", analysis_method )
    alpha = [0,15]
    alpha_end = [15]
    vel_in_mach = final.cruise_velocity*0.00291545
    mach = [vel_in_mach]
    Npts = [61,1]
    re = [(final.cruise_velocity*final.chord_length/0.000015)]
    vsp.SetDoubleAnalysisInput( analysis_name, "AlphaStart", alpha, 0 )
    vsp.SetDoubleAnalysisInput( analysis_name, "MachStart", mach, 0 )
    vsp.SetDoubleAnalysisInput( analysis_name, "AlphaEnd", alpha_end, 0 )
    vsp.SetIntAnalysisInput( analysis_name, "AlphaNpts", Npts, 0 )
    vsp.SetDoubleAnalysisInput( analysis_name, "ReCref", re, 0 )
    
    # list inputs, type, and current values
    vsp.PrintAnalysisInputs( analysis_name )
    print( "" )
    
    # Execute
    print( "Executing..." )
    rid = vsp.ExecAnalysis( analysis_name )
    print( "COMPLETE" )
    
    # Get & Display Results
    vsp.PrintResults( rid )
    vsp.WriteResultsCSVFile(rid, "Results.csv")