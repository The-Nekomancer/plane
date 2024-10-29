from Plane_Class import Plane
import fuse_equations

obj = Plane(payload = 10, priority = "Lift")

L = obj.calc_lift()
D = obj.calc_drag()
print(L)

obj.determine_wing_properties()

L = obj.calc_lift()

print(L)
print(D)
print(obj.chord_length)


fuse_equations.fuse_equations()