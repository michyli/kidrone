import os
from arcgis.features import GeoAccessor, GeoSeriesAccessor, FeatureLayer
import pandas as pd

# Path to the shapefile directory
shapefile_path = r"C:\Users\edwar\OneDrive\Desktop\Kidrone\2023 Canfor Projects\CBK0035 PU1\Site Shapefiles - Winter\KiDrone Seeding 2024_Cranbrook_CBK0035-pu1_Secondary Data.shp"

# Read the shapefile into a Spatial DataFrame
sdf = pd.DataFrame.spatial.from_featureclass(shapefile_path)

# # Create a FeatureLayer object
# feature_layer = FeatureLayer(shapefile_path)
# # Access the spatial reference information
# spatial_reference = feature_layer.properties.extent.spatialReference
# # Print the spatial reference information
# print(spatial_reference)

# Print the first few rows of the Spatial DataFrame
print(sdf)

# Access geometry and attributes
print(sdf.spatial.geometry_type)
print(sdf.columns)
