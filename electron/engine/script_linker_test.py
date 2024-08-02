import sys
import time
import geopandas as gpd
from basic_functions import *
from optimization import * 

#Reference
# var settingsValues = new Map([
#     ["dispersionDiameter", undefined],
#     ["dispersionVelocity", undefined],
#     ["nondispersionVelocity", undefined],
#     ["acceleration", undefined],
#     ["minimumCoverage", undefined],
#     ["windDirection", undefined],
#     ["windVelocity", undefined]
# ]);

# Example shapefile path
shapefile_path = r"C:\Users\edwar\OneDrive\Desktop\Kidrone\2023 Canfor Projects\CBK0035 PU1\Site Shapefiles - Fall\CBK0035_PU1.shp"

#Get data from javascript, should be dict rn
readData = sys.stdin.read() 
print(readData)
sys.stdout.flush()

# # Construct the best path and measure runtime
# optimal_func = airtime_coverage_weighted(100, 0, 0)
# pathlist, pathlistruntime = construct_pathlist(
#     polygon, disp_diam, children=None, poly_offset=0, num_path=10)  # calculates the optimized path
# datatable, best_path = find_best_path(pathlist, optimal_func)




