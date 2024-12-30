# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 13:56:06 2024

@author: brigg
"""

from Plane_Class import Plane
import random as r
import matplotlib.pyplot as plt

'''Initial Population Creation'''
record = []
objects = []
pop = 10
for i in range(pop):
    obj = Plane(wingspan=r.uniform(1,3),batteries=r.randint(1, 4),motor=Plane.motors[r.randint(0, 3)])
    objects.append(obj)

e = 1
while e < 5:     
    for g in range(pop):
        # obj = Plane(wingspan=r.uniform(1,3),batteries=r.randint(1, 4),motor=Plane.motors[r.randint(0, 3)])
        objects[g].calc_mass()
        objects[g].calc_endurance()
        objects[g].calc_range()
        objects[g].calc_lift()
        objects[g].calc_vtail_lift()
        objects[g].calc_drag()
        objects[g].calc_velocity()
        # objects.append(obj)
        record.append(objects[g])
        
    '''Evaluation'''
    total_mass = 0
    total_wingspan = 0
    total_vel = 0
    mass_score  = []
    wingspan_score = []
    vel_score = []
    for j in range(pop):
        total_mass = total_mass + (objects[j].mass)
        total_wingspan = total_wingspan + (objects[j].wingspan)
        total_vel = total_vel + objects[j].cruise_velocity
    for u in range(pop):
        mass_score.append(objects[u].mass/total_mass)
        wingspan_score.append(objects[u].wingspan/total_wingspan)
        vel_score.append(objects[u].cruise_velocity/total_vel)
            
    '''Fitness Function'''
    #Weighted fitness function, allows for the user to specify priorities
    #This is in contrast to prioritizing a single metric and moving the rest to constraints
    score = []
    for k in range(pop):
        score.append((1)*mass_score[k] + (10)*vel_score[k] + (3)*wingspan_score[k])
        
    '''Selection'''
    average_score = sum(score)/pop
    keepers = []
    #Keeping indivisual sizes for later use
    wings = []
    bat = []
    motors = []
    
    for n in range(pop):
        if score[n] < average_score:
            keepers.append(objects[n])
            
    for h in range(len(keepers)):
        wings.append(keepers[h].wingspan)
        bat.append(keepers[h].batteries)
        motors.append(keepers[h].motor)

    '''Crossover'''
    #Uniform crossover pattern, each chromasom is crossed over
    objects = []
    crossover = []
    for p in range(len(keepers)):
        wingspan = keepers[r.randint(0, len(keepers)-1)].wingspan
        batteries = keepers[r.randint(0, len(keepers)-1)].batteries
        motor = keepers[r.randint(0, len(keepers)-1)].motor
        obj = Plane(wingspan=wingspan,batteries=batteries,motor=motor)
        crossover.append(obj)
        objects.append(obj)
    
    '''Mutation'''
    mutants = []
    for u in range(len(crossover)):
        if r.randint(1, 10) > 8:
            crossover[u].wingspan = r.uniform(1, 3)
            crossover[u].batteries = r.randint(1, 4)
            crossover[u].motor = keepers[r.randint(0, len(keepers)-1)].motor
            mutants.append(crossover[u])
            record.append(obj)

    for y in range(len(mutants)):
        objects.append(mutants[y])
    
    '''Population Replacement'''
    while len(objects) < len(range(pop)):
        wingspan = r.uniform(min(wings)*1, max(wings)*1)
        batteries = r.randint(min(bat), max(bat))
        motor = keepers[r.randint(0, len(keepers)-1)].motor
        obj = Plane(wingspan=wingspan,batteries=batteries,motor=motor)
        objects.append(obj)
        record.append(obj)
        
    '''Additional Calculations'''
    # for w in range(len(objects)):
    #     objects[w].calc_mass()
    #     objects[w].calc_endurance()
    #     objects[w].calc_range()
    #     objects[w].calc_lift()
    #     objects[w].calc_vtail_lift()
    #     objects[w].calc_drag()
    #     objects[w].calc_velocity()
        
    e = e + 1

'''Plotting'''
all_wingspans = []
all_mass = []
all_vel = []
all_endur = []
all_range = []
for f in range(len(record)):
    all_wingspans.append(record[f].wingspan)

plt.scatter(range(len(all_wingspans)),all_wingspans)
plt.show()