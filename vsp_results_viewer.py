import pandas as pd
import csv
import numpy as np
def vsp_results_viewer():
    num_wakes=5
    with open('Results.csv', 'r') as infile:
        reader = csv.reader(infile)
        CL = []
        CD = []
        LD = []
        Alpha = []
        # read each row, save it if it has valuable information
        for row in reader:
            if row[0] == 'CLi' and len(row) == 6:
                CL.append(round((float(row[1])+float(row[2])+float(row[3])+float(row[4])+float(row[5]))/num_wakes,7))
            if row[0] == 'CDtot' and len(row) == 6:
                CD.append(round((float(row[1])+float(row[2])+float(row[3])+float(row[4])+float(row[5]))/num_wakes,7))
            if row[0] == 'L/D' and len(row) == 6:
                LD.append(round((float(row[1])+float(row[2])+float(row[3])+float(row[4])+float(row[5]))/num_wakes,7))
            if row[0] == 'Alpha' and len(row) == 6:
                Alpha.append((float(row[1])+float(row[2])+float(row[3])+float(row[4])+float(row[5]))/num_wakes)
    return(CL,CD,LD,Alpha)