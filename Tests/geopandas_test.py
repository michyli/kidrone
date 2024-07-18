import geopandas as gpd
import sys
import os
from src.basic_functions import *
from src.optimization import *
from shapely.geometry import LineString

# Add the src directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Example shapefile path
shapefile_path = r"C:\Users\edwar\OneDrive\Desktop\Kidrone\2023 Canfor Projects\CBK0035 PU1\Site Shapefiles - Fall\CBK0035_PU1.shp"
# # Read shapefile into a GeoDataFrame
# gdf = gpd.read_file(shapefile_path)

# # Print the CRS
# print("CRS:", gdf.crs)
# print("\n")

# print(gdf)
# #Get all the geometries in the geometry column
# geometries = gdf['geometry']

# #For each geometry make a list to store it's polygons
# #Each element in the list is a list of polygons, representing the polygons of a geo
# geo_poly_list = []
# for geo in geometries:
#     polygons = extractPolygons(geo)
#     geo_poly_list.append(polygons)


# #For each polygon extract the coordinates
# coordinates = []
# for poly_list in geo_poly_list:
#     for polygon in poly_list:
#         coordinates.append(extract_coords(polygon))


extractedCoords = shp2coords(shapefile_path)
print(extractedCoords)

bestPathList = []
for polygon in extractedCoords:
    optimal_func = airtime_coverage_weighted(75, 15, 10)                                    #75:15:10 weighting between airtime:seeding_percentage:spilling
    pathlist, pathlistruntime = construct_pathlist(polygon, 20, children=None, poly_offset=0, num_path=10) #calculates the optimized path
    datatable, best_path = find_best_path(pathlist, optimal_func)
    showpath(best_path)
    bestPathList.append(best_path.path)

print(bestPathList)

#Test extraction

gdf = gpd.GeoDataFrame(geometry=bestPathList[0])
gdf.set_crs(epsg=3857, inplace=True)

output_directory = r"shp_output"
output_file = os.path.join(output_directory, "best_path.shp")
gdf.to_file(output_file)
