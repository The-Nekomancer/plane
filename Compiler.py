from Plane_Class import Plane
import fuse_equations



obj = Plane(payload_mass = 3.5, priority = "Lift")

obj.calc_lift()
obj.calc_endurance()
obj.calc_range()
obj.calc_fuse_size()
obj.calc_mass()
#fuse_equations.fuse_equations(fuse_diam,fuse_length,wing_chord_length,wingspan)