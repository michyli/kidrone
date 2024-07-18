from src.optimization import *
import time
import os

"""
=====================
====== Testing ======
=====================
"""
points = gcs2pcs_batch(csv2coords("coordinates.csv"))

# Define examples of exclusion area
exclude1 = Outline('child1', gcs2pcs_batch(csv2coords("exclusion1.csv")))
exclude2 = Outline('child2', gcs2pcs_batch(csv2coords("exclusion2.csv")))

disp_diam = 40  # meters



optimal_func = airtime_coverage_weighted(75, 15, 10)                                    #75:15:10 weighting between airtime:seeding_percentage:spilling
pathlist, pathlistruntime = construct_pathlist(points, disp_diam, children=[exclude1], 
                                                poly_offset=0, num_path=10)             #calculates the optimized path
datatable, best_path = find_best_path(pathlist, optimal_func)

#print(datatable)                                                               #Prints the pandas DataFrame for all paths ran (all data values are max-min normalized)
#showpath(best_path)                                                            #Display the highest-scored path
show3Dpath(best_path, height_offset=60, plottype="dense", gif=True)             #Plot in 3D with respect to elevation #*(This is where it takes the longest)
                                                                                #Change "dense" to "coarse" to run faster with less accuracy in height

print(f"Pathlist construction runtime: {round(pathlistruntime, 3)}sec")
