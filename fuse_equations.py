import math

def fuse_equations(fuse_diam,fuse_length,wing_chord_length,wingspan):
    
    #fuse_diam = 10
    fuse_rad = fuse_diam /2
    fuse_length = 25
    #wingspan = 100
    wing_mount_diam = 3
    #wing_chord_length = 5
    wing_rotation_hor = 0.25 * fuse_length
    wing_rotation_vert = 0.6 * fuse_rad
    tail_length = fuse_length * 1.5
    tail_diam = 0.5 * fuse_diam
    tail_rad = tail_diam / 2
    tail_connector = tail_length * 0.33
    tail_elevation = ( fuse_diam - tail_diam ) * 0.2
    nose_cone_length = fuse_length / 2
    nose_cone_splinex = nose_cone_length * 0.76
    nose_cone_spliney = fuse_rad * 0.48
    tri_length = 1.5
    tri_degrees = 45
    tail_connect_top = fuse_rad - wing_rotation_vert + (fuse_rad * 0.05)
    tail_connect_bottom = math.sqrt((tail_rad**2)-(tri_length/2)**2)
    tail_base_len = math.sqrt((tail_rad**2)-(tri_length/2)**2)
    tail_gamma = math.acos((-(tail_base_len**2)+(tail_rad**2)+((tri_length/2)**2))/(2*(tri_length/2)*tail_base_len))
    tail_angle_of_int = math.pi - 2*(math.pi - tail_gamma - math.pi/4)
    fillet_rad = 0.1 ## inches
    tail_chord_length = math.sqrt((tail_rad**2)+(tail_rad**2)-2*(tail_rad)*(tail_rad)*math.cos(tail_angle_of_int)) - 2*fillet_rad
    tail_offset = 2
    vtail_length = tail_length - tail_offset - 2
    
    
    f = open("assem equations.txt", "w")
    f.write('"fuse_diam"= ' + str(fuse_diam)) #fuselage diameter
    f.write('\n"fuse_rad"= ' + str(fuse_rad)) #fuselage radius
    f.write('\n"fuse_length"= ' + str(fuse_length))
    f.write('\n"wing_rotation_hor"= ' + str(wing_rotation_hor)) #the horizontal length of the wing shelf
    f.write('\n"wing_rotation_vert"= ' + str(wing_rotation_vert)) #the vertical wing cutout in the fuselage
    f.write('\n"tail_length"= ' + str(tail_length)) #length of tail
    f.write('\n"tail_diam"= ' + str(tail_diam)) #diameter of the tail
    f.write('\n"tail_rad"= ' + str(tail_rad))
    f.write('\n"tail_connector"= ' + str(tail_connector)) #the length of span that connects 
    f.write('\n"wingspan"= ' + str(wingspan)) #tip to tip wingspan
    f.write('\n"wing_mount_diam"= ' + str(wing_mount_diam))
    f.write('\n"tail_elevation"= ' + str(tail_elevation))
    f.write('\n"tail_chord_length"= ' +str(tail_chord_length))
    f.write('\n"nose_cone_length"= ' + str(nose_cone_length))
    f.write('\n"nose_cone_splinex"= ' + str(nose_cone_splinex))
    f.write('\n"nose_cone_spliney"= ' + str(nose_cone_spliney))
    f.write('\n"wing_chord_length"= ' + str(wing_chord_length))
    f.write('\n"tri_length"= ' + str(tri_length))
    f.write('\n"tri_degrees"= ' + str(tri_degrees))
    f.write('\n"tail_offset"= ' + str(tail_offset))
    f.write('\n"vtail_length"= ' + str(vtail_length))
    f.write('\n"fillet_rad"= ' + str(fillet_rad))
    f.write('\n"tail_connect_top"= ' + str(tail_connect_top))
    f.write('\n"tail_connect_bottom"= ' + str(tail_connect_bottom))
    f.close()