import numpy as np
from shapely.geometry import LineString, Point, LinearRing, MultiPoint
from segment import *

class Path:
    """
    Path class processes the path object and extracts information about the path.
    """
    def __init__(self, path, parent, start_velo=0, end_velo=0):
        """      
        path:   a list of LineStrings. Usually the output of generate_path() function
        parent: the polygon object the path belongs to
        """
        self.path = path
        self.parent = parent
        
        #Assuming drone starts from and ends on static
        self.start_velo = start_velo #KM/h
        self.end_velo = end_velo #KM/h
    
    def pathlength(self):
        """Returns the length of path in KM
        Note that the point coordinates in self.path are in unit of longtitude and latitude.
        """
        return sum([linestring_dist(line) for line in self.path])
    
    def airtime(self):
        """Returns the projected air time when executing the given path"""
        airtime_list = []
        #construct all lines in path into Segment object
        """ for index, line in enumerate(self.path):
            airtime_list.append(Segment(line, self, self.start_velo, self.path[]))
              """
        return airtime_list
        
    def offset_path(self, wind_dir, height, seed_weight):
        """Returns an offsetted path based on the wind direction, drone height, and seed weight.
        
        wind_dir:       a tuple containing the x and y components of the wind vector
        height:         constant height the drone aims to travel at (m)
        seed_weight:    weight of the seed (kg)
        """
        pass
    
    
