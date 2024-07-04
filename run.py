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
  
shapefile_path = r"C:\Users\edwar\OneDrive\Desktop\Kidrone\2023 Canfor Projects\CBK0035 PU1\Site Shapefiles - Fall\CBK0035_PU1.shp"
points = csv2coords("test_coordinates.csv")                 #extract coords from test_coordinates.csv file
points = shp2coords(shapefile_path)[0]

disp_diam = 50                                              #meters

pathlist, runtime = path_list_constructor(points, disp_diam)#construct a list of path to iterate over
print(f"runtime is {runtime}")
optimized_path = optimizer(pathlist, shortest_airtime())    #calculates the optimized path
showpath(optimized_path)                                    #show the optimized path




