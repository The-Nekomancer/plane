# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 13:56:06 2024

@author: briggs

PURPOSE: The meat and potatos
MAIN COMPONENTS:
- population creation
- evaluation
- fitness function
- selction
- crossover
- population replacment
- mutation

Several plots occour afterward, but only occour is 'plots' is True, is useful for debugging GA
"""

from Plane_Class import Plane
import numpy as np
import random as r
import matplotlib.pyplot as plt
import pandas as pd
from instance_update import *

# r.seed(36)
def GA(payload,max_wing,max_bat,max_motors,arspd_weight,end_weight,range_weight,stall_weight,plots,vel_obj,end_obj,range_obj,stall_obj,bat_cell_size):
    '''Initial Population Creation'''
    record = []
    objects = []
    pure = []
    all_mutants = []
    mutants_list = []
    keepers_score = []
    pop = 100
    iteration_limit = 100
    keep = int(round(pop*0.05,0))
    mutation_rate = 2
    '''battery pool'''
    usable_bats =[]
    for q in range(len(Plane.batts)):
        if Plane.batts[q].get("cells") == bat_cell_size:
            usable_bats.append(Plane.batts[q])
    
    for i in range(pop):
        wing= r.uniform((max_wing * 0.25),max_wing)
        batteries = r.randint(1, max_bat)
        motor_num = r.randint(0, len(Plane.motors)-1)
        motor = Plane.motors[motor_num]
        motors = r.randint(1, max_motors)
        throttle = r.randint(1,4)
        alpha = r.randint(0,36)/4
        airfoil_num = r.randint(0, len(Plane.airfoils)-1)
        airfoil = Plane.airfoils[airfoil_num]
        bat = Plane.batts[2]
        obj = Plane(payload_mass=payload,wingspan=wing,batteries=batteries,motor=motor,motors=motors,alpha=alpha,throttle=throttle,motor_num=motor_num,airfoil_num=airfoil_num,airfoil=airfoil)
        objects.append(obj)
        pure.append(obj)
        record.append(obj)

    '''GA LOOP'''
    e = 1
    while e < iteration_limit: 
        print(e)    
        for g in range(pop):
            objects[g] = instance_update(objects[g])

        '''Evaluation'''
        # Every object in our population is given a score, and added to the list of scores
        # The scores are reset after every generation
        total_mass = 0
        total_wingspan = 0
        total_vel = 0
        total_stall = 0
        total_end = 0
        total_range = 0
        total_ld = 0
        mass_score  = []
        wingspan_score = []
        vel_score = []
        stall_score = []
        end_score = []
        range_score = []
        ld_score = []
        mass_obj = 0.25
        ld_obj = 100
        wingspan_obj = 0.1

        for j in range(pop):
            total_mass = total_mass + (objects[j].mass)
            total_wingspan = total_wingspan + (objects[j].wingspan)
            total_vel = total_vel + objects[j].cruise_velocity
            total_stall = total_stall + objects[j].stall_speed
            total_end = total_end + objects[j].endurance
            total_range = total_range + objects[j].range
            total_ld = total_ld + (objects[j].lift/objects[j].drag)
        for u in range(pop):
            mass_score.append(abs(mass_obj - objects[u].mass)/mass_obj)
            vel_score.append(abs(vel_obj - objects[u].cruise_velocity)/vel_obj)
            stall_score.append(abs(stall_obj - objects[u].stall_speed)/stall_obj)
            wingspan_score.append(abs(wingspan_obj - objects[u].wingspan)/wingspan_obj)
            end_score.append(abs(end_obj - objects[u].endurance)/end_obj)
            range_score.append(abs(range_obj - objects[u].range)/range_obj)
            ld_score.append(abs(ld_obj - (objects[u].lift/objects[u].drag))/ld_obj)

        '''Fitness Function'''
        # Weighted fitness function, allows for the user to specify priorities
        # This is in contrast to prioritizing a single metric and moving the rest to constraints
        score = []
        avg_weight = 0.25*(arspd_weight+end_weight+range_weight+stall_weight)/(4)
        for k in range(pop):
            objects[k].indi_score = (arspd_weight)*(1-vel_score[k]) + (end_weight)*(1-end_score[k]) + (range_weight)*(1-range_score[k]) + (stall_weight)*(1-stall_score[k]) + (avg_weight*0.1)*(1-mass_score[k])+(avg_weight*0)*(1-wingspan_score[k])+(avg_weight)*(1-ld_score[k])
            score.append(objects[k].indi_score)

        '''Selection'''
        score_to_beat = np.linspace(min(score), max(score), pop)
        keepers = []
        #Keeping individual sizes for later use
        wings = []
        bat = []
        motors = []
        moto_sel = []
        alfa = []
        throttles = []
        airfoils = []
        airfoil_nums = []

        # In order for a plane to pass on its genes, it must be in the top 5% of its generation
        # Several objects tied for 5th will all be included, this is because if mutations
        # don't signifigantly improve a generation the whole generation is likely to 
        # tie for first place, and all will be kept, crossed over and mutated
        for n in range(pop):
            if score[n] >= score_to_beat[pop - keep]:
                keepers.append(objects[n])
                keepers_score.append(score[n])

        for h in range(len(keepers)):
            wings.append(keepers[h].wingspan)
            bat.append(keepers[h].batteries)
            motors.append(keepers[h].motor)
            alfa.append(keepers[h].alpha)
            throttles.append(keepers[h].throttle)
            moto_sel.append(keepers[h].motor_num)
            airfoils.append(keepers[h].airfoil)
            airfoil_nums.append(keepers[h].airfoil_num)

        '''Crossover'''
        #Uniform crossover pattern, each chromasom is crossed over
        objects = []
        crossover = []
        for p in range(len(keepers)):
            wingspan = wings[r.randint(0, len(wings)-1)]
            batteries = bat[r.randint(0, len(bat)-1)]
            moto_select = moto_sel[r.randint(0, len(moto_sel)-1)]
            moto_num = moto_select
            motor = Plane.motors[moto_select]
            alpha = alfa[r.randint(0, len(alfa)-1)]
            throttle = throttles[r.randint(0, len(throttles)-1)]
            airfoil_sel = r.randint(0, len(airfoils)-1)
            airfoil = airfoils[airfoil_sel]
            airfoil_num = airfoil_nums[airfoil_sel]

            obj = Plane(payload_mass=payload,wingspan=wingspan,batteries=batteries,motor=motor,motor_num=moto_num,alpha=alpha,throttle=throttle,airfoil=airfoil,airfoil_num=airfoil_num)
            crossover.append(obj)
            objects.append(obj)

        '''Population Replacement'''
        while len(objects) < len(range(pop)):
            wingspan = r.uniform(min(wings)*1, max(wings)*1)
            batteries = r.randint(min(bat), max(bat))
            moto_sel = r.randint(0, len(keepers)-1)
            motor_num = keepers[moto_sel].motor_num
            motor = keepers[moto_sel].motor
            motors = keepers[moto_sel].motors
            airfoil_sel = r.randint(0, len(keepers)-1)
            airfoil = keepers[airfoil_sel].airfoil
            airfoil_num = keepers[airfoil_sel].airfoil_num
            alpha = keepers[r.randint(0, len(keepers)-1)].alpha
            throttle = keepers[r.randint(0, len(keepers)-1)].throttle
            obj = Plane(payload_mass=payload,wingspan=wingspan,batteries=batteries,motor=motor,motor_num=moto_num,motors=motors,alpha=alpha,throttle=throttle,airfoil=airfoil,airfoil_num=airfoil_num)
            objects.append(obj) 
            record.append(obj)
            if e < iteration_limit-1:
                pure.append(obj)

        '''Mutation'''
        mutants = []
        for u in range(len(objects)):
            if r.uniform(0, 100) >= (100 - mutation_rate):
                objects[u].wingspan = r.uniform((max_wing * 0.25), max_wing)
                objects[u].batteries = r.randint(1, max_bat)
                moto = r.randint(0, len(keepers)-1)
                objects[u].motor_num = keepers[moto].motor_num
                objects[u].motor = keepers[moto].motor
                objects[u].motors = r.randint(1, max_motors)
                ############AIRFOILS#############
                objects[u].airfoil_num = r.randint(0, len(Plane.airfoils)-1)
                objects[u].airfoil = Plane.airfoils[airfoil_num]
                objects[u].alpha = r.randint(0,36)/4
                objects[u].throttle = r.randint(1,4)
                #objects[u].throttle = r.randint(1,len(objects[u].motor)-1)
                mutants.append(objects[u])
                all_mutants.append(objects[u])
                mutants_list.append(len(record) - len(objects) + u -1)

        '''Additional Calculations'''
        for w in range(len(objects)):
            objects[w].calc_mass()
            objects[w].calc_endurance()
            objects[w].calc_range()
            objects[w].calc_lift()
            objects[w].calc_vtail_lift()
            objects[w].calc_drag()
            objects[w].calc_velocity()

        e = e + 1

    '''Plotting values collected'''
    #All of these values are saved to be used in plotting and analysis
    all_wingspans = []
    all_end = []
    all_range = []
    all_mass = []
    all_lift = []
    all_vel = []
    all_stall_speed = []
    all_drag = []
    all_ld = []
    all_cl = []
    all_cd = []

    pure_wing = []

    mutant_wing = []
    mutant_end = []
    mutant_range = []
    mutant_mass = []
    mutant_lift = []
    mutant_vel = []
    mutant_stall_speed = []

    for f in range(len(record)):
        record[f].calc_mass()
        record[f].calc_endurance()
        record[f].calc_range()
        record[f].calc_lift()
        record[f].calc_vtail_lift()
        record[f].calc_drag()
        record[f].calc_velocity()
        all_wingspans.append(record[f].wingspan)
        all_end.append(record[f].endurance)
        all_range.append(record[f].range)
        all_mass.append(record[f].mass)
        all_lift.append(record[f].lift)
        all_vel.append(record[f].cruise_velocity)
        all_stall_speed.append(record[f].stall_speed)
        all_drag.append(record[f].drag)
        all_ld.append(record[f].lift/record[f].drag)
        all_cl.append(record[f].CL)
        all_cd.append(record[f].CD)

    for x in range(len(pure)):
        pure_wing.append(pure[x].wingspan)
    for z in range(len(all_mutants)):
        mutant_wing.append(all_mutants[z].wingspan)
        mutant_end.append(all_mutants[z].endurance)
        mutant_range.append(all_mutants[z].range)
        mutant_mass.append(all_mutants[z].mass)
        mutant_lift.append(all_mutants[z].lift)
        mutant_vel.append(all_mutants[z].cruise_velocity)
        mutant_stall_speed.append(all_mutants[z].stall_speed)

    '''Final Airplane'''
    # Here the final planes charecteristics are finalized and saved
    final_wing = pure[-1].wingspan
    final_bat = pure[-1].batteries
    final_motor = pure[-1].motor
    final_motor_num = pure[-1].motor_num
    final_motors = pure[-1].motors
    final_alpha = pure[-1].alpha
    final_airfoil = pure[-1].airfoil
    final_airfoil_num = pure[-1].airfoil_num
    final_throttle = pure[-1].throttle
    final = Plane(payload_mass=payload, wingspan=final_wing,batteries=final_bat,motor=final_motor,motor_num=final_motor_num,motors=final_motors,alpha=final_alpha,airfoil=final_airfoil,airfoil_num=final_airfoil_num,throttle=final_throttle)
    final.wingspan = round(final.wingspan,3)
    final.chord_length = round(final.chord_length,3)

    '''CG Calc'''
    final.cg_checker()
    while final.cg_check == False:
        if final.cg_correction == 'tail heavy':
            final.fuse_length = final.fuse_length*1.01
        if final.cg_correction == 'nose heavy':
            if final.fuse_length > 0.1:
                final.fuse_length = final.fuse_length*0.99
            elif final.batteries > 1:
                final.batteries = final.batteries -1
            else:
                print("Conduct addiaional calculations for the cg, likely unstable")
                break
        final.cg_checker()
    print(final.cg_check)
    final.fuse_diam = round(final.fuse_diam,3)
    final.fuse_length = round(final.fuse_length,3)
    
    # Properites are calculated
    final = instance_update(final)
    
    # Final score is calculated
    mass_score = (abs(mass_obj - final.mass)/mass_obj)
    vel_score = (abs(vel_obj - final.cruise_velocity)/vel_obj)
    wingspan_score = (abs(wingspan_obj - final.wingspan)/wingspan_obj)
    end_score = (abs(end_obj - final.endurance)/end_obj)
    range_score = (abs(range_obj - final.range)/range_obj)
    stall_score = (abs(stall_obj - final.stall_speed)/stall_obj)
    ld_score = (abs(ld_obj - (final.lift/final.drag))/ld_obj)
    final.active_score = (arspd_weight)*(1-vel_score) + (end_weight)*(1-end_score) + (range_weight)*(1-range_score) + (stall_weight)*(1-stall_score)
    final.reactive_score = (avg_weight)*(1-mass_score)+(avg_weight)*(1-wingspan_score)+(avg_weight)*(1-ld_score)
    final.score = final.active_score + final.reactive_score
    final_error = ((arspd_weight+end_weight+range_weight+stall_weight - final.active_score)/(arspd_weight+end_weight+range_weight+stall_weight))*100

    # All of our plots are generated
    if plots == 1:
        '''wingspan'''
        fig = plt.figure(1)
        plt.scatter(range(len(record)),all_wingspans, marker = ".", label="Solutions")
        plt.scatter(mutants_list ,mutant_wing, marker = ".", label="Mutants")
        plt.legend()
        plt.title("Wingspan")
        plt.xlabel("Instance Number")
        plt.ylabel("Meters")
        plt.show()
        '''velocity'''
        fig = plt.figure(2)
        plt.scatter(range(len(record)),all_vel, marker = ".", label="Solutions")
        plt.scatter(mutants_list ,mutant_vel, marker = ".", label="Mutants")
        plt.legend()
        plt.title("Cruise Velocity")
        plt.xlabel("Instance Number")
        plt.ylabel("Meters/Second")
        plt.show()
        '''mass'''
        fig = plt.figure(3)
        plt.scatter(range(len(record)),all_mass, marker = ".", label="Solutions")
        plt.scatter(mutants_list ,mutant_mass, marker = ".", label="Mutants")
        plt.legend()
        plt.title("Mass")
        plt.xlabel("Instance Number")
        plt.ylabel("Kg")
        plt.show()
        '''endurance'''
        fig = plt.figure(4)
        plt.scatter(range(len(record)),all_end, marker = ".", label="Solutions")
        plt.scatter(mutants_list ,mutant_end, marker = ".", label="Mutants")
        plt.legend()
        plt.title("Endurance")
        plt.xlabel("Instance Number")
        plt.ylabel("Hours")
        plt.show()
        '''range'''
        fig = plt.figure(5)
        plt.scatter(range(len(record)),all_range, marker = ".", label="Solutions")
        plt.scatter(mutants_list ,mutant_range, marker = ".", label="Mutants")
        plt.legend()
        plt.title("Range")
        plt.xlabel("Instance Number")
        plt.ylabel("Km")
        plt.show()
        '''lift'''
        fig = plt.figure(6)
        plt.scatter(range(len(record)),all_lift, marker = ".", label="Solutions")
        plt.scatter(mutants_list ,mutant_lift, marker = ".", label="Mutants")
        plt.legend()
        plt.title("Lift")
        plt.xlabel("Instance Number")
        plt.ylabel("Kg (converted from N)")
        plt.show()
        '''Endurance and Range'''
        fig = plt.figure(7)
        plt.scatter(all_end,all_range, marker = ".", label="Solutions")
        plt.scatter(final.endurance, final.range, label="Final")
        plt.legend()
        plt.title("Performance Curve Comparison")
        plt.xlabel("Endurance (Hours)")
        plt.ylabel("Range (Km)")
        plt.show()
        '''L over D'''
        fig = plt.figure(8)
        plt.scatter(all_drag,all_lift, marker = ".", label="Solutions")
        plt.scatter(final.drag, final.lift, label="Final")
        plt.legend()
        plt.title("Performance Curve Comparison")
        plt.xlabel("Drag (Kg)")
        plt.ylabel("Lift (Kg)")
        plt.show()
        '''CL and CD over alpha'''
        fig = plt.figure(9)
        plt.subplot(2, 1,1)
        plt.scatter(Plane.naca2412['Alpha'],Plane.naca2412['CL'], marker = ".", label="CL")
        plt.ylabel("CL")
        plt.title("CD and CL w/ respect to alpha")
        plt.subplot(2, 1,2)
        plt.scatter(Plane.naca2412['Alpha'],Plane.naca2412['CD'], marker='.',label="CD")
        plt.xlabel("Alpha")
        plt.ylabel("CD")
        plt.show()

        fig = plt.figure(10)
        plt.plot(range(len(keepers_score)), keepers_score)
        plt.xlabel("Instances kept")
        plt.ylabel("score")
        plt.title("Scores over time")
        plt.show()
    return final, record, objects, final_error
