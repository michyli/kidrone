from src.optimization import *
import time

"""
=====================
====== Testing ======
=====================
"""
print()
#extract coords from test_coordinates.csv file
points = csv2coords("test_coordinates.csv")
#Define an example of exclusion area
exclude1 =[[-79.4682806,43.6477834],
        [-79.4683807,43.6456511],
        [-79.466307,43.6427836],
        [-79.4634324,43.6451749],
        [-79.4642476,43.6479697],
        [-79.4682806,43.6477834]]
exclude1 = Outline('child1', gcs2pcs_batch(exclude1))

disp_diam = 10 #meters

shapefile_path = r"C:\Users\edwar\Downloads\Shapefile With Bars\KiDrone Seeding_CBK0035-pu1_GHTE.shp"
points = shp2coords(shapefile_path)[0]
print(points)


optimal_func = airtime_coverage_weighted(75, 15, 10)                                    #75:15:10 weighting between airtime:seeding_percentage:spilling
pathlist, pathlistruntime = construct_pathlist(points, disp_diam, children=None, num_path=10) #calculates the optimized path
datatable, best_path = find_best_path(pathlist, optimal_func)

#print(datatable)                       #Prints the pandas DataFrame for all paths ran (all data values are max-min normalized)
#showpath(best_path)                     #Display the highest-scored path
show3Dpath(best_path, "coarse", gif=True)          #Plot in 3D with respect to elevation #*(This is where it takes the longest)
                                        #Change "dense" to "coarse" to run faster with less accuracy in height

print(f"Pathlist construction runtime: {round(pathlistruntime, 3)}sec")

