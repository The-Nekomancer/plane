# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 13:56:06 2024

@author: brigg
"""

from Plane_Class import Plane
import numpy as np
import random as r
import matplotlib.pyplot as plt
import pandas as pd

def GA(priority):
    '''Initial Population Creation'''
    record = []
    objects = []
    pure = []
    all_mutants = []
    mutants_list = []
    pop = 100
    iteration_limit = 100
    keep = 5
    mutation_rate = 2
    for i in range(pop):
        wing= r.uniform(1,3)
        batteries = r.randint(1, 4)
        motor_num = r.randint(0, 1)
        motor = Plane.motors[motor_num]
        throttle = r.randint(2,len(motor)-1)
        alpha = r.randint(0,40)/4
        obj = Plane(wingspan=wing,batteries=batteries,motor=motor,alpha=alpha,throttle=throttle,motor_num=motor_num)
        objects.append(obj)
        pure.append(obj)
        record.append(obj)
    
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
            # objects.append(obj)
            # record.append(objects[g])
            # pure.append(objects[g])
            
        '''Evaluation'''
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
            mass_score.append(objects[u].mass/total_mass)
            wingspan_score.append(objects[u].wingspan/total_wingspan)
            vel_score.append(objects[u].cruise_velocity/total_vel)
            end_score.append(objects[u].endurance/total_end)
            range_score.append(objects[u].range/total_range)
            ld_score.append((objects[u].CL/objects[u].CD)/total_ld)
                
        '''Fitness Function'''
        #Weighted fitness function, allows for the user to specify priorities
        #This is in contrast to prioritizing a single metric and moving the rest to constraints
        score = []
        for k in range(pop):
            if priority == "low speed":
                score.append((4)*(1-mass_score[k]) + (4)*(ld_score[k]) + (10)*(1-vel_score[k]) + (3)*(1-wingspan_score[k]) + (6)*end_score[k] + (3)*range_score[k])
            elif priority == "high speed":
                score.append((1)*(1-mass_score[k]) + (1)*(ld_score[k]) + (10)*(vel_score[k]) + (1)*(1-wingspan_score[k]) + (1)*end_score[k] + (1)*range_score[k])
            
        '''Selection'''
        average_score = sum(score)/pop
        score_to_beat = np.linspace(min(score), max(score), pop)
        keepers = []
        #Keeping indivisual sizes for later use
        wings = []
        bat = []
        motors = []
        alfa = []
        
        for n in range(pop):
            # if score[n] < average_score:
            if score[n] >= score_to_beat[pop - keep]:
                keepers.append(objects[n])
                
        for h in range(len(keepers)):
            wings.append(keepers[h].wingspan)
            bat.append(keepers[h].batteries)
            motors.append(keepers[h].motor)
            alfa.append(keepers[h].alpha)
    
        '''Crossover'''
        #Uniform crossover pattern, each chromasom is crossed over
        objects = []
        crossover = []
        for p in range(len(keepers)):
            wingspan = keepers[r.randint(0, len(keepers)-1)].wingspan
            batteries = keepers[r.randint(0, len(keepers)-1)].batteries
            motor = keepers[r.randint(0, len(keepers)-1)].motor
            alpha = keepers[r.randint(0, len(keepers)-1)].alpha
            obj = Plane(wingspan=wingspan,batteries=batteries,motor=motor,alpha=alpha)
            crossover.append(obj)
            objects.append(obj)
        
        '''Population Replacement'''
        while len(objects) < len(range(pop)):
            wingspan = r.uniform(min(wings)*1, max(wings)*1)
            batteries = r.randint(min(bat), max(bat))
            motor_num = r.randint(0, len(keepers)-1)
            motor = keepers[motor_num].motor
            motor_num = keepers[motor_num].motor_num
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
                objects[u].motor = keepers[r.randint(0, len(keepers)-1)].motor
                objects[u].alpha = r.randint(0,40)/4
                objects[u].throttle = r.randint(1,len(objects[u].motor)-1)
                
                mutants.append(objects[u])
                # record.append(objects[u])
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
          # if objects[w].lift >= objects[w].mass * 1.35:
          #     i = r.randint(1,2)
          #     if i == 1:
          #         while objects[w].lift >= objects[w].mass * 1.35:
          #             objects[w].wingspan = objects[w].wingspan * 0.99
          #             objects[w].chord_length = objects[w].chord_length * 0.99
          #             objects[w].calc_lift()
          #     elif i == 2:
          #         while objects[w].lift >= objects[w].mass * 1.35:
          #             objects[w].alpha = objects[w].alpha - 0.25
          #             objects[w].calc_lift()
              # elif i == 3:
              #     while objects[w].lift >= objects[w].mass * 1.05:
              #         objects[w].cruise_velocity = objects[w].cruise_velocity * 0.99
              #         objects[w].calc_lift()
            
        e = e + 1
    
    '''Plotting'''
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
        all_wingspans.append(record[f].wingspan)
        all_end.append(record[f].endurance)
        all_range.append(record[f].range/1000)
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
        mutant_range.append(all_mutants[z].range/1000)
        mutant_mass.append(all_mutants[z].mass)
        mutant_lift.append(all_mutants[z].lift)
        mutant_vel.append(all_mutants[z].cruise_velocity)
        mutant_stall_speed.append(all_mutants[z].stall_speed)
    
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
    #
    final_wing = np.mean(keepers[-1].wingspan)
    final_bat = pure[-1].batteries
    final_motor = pure[-1].motor
    final_alpha = pure[-1].alpha
    final = Plane(wingspan=final_wing,batteries=final_bat,motor=final_motor,alpha=final_alpha)
    final.wingspan = round(final.wingspan,3)
    final.chord_length = round(final.chord_length,3)
    final.fuse_diam = round(final.fuse_diam,3)
    final.fuse_length = round(final.fuse_length,3)
    final.calc_mass()
    final.calc_endurance()
    final.calc_range()
    final.calc_lift()
    final.calc_vtail_lift()
    final.calc_drag()
    final.calc_velocity()


    # 
    '''plot'''
    fig = plt.figure(7)
    plt.scatter(all_end,all_range, marker = ".", label="Solutions")
    # plt.scatter(mutant_end,mutant_range, marker = ".", label="Mutants")
    plt.scatter(final.endurance, final.range/1000, label="Final")
    plt.legend()
    plt.title("Performance Curve Comparison")
    plt.xlabel("Endurance (Hours)")
    plt.ylabel("Range (Km)")
    plt.show()
    
    fig = plt.figure(8)
    plt.scatter(all_drag,all_lift, marker = ".", label="Solutions")
    # plt.scatter(mutant_end,mutant_range, marker = ".", label="Mutants")
    plt.scatter(final.drag, final.lift, label="Final")
    plt.legend()
    plt.title("Performance Curve Comparison")
    plt.xlabel("Drag (Kg)")
    plt.ylabel("Lift (Kg)")
    plt.show()
    
    fig = plt.figure(9)
    plt.subplot(2, 1,1)
    plt.scatter(Plane.naca2412['Alpha'],Plane.naca2412['CL'], marker = ".", label="CL")
    plt.ylabel("CL")
    plt.subplot(2, 1,2)
    plt.scatter(Plane.naca2412['Alpha'],Plane.naca2412['CD'], marker='.',label="CD")
    # plt.scatter(Plane.naca2412['Alpha'],(Plane.naca2412['CL']/Plane.naca2412['CD']), marker='.',label="L/D")
    # plt.legend()
    plt.title("CD and CL w/ respect to alpha")
    plt.xlabel("Alpha")
    plt.ylabel("CD")
    plt.show()
    # 
    return final
