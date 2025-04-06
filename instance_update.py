from Plane_Class import Plane
import numpy as np
import pandas as pd

def instance_update(object):
    object.calc_mass()
    object.calc_endurance()
    object.calc_range()
    object.calc_lift()
    object.calc_vtail_lift()
    object.calc_drag()
    object.calc_velocity()

    if object.lift <= object.mass* 0.95:
        i = 1#r.randint(1,3)
        if i == 1:
            while object.lift <= object.mass * 0.95:
                if object.alpha <= 9:
                    object.alpha = object.alpha + 0.25
                    object.calc_lift()
                    object.calc_velocity()
                else:
                    i == 2
                    break
        if i == 2:
            while object.lift <= object.mass* 0.95:
                if object.throttle < (len(object.motor)-8):
                    object.throttle = object.throttle + 1
                    object.calc_velocity()
                    object.calc_lift()
                else:
                    i ==3
                    break
        if i == 3:
            while object.lift <= object.mass* 0.95:
                    if object.wingspan <= object.max_wingspan*0.98:
                        object.wingspan = object.wingspan * 1.01
                        object.chord_length = object.chord_length * 1.01
                        object.calc_lift()
                        object.calc_velocity()
                    else:
                        del object
        object.calc_mass()
        object.calc_endurance()
        object.calc_range()
        object.calc_lift()
        object.calc_vtail_lift()
        object.calc_drag()
        object.calc_velocity()

    if object.lift >= object.mass* 1.05:
        i = 1
        if i == 1:
            while object.lift >= object.mass * 1.05:
                if object.alpha >= 2:
                    object.alpha = object.alpha - 0.25
                    object.calc_lift()
                    object.calc_velocity()
                else:
                    i == 2
                    break
        if i == 2:
            while object.lift >= object.mass* 1.05:
                if object.throttle > 2:
                    object.throttle = object.throttle - 1
                    object.calc_velocity()
                    object.calc_lift()
                else:
                    i ==3
                    break
        if i == 3:
            while object.lift >= object.mass* 1.05:
                    if object.wingspan >= object.min_wingspan*1.1:
                        object.wingspan = object.wingspan * 0.99
                        object.chord_length = object.chord_length * 0.99
                        object.calc_lift()
                        object.calc_velocity()
                    else:
                        del object
    object.calc_mass()
    object.calc_endurance()
    object.calc_range()
    object.calc_lift()
    object.calc_vtail_lift()
    object.calc_drag()
    object.calc_velocity()
    
    while object.cruise_velocity < object.stall_speed*1.1:
        if object.throttle < len(object.motor) -4:
            object.throttle = object.throttle + 1
            object.calc_mass()
            object.calc_endurance()
            object.calc_range()
            object.calc_lift()
            object.calc_vtail_lift()
            object.calc_drag()
            object.calc_velocity()
        else:
            break
    return object