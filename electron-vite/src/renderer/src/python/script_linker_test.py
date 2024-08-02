import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import sys
import time
import geopandas as gpd
from src.basic_functions import *


# Example shapefile path
shapefile_path = r"C:\Users\edwar\OneDrive\Desktop\Kidrone\2023 Canfor Projects\CBK0035 PU1\Site Shapefiles - Fall\CBK0035_PU1.shp"

readData = sys.stdin.read()

print(readData)
time.sleep(2)
print("test 1")
time.sleep(2)
print("test 2")
# print(shp2coords(shapefile_path))

