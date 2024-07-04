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
  

""" points = csv2coords("test_coordinates.csv")                 #extract coords from test_coordinates.csv file
disp_diam = 10                                              #meters

pathlist, runtime = path_list_constructor(points, disp_diam)#construct a list of path to iterate over
print(f"runtime is {runtime}") 
optimized_path = optimizer(pathlist, shortest_airtime())    #calculates the optimized path
showpath(optimized_path)                                    #show the optimized path
 """


p1 = (0, 0)
p2 = (0, 1000)
p3 = (1000, 1000)
p4 = (1000, 0)
p5 = (0, 0)
points = [p1, p2, p3, p4, p5]
new_points = pcs2gcs_batch(points)
outline = Outline('test', new_points)
path = outline.swath_gen(10, 0)


