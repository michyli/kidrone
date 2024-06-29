from optimization import *

"""
=====================
====== Testing ======
=====================
"""

""" lake1 =[[-119.3234427, 47.6949743],
            [-119.3014756, 47.349989],
            [-118.9774616, 47.52462],
            [-119.3069674, 47.6949743]] """
  

points = csv2coords("coordinates.csv")
pathlist = path_list_constructor(points, 100)
optimized_path = optimizer(pathlist, shortest_airtime())
showpath(optimized_path)