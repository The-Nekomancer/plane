from vsp_results_viewer import vsp_results_viewer
from performance_plotter import performance_plotter
from Plane_Class import Plane

CL,CD,LD,Alpha =vsp_results_viewer()
a = len(Plane.motors[0])
for i in range(a):
    thrust = Plane.motors[0].loc[i,'Thrust (kg)']
    print(thrust)
# print(a)
# performance_plotter(CL,CD,LD,Alpha)
# print(Alpha)
# print(CL)
# print(CD)
# print(LD)