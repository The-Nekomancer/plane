# -*- coding: utf-8 -*-
import math
import pandas as pd
import numpy as np

def fuse_equations(final):

    '''Battery Bay'''
    fuse_rad = final.fuse_diam /2
    battery_length = final.bat["length"]
    battery_width = final.bat["width"]
    battery_height = final.bat["height"]
    wing_shelf = fuse_rad*0.5
    tail_length = (final.wingspan*0.33)
    tail_diam = final.fuse_diam/2
    connector = tail_length/4
    if final.batteries <=4:
        bat_bay_length = battery_length + 0.02
    elif final.batteries >4 and final.batteries <= 8:
        bat_bay_length = 2*battery_length + 0.02
    else:
        bat_bay_length = 3*battery_length + 0.02
    shell = 0.002

    with open("battery bay specifications.txt", "w") as f:
        f.write(f'"fuse_diam"= {str(final.fuse_diam)}')
        f.write('\n"fuse_rad"= ' + str(fuse_rad)) #fuselage radius
        f.write('\n"battery_length"= ' + str(battery_length))
        f.write('\n"battery_width"= ' + str(battery_width))
        f.write('\n"battery_height"= ' + str(battery_height))
        f.write('\n"bat_bay_length"= ' + str(bat_bay_length))
        f.write('\n"wing_shelf"= ' + str(wing_shelf))
        f.write('\n"shell"= ' + str(shell))
        f.write('\n"chord_length"= ' + str(final.chord_length))
        f.write('\n"tail_length"= ' + str(tail_length))
        f.write('\n"tail_diam"= ' + str(tail_diam))
        f.write('\n"connector"= ' + str(connector))
        
        
    #fuse_diam = 10
    fuse_length = 25
    #wingspan = 100
    wing_mount_diam = 3
    #wing_chord_length = 5
    wing_rotation_hor = 0.25 * fuse_length
    wing_rotation_vert = 0.6 * fuse_rad
    tail_length = fuse_length * 1.5
    tail_diam = 0.5 * final.fuse_diam
    tail_rad = tail_diam / 2
    tail_connector = tail_length * 0.33
    tail_elevation = ( final.fuse_diam - tail_diam ) * 0.2
    nose_cone_length = fuse_length / 2
    nose_cone_splinex = nose_cone_length * 0.76
    nose_cone_spliney = fuse_rad * 0.48
    tri_length = 1.5
    tri_degrees = 45
    tail_connect_top = fuse_rad - wing_rotation_vert + (fuse_rad * 0.05)
    #tail_connect_bottom = math.sqrt((tail_rad**2)-(tri_length/2)**2)
    #tail_base_len = math.sqrt((tail_rad**2)-(tri_length/2)**2)
    #tail_gamma = math.acos((-(tail_base_len**2)+(tail_rad**2)+((tri_length/2)**2))/(2*(tri_length/2)*tail_base_len))
    #tail_angle_of_int = math.pi - 2*(math.pi - tail_gamma - math.pi/4)
    fillet_rad = 0.1 ## inches
    #tail_chord_length = math.sqrt((tail_rad**2)+(tail_rad**2)-2*(tail_rad)*(tail_rad)*math.cos(tail_angle_of_int)) - 2*fillet_rad
    tail_offset = 2
    vtail_length = tail_length - tail_offset - 2
    battery_length = final.bat["length"]
    battery_width = final.bat["width"]
    battery_height = final.bat["height"]
    with open("assem equations.txt", "w") as f:
        f.write(f'"fuse_diam"= {str(final.fuse_diam)}')
        f.write('\n"fuse_rad"= ' + str(fuse_rad)) #fuselage radius
        f.write('\n"fuse_length"= ' + str(fuse_length))
        f.write('\n"wing_rotation_hor"= ' + str(wing_rotation_hor)) #the horizontal length of the wing shelf
        f.write('\n"wing_rotation_vert"= ' + str(wing_rotation_vert)) #the vertical wing cutout in the fuselage
        f.write('\n"tail_length"= ' + str(tail_length)) #length of tail
        f.write('\n"tail_diam"= ' + str(tail_diam)) #diameter of the tail
        f.write('\n"tail_rad"= ' + str(tail_rad))
        f.write('\n"tail_connector"= ' + str(tail_connector)) #the length of span that connects 
        f.write('\n"wingspan"= ' + str(final.wingspan)) #tip to tip wingspan
        f.write('\n"wing_mount_diam"= ' + str(wing_mount_diam))
        f.write('\n"tail_elevation"= ' + str(tail_elevation))
        #f.write('\n"tail_chord_length"= ' +str(tail_chord_length))
        f.write('\n"nose_cone_length"= ' + str(nose_cone_length))
        f.write('\n"nose_cone_splinex"= ' + str(nose_cone_splinex))
        f.write('\n"nose_cone_spliney"= ' + str(nose_cone_spliney))
        f.write('\n"wing_chord_length"= ' + str(final.chord_length))
        f.write('\n"tri_length"= ' + str(tri_length))
        f.write('\n"tri_degrees"= ' + str(tri_degrees))
        f.write('\n"tail_offset"= ' + str(tail_offset))
        f.write('\n"vtail_length"= ' + str(vtail_length))
        f.write('\n"fillet_rad"= ' + str(fillet_rad))
        f.write('\n"tail_connect_top"= ' + str(tail_connect_top))
        #f.write('\n"tail_connect_bottom"= ' + str(tail_connect_bottom))
        f.write('\n"wing_pos"= ' + str(final.wing_pos))
        f.write('\n"airfoil_num"= ' + str(final.airfoil_num))
        f.write('\n"alpha"= ' + str(final.alpha))
        f.write('\n"batteries"= ' + str(final.batteries))
        f.write('\n"battery_length"= ' + str(battery_length))
        f.write('\n"battery_width"= ' + str(battery_width))
        f.write('\n"battery_height"= ' + str(battery_height))

    # identify combined airfoil CSV path
    if final.airfoil_num == 0:
        csv_path = "naca4412_combined.csv"
    elif final.airfoil_num == 1:
        csv_path = "naca2412_combined.csv"
    else:
        raise ValueError("Invalid airfoil number")

    # Read the combined airfoil CSV
    combined_df = pd.read_csv(csv_path)

    # Filter for the Geometry rows
    geometry_df = combined_df[combined_df["Block_Type"] == "Geometry"]

    # Extract raw coordinates
    x_raw = geometry_df["x_coord"].to_numpy()
    y_raw = geometry_df["y_coord"].to_numpy()

    # Scale the coordinates
    x_scaled = x_raw * final.chord_length
    y_scaled = y_raw * final.chord_length

    # Write the scaled coordinates to a text file
    with open("scaled_airfoil_coords.txt", "w") as airfoil_file:
        for xx, yy in zip(x_scaled, y_scaled):
            airfoil_file.write(f"{xx}, {yy}\n")
    