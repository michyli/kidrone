from src.optimization import *

"""
=====================
====== Testing ======
=====================
"""

lake1 =[[-79.4682806,43.6477834],
        [-79.4683807,43.6456511],
        [-79.466307,43.6427836],
        [-79.4634324,43.6451749],
        [-79.4642476,43.6479697],
        [-79.4682806,43.6477834]]

shapefile_path = r"2023 Canfor Projects\CBK0035 PU1\Site Shapefiles - Fall\CBK0035_PU1.shp"
#extract coords from test_coordinates.csv file
points = csv2coords("test_coordinates.csv")
#points = shp2coords(shapefile_path)[0]
disp_diam = 50 #meters

lake1 = gcs2pcs_batch(lake1)
lake1 = Outline('child1', lake1)

best_path, runtime = construct_best_path(
    points, disp_diam, lake1)  # calculates the optimized path
# print(f"runtime is {runtime}")
print(f"runtime: {round(runtime, 3)}sec")
showpath(best_path)  # show the optimized path
