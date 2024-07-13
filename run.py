from src.optimization import *

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

optimal_func = airtime_coverage_weighted(75, 15, 10)
pathlist, runtime = construct_pathlist(points, disp_diam, exclude1)  # calculates the optimized path
datatable, best_path = find_best_path(pathlist, optimal_func)

showpath(best_path)
print(datatable)
print(f"Algorithm runtime: {round(runtime, 3)}sec")
#showpath(best_path)  # show the optimized path