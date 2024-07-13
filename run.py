from src.optimization import *
import time

"""
=====================
====== Testing ======
=====================
"""

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

disp_diam = 50 #meters

shapefile_path = r"2023 Canfor Projects\CBK0035 PU1\Site Shapefiles - Fall\CBK0035_PU1.shp"
#points = shp2coords(shapefile_path)[0]

#75:15:10 weighting between airtime:seeding_percentage:spilling
optimal_func = airtime_coverage_weighted(75, 15, 10)
pathlist, pathlistruntime = construct_pathlist(points, disp_diam, exclude1, num_path=1)  # calculates the optimized path
#datatable is a DataFrame with all considered paths and their scores. Note that all numbers are min-max normalized
datatable, best_path = find_best_path(pathlist, optimal_func)

print(datatable)
showpath(best_path)
show3Dpath(best_path, "dense")

print(f"Pathlist construction runtime: {round(pathlistruntime, 3)}sec")