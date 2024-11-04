from Plane_Class import Plane
import fuse_equations



obj = Plane(payload = 3.5, priority = "Lift")

L = obj.calc_lift()
print(L)
#fuse_equations.fuse_equations(fuse_diam,fuse_length,wing_chord_length,wingspan)