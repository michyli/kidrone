from src.optimization import *

"""
=====================
====== Testing ======
=====================
"""

""" lake1 =[[-119.3234427, 47.6949743],
            [-119.3014756, 47.349989],
            [-118.9774616, 47.52462],
            [-119.3069674, 47.6949743]] """

shapefile_path = r"2023 Canfor Projects\CBK0035 PU1\Site Shapefiles - Fall\CBK0035_PU1.shp"
# extract coords from test_coordinates.csv file
points = csv2coords("test_coordinates.csv")
# points = shp2coords(shapefile_path)[0]

disp_diam = 50  # meters

best_path, runtime = construct_best_path(
    points, disp_diam)  # calculates the optimized path
# print(f"runtime is {runtime}")
showpath(best_path)  # show the optimized path
