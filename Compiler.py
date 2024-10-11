from Plane_Class import Plane

obj = Plane(payload = 50, priority = "Range")

L = obj.calc_lift()
D = obj.calc_drag()
V = obj.calc_vel()
print("Lift: " + str(L) + " lbs")
print("Drag: " + str(D) + " lbs")
print("Velocity: " + str(V/12) + " ft/s")
obj.determine_wing_properties()
L = obj.calc_lift()
print("Lift: " + str(L) + " lbs")