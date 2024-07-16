import geopandas as gpd
from src.basic_functions import *

# Example shapefile path
shapefile_path = r"C:\Users\edwar\Downloads\Shapefile With Points\KiDrone Seeding_CBK0035-pu1_Secondary Data.shp"
# # Read shapefile into a GeoDataFrame
# gdf = gpd.read_file(shapefile_path)

# # Print the CRS
# print("CRS:", gdf.crs)
# print("\n")

# # print("gdf", gdf)
# # Get all the geometries in the geometry column
# geometries = gdf['geometry']

# # For each geometry make a list to store it's polygons
# # Each element in the list is a list of polygons, representing the polygons of a geo
# geo_poly_list = []
# for geo in geometries:
#     polygons = extractPolygons(geo)
#     geo_poly_list.append(polygons)


# # For each polygon extract the coordinates
# coordinates = []
# for poly_list in geo_poly_list:
#     for polygon in poly_list:
#         coordinates.append(extract_coords(polygon))

print(shp2coords(shapefile_path))
