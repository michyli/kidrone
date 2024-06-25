import numpy as np
from shapely.geometry import LineString, Point, LinearRing, MultiPoint, Polygon
from segment import *

class Path:
    """
    Path class processes the path object and extracts information about the path.
    """
    def __init__(self, path, parent, swath_slope, start_velo=0, end_velo=0):
        """      
        path:   a list of LineStrings. Usually the output of generate_path() function
        parent: the polygon object the path belongs to
        """
        self.path = path
        self.parent = parent
        self.swath_slope = swath_slope
        
        #Assuming drone starts from and ends on static
        self.start_velo = start_velo #KM/h
        self.end_velo = end_velo #KM/h
        
        """
        Parameters used:
        1) Dispersing velocity:                         100km/h
        2) Max non-dispersing velocity:                 200km/h
        3) Turning velocity (90deg):                    50km/h
            *Scales linearly with angle
        4) Min. acceleration / Deceleration distance:   0.1km (100m)
        5) Acceleration / Deceleration:                 Linear
        """
        self.disp_velo = 100 #KM/h
        self.nondisp_velo = 200 #KM/h
        self.turn_velo = 50 #KM/h
        self.turn_dist = 0.1 #KM, minimum distance for drone to accelerate or decelerate to disp_velo
        self.acc = self.turn_dist / (self.nondisp_velo - self.disp_velo) #KM/h^2
        self.dec = self.turn_dist / (self.turn_velo - self.disp_velo) #KM/h^2
        
    def offset_path(self, wind_dir, height, seed_weight):
        """Returns an offsetted path based on the wind direction, drone height, and seed weight.
        
        wind_dir:       a tuple containing the x and y components of the wind vector
        height:         constant height the drone aims to travel at (m)
        seed_weight:    weight of the seed (kg)
        """
        #TODO: need to be completed
        pass
        
    @property
    def pathlength(self):
        """Returns the length of path in KM
        Note that the point coordinates in self.path are in unit of longtitude and latitude.
        """
        return sum([linestring_dist(line) for line in self.path])
    
    def airtime(self):
        """Returns the projected air time when executing the given path"""
        #construct all lines in path into Segment object
        airtime_list = [Segment(line, self) for line in self.path]
        #Set starting and ending velocity
        airtime_list[0].prev_velo = self.start_velo
        airtime_list[-1].next_velo = self.end_velo

        #Assign prev and next velocities to all Segment objects
        for i in range(len(airtime_list)):
            if i != 0 and i != len(airtime_list):
                airtime_list[i].prev_velo = airtime_list[i-1].curr_velo
                airtime_list[i].next_velo = airtime_list[i+1].curr_velo  

        return sum([seg.time for seg in airtime_list])      
        
    
    
