# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 13:56:06 2024

@author: briggs
"""

from Plane_Class import Plane
import numpy as np
import random as r
import matplotlib.pyplot as plt
import pandas as pd

# r.seed(36)
def GA(min_wing,max_wing,min_bat,max_bat,A,B,C,D,E,F,plots,q1,q2,q3,q4,mass_obj,ld_obj,vel_obj,wingspan_obj,end_obj,range_obj):
    '''Initial Population Creation'''
    record = []
    objects = []
    pure = []
    all_mutants = []
    mutants_list = []
    keepers_score = []
    #THESE VALUES WORK
    #pop = 100
    #iteration_limit = 100
    #keep = 5
    #mutation_rate = 2
    pop = q1
    iteration_limit = q2
    keep = int(round(pop*q3,0))
    mutation_rate = q4
    for i in range(pop):
        wing= r.uniform(min_wing,max_wing)
        batteries = r.randint(min_bat, max_bat)
        motor_num = r.randint(0, len(Plane.motors)-1)
        motor = Plane.motors[motor_num]
        throttle = r.randint(1,4)
        alpha = r.randint(0,40)/4
        airfoil_num = r.randint(0, 1)
        airfoil = Plane.airfoils[airfoil_num]
        obj = Plane(wingspan=wing,batteries=batteries,motor=motor,alpha=alpha,throttle=throttle,motor_num=motor_num, airfoil_num=airfoil_num, airfoil = airfoil)
        objects.append(obj)
        pure.append(obj)
        record.append(obj)

    '''GA LOOP'''
    e = 1
    while e < iteration_limit:     
        for g in range(pop):
            objects[g].calc_mass()
            objects[g].calc_endurance()
            objects[g].calc_range()
            objects[g].calc_lift()
            objects[g].calc_vtail_lift()
            objects[g].calc_drag()
            objects[g].calc_velocity()

            if objects[g].lift <= objects[g].mass* 0.95:
                i = 1#r.randint(1,3)
                if i == 1:
                    while objects[g].lift <= objects[g].mass * 0.95:
                        if objects[g].alpha <= 10:
                            objects[g].alpha = objects[g].alpha + 0.25
                            objects[g].calc_lift()
                            objects[g].calc_velocity()
                        else:
                            i == 2
                            break
                if i == 2:
                    while objects[g].lift <= objects[g].mass* 0.95:
                        if objects[g].throttle < (len(objects[g].motor)-1):
                            objects[g].throttle = objects[g].throttle + 1
                            objects[g].calc_velocity()
                            objects[g].calc_lift()
                        #elif objects[g].motor_num < len(Plane.motors)-1:
                        #    objects[g].motor_num = objects[g].motor_num + 1
                        #    objects[g].motor = Plane.motors[objects[g].motor_num]
                        #    objects[g].throttle = 1
                        #    objects[g].calc_velocity()
                        #    objects[g].calc_lift()
                        else:
                            i ==3
                            break
                if i == 3:
                    while objects[g].lift <= objects[g].mass* 0.95:
                            if objects[g].wingspan <= objects[g].max_wingspan*0.98:
                                objects[g].wingspan = objects[g].wingspan * 1.01
                                objects[g].chord_length = objects[g].chord_length * 1.01
                                objects[g].calc_lift()
                                objects[g].calc_velocity()
                            else:
                                del objects[g]
            objects[g].calc_mass()
            objects[g].calc_endurance()
            objects[g].calc_range()
            objects[g].calc_lift()
            objects[g].calc_vtail_lift()
            objects[g].calc_drag()
            objects[g].calc_velocity()

            if objects[g].lift >= objects[g].mass* 1.05:
                i = 1#r.randint(1,3)
                if i == 1:
                    while objects[g].lift >= objects[g].mass * 1.05:
                        if objects[g].alpha >= 2:
                            objects[g].alpha = objects[g].alpha - 0.25
                            objects[g].calc_lift()
                            objects[g].calc_velocity()
                        else:
                            i == 2
                            break
                if i == 2:
                    while objects[g].lift >= objects[g].mass* 1.05:
                        if objects[g].throttle > 2:
                            objects[g].throttle = objects[g].throttle - 1
                            objects[g].calc_velocity()
                            objects[g].calc_lift()
                        #elif objects[g].motor_num > len(Plane.motors)-1:
                        #    objects[g].motor_num = objects[g].motor_num - 1
                        #    objects[g].motor = Plane.motors[objects[g].motor_num]
                        #    objects[g].throttle = len(Plane.motors) - 1
                        #    objects[g].calc_velocity()
                        #    objects[g].calc_lift()
                        else:
                            i ==3
                            break
                if i == 3:
                    while objects[g].lift >= objects[g].mass* 1.05:
                            if objects[g].wingspan >= objects[g].min_wingspan*1.1:
                                objects[g].wingspan = objects[g].wingspan * 0.99
                                objects[g].chord_length = objects[g].chord_length * 0.99
                                objects[g].calc_lift()
                                objects[g].calc_velocity()
                            else:
                                del objects[g]
            objects[g].calc_mass()
            objects[g].calc_endurance()
            objects[g].calc_range()
            objects[g].calc_lift()
            objects[g].calc_vtail_lift()
            objects[g].calc_drag()
            objects[g].calc_velocity()

        '''Evaluation'''
        # Every object in our population is given a score, and added to the list of scores
        # The scores are reset after every generation
        total_mass = 0
        total_wingspan = 0
        total_vel = 0
        total_end = 0
        total_range = 0
        total_ld = 0
        mass_score  = []
        wingspan_score = []
        vel_score = []
        end_score = []
        range_score = []
        ld_score = []

        for j in range(pop):
            total_mass = total_mass + (objects[j].mass)
            total_wingspan = total_wingspan + (objects[j].wingspan)
            total_vel = total_vel + objects[j].cruise_velocity
            total_end = total_end + objects[j].endurance
            total_range = total_range + objects[j].range
            total_ld = total_ld + (objects[j].lift/objects[j].drag)
        for u in range(pop):
            mass_score.append(abs(mass_obj - objects[u].mass)/mass_obj)
            # ld_score.append(abs(ld_obj - (objects[u].CL/objects[u].CD))/ld_obj)
            ld_score.append(abs(ld_obj - (Plane.airfoils[objects[u].airfoil_num].loc[1+4*objects[u].alpha, 'CL']/Plane.airfoils[objects[u].airfoil_num].loc[1+4*objects[u].alpha, 'CD']))/ld_obj)
            vel_score.append(abs(vel_obj - objects[u].cruise_velocity)/vel_obj)
            wingspan_score.append(abs(wingspan_obj - objects[u].wingspan)/wingspan_obj)
            end_score.append(abs(end_obj - objects[u].endurance)/end_obj)
            range_score.append(abs(range_obj - objects[u].range)/range_obj)

        '''Fitness Function'''
        # Weighted fitness function, allows for the user to specify priorities
        # This is in contrast to prioritizing a single metric and moving the rest to constraints
        score = []
        for k in range(pop):
            score.append((A)*(1-mass_score[k]) + (B)*(1-ld_score[k]) + (C)*(1-vel_score[k]) + (D)*(1-wingspan_score[k]) + (E)*(1-end_score[k]) + (F)*(1-range_score[k]))

        '''Selection'''
        score_to_beat = np.linspace(min(score), max(score), pop)
        keepers = []
        #Keeping indivisual sizes for later use
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

            obj = Plane(wingspan=wingspan,batteries=batteries,motor=motor,motor_num=moto_num,alpha=alpha, throttle=throttle, airfoil=airfoil, airfoil_num = airfoil_num)
            crossover.append(obj)
            objects.append(obj)

        '''Population Replacement'''
        while len(objects) < len(range(pop)):
            wingspan = r.uniform(min(wings)*1, max(wings)*1)
            batteries = r.randint(min(bat), max(bat))
            moto_sel = r.randint(0, len(keepers)-1)
            motor_num = keepers[moto_sel].motor_num
            motor = keepers[moto_sel].motor
            airfoil_sel = r.randint(0, len(keepers)-1)
            airfoil = keepers[airfoil_sel].airfoil
            airfoil_num = keepers[airfoil_sel].airfoil_num
            
            alpha = keepers[r.randint(0, len(keepers)-1)].alpha
            throttle = keepers[r.randint(0, len(keepers)-1)].throttle
            obj = Plane(wingspan=wingspan,batteries=batteries,motor=motor,alpha=alpha,throttle=throttle,motor_num=motor_num)
            objects.append(obj) 
            record.append(obj)
            pure.append(obj)

        '''Mutation'''
        mutants = []
        for u in range(len(objects)):
            if r.uniform(0, 100) >= (100 - mutation_rate):
                objects[u].wingspan = r.uniform(1, 3)
                objects[u].batteries = r.randint(1, 4)
                moto = r.randint(0, len(keepers)-1)
                objects[u].motor_num = keepers[moto].motor_num
                objects[u].motor = keepers[moto].motor
                
                objects[u].alpha = r.randint(0,40)/4
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
    final_alpha = pure[-1].alpha
    final_airfoil = pure[-1].airfoil
    final_throttle = pure[-1].throttle
    final = Plane(wingspan=final_wing,batteries=final_bat,motor=final_motor,alpha=final_alpha, airfoil = final_airfoil, throttle = final_throttle)
    final.wingspan = round(final.wingspan,3)
    final.chord_length = round(final.chord_length,3)
    final.fuse_diam = round(final.fuse_diam,3)
    final.fuse_length = round(final.fuse_length,3)
    # Properites are calculated
    final.calc_mass()
    final.calc_endurance()
    final.calc_range()
    final.calc_lift()
    final.calc_vtail_lift()
    final.calc_drag()
    final.calc_velocity()
    # This if loop is used to make sure that the plane generates sufficient lift
    if final.lift <= final.mass* 0.95:
        i = 1#r.randint(1,3)
        if i == 1:
            while final.lift <= final.mass * 0.95:
                if final.alpha <= 10:
                    final.alpha = final.alpha + 0.25
                    final.calc_lift()
                    final.calc_velocity()
                else:
                    i == 2
                    break
        if i == 2:
            while final.lift <= final.mass* 0.95:
                if final.throttle < (len(final.motor)-1):
                    final.throttle = final.throttle + 1
                    final.calc_velocity()
                    final.calc_lift()
                elif final.motor_num < len(Plane.motors)-1:
                    final.motor_num = final.motor_num + 1
                    final.motor = Plane.motors[final.motor_num]
                    final.throttle = 1
                    final.calc_velocity()
                    final.calc_lift()
                else:
                    i ==3
                    break
        if i == 3:
            while final.lift <= final.mass* 0.95:
                    if final.wingspan <= final.max_wingspan*0.98:
                        final.wingspan = final.wingspan * 1.01
                        final.chord_length = final.chord_length * 1.01
                        final.calc_lift()
                        final.calc_velocity()
                    else:
                        del final
                        print("The algorithm failed to find a valid solution")
                        print("Rethink your expectations!")
        # If the charecteristics have changed then the properties are calculated again
        final.calc_mass()
        final.calc_endurance()
        final.calc_range()
        final.calc_lift()
        final.calc_vtail_lift()
        final.calc_drag()
        final.calc_velocity()
        if final.lift >= final.mass* 1.05:
            i = 1#r.randint(1,3)
            if i == 1:
                while final.lift >= final.mass * 1.05:
                    if final.alpha >= 2:
                        final.alpha = final.alpha - 0.25
                        final.calc_lift()
                        final.calc_velocity()
                    else:
                        i == 2
                        break
            if i == 2:
                while final.lift >= final.mass* 1.05:
                    if final.throttle > 2:
                        final.throttle = final.throttle - 1
                        final.calc_velocity()
                        final.calc_lift()
                    #elif final.motor_num > len(Plane.motors)-1:
                    #    final.motor_num = final.motor_num - 1
                    #    final.motor = Plane.motors[final.motor_num]
                    #    final.throttle = len(Plane.motors) - 1
                    #    final.calc_velocity()
                    #    final.calc_lift()
                    else:
                        i ==3
                        break
            if i == 3:
                while final.lift >= final.mass* 1.05:
                        if final.wingspan >= final.min_wingspan*1.1:
                            final.wingspan = final.wingspan * 0.99
                            final.chord_length = final.chord_length * 0.99
                            final.calc_lift()
                            final.calc_velocity()
                        else:
                            del final
            final.calc_mass()
            final.calc_endurance()
            final.calc_range()
            final.calc_lift()
            final.calc_vtail_lift()
            final.calc_drag()
            final.calc_velocity()

    # Final score is calculated
    mass_score = (abs(mass_obj - final.mass)/mass_obj)
    ld_score = (abs(ld_obj - (final.CL/final.CD))/ld_obj)
    vel_score = (abs(vel_obj - final.cruise_velocity)/vel_obj)
    wingspan_score = (abs(wingspan_obj - final.wingspan)/wingspan_obj)
    end_score = (abs(end_obj - final.endurance)/end_obj)
    range_score = (abs(range_obj - final.range)/range_obj)
    final.score = ((A)*(1-mass_score) + (B)*(1-ld_score) + (C)*(1-vel_score) + (D)*(1-wingspan_score) + (E)*(1-end_score) + (F)*(1-range_score))
    final_error = ((A+B+C+D+E+F - final.score)/(A+B+C+D+E+F))*100

    if final.score <= 0:
        plots = 0
        print("The Algorithm failed to produce a viable options based on the requirements")
    # All of our plots are generated
    if plots == 1:
        '''wingspan'''
        fig = plt.figure(1)
        plt.scatter(range(len(record)),all_wingspans, marker = ".", label="Solutions")
        plt.scatter(mutants_list ,mutant_wing, marker = ".", label="Mutants")
        plt.legend()
        plt.title("Wingspan")
        plt.xlabel("Iteration Number")
        plt.ylabel("Meters")
        plt.show()
        '''velocity'''
        fig = plt.figure(2)
        plt.scatter(range(len(record)),all_vel, marker = ".", label="Solutions")
        plt.scatter(mutants_list ,mutant_vel, marker = ".", label="Mutants")
        plt.legend()
        plt.title("Cruise Velocity")
        plt.xlabel("Iteration Number")
        plt.ylabel("Meters/Second")
        plt.show()
        '''mass'''
        fig = plt.figure(3)
        plt.scatter(range(len(record)),all_mass, marker = ".", label="Solutions")
        plt.scatter(mutants_list ,mutant_mass, marker = ".", label="Mutants")
        plt.legend()
        plt.title("Mass")
        plt.xlabel("Iteration Number")
        plt.ylabel("Kg")
        plt.show()
        '''endurance'''
        fig = plt.figure(4)
        plt.scatter(range(len(record)),all_end, marker = ".", label="Solutions")
        plt.scatter(mutants_list ,mutant_end, marker = ".", label="Mutants")
        plt.legend()
        plt.title("Endurance")
        plt.xlabel("Iteration Number")
        plt.ylabel("Hours")
        plt.show()
        '''range'''
        fig = plt.figure(5)
        plt.scatter(range(len(record)),all_range, marker = ".", label="Solutions")
        plt.scatter(mutants_list ,mutant_range, marker = ".", label="Mutants")
        plt.legend()
        plt.title("Range")
        plt.xlabel("Iteration Number")
        plt.ylabel("Km")
        plt.show()
        '''lift'''
        fig = plt.figure(6)
        plt.scatter(range(len(record)),all_lift, marker = ".", label="Solutions")
        plt.scatter(mutants_list ,mutant_lift, marker = ".", label="Mutants")
        plt.legend()
        plt.title("Lift")
        plt.xlabel("Iteration Number")
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
        plt.xlabel("Interations kept")
        plt.ylabel("score")
        plt.title("Scores over time")
        plt.show()
    return final, record, objects, final_error
