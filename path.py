import numpy as np
from shapely.geometry import LineString, Point, LinearRing, MultiPoint, Polygon
from segment import *

class Path:
    """
    Path class processes the path object and extracts information about the path.
    """
    def __init__(self, path: list[LineString], parent, swath_slope, start_velo=0, end_velo=0, _disp_map=[], _pathlength=None, _airtime=None):
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
        
        #@property definition
        self.disp_map = _disp_map
        self.pathlength = _pathlength
        self.airtime = _airtime
        
    def offset_path(self, wind_dir, height, seed_weight):
        """Returns an offsetted path based on the wind direction, drone height, and seed weight.
        
        wind_dir:       a tuple containing the x and y components of the wind vector
        height:         constant height the drone aims to travel at (m)
        seed_weight:    weight of the seed (kg)
        """
        #TODO: need to be completed
        pass
        
    @property
    def disp_map(self):
        return self._disp_map
    
    @disp_map.setter
    def disp_map(self, value):
        """Determines the max velocity of each corresponding Segment within the Path within the Polygon.
        Note that lines that connects the swath are not dispersing lines.
        """
        map = []
        for line in self.path:
            print(np.isclose(line_slope(line), self.swath_slope, rtol=1e-05, atol=1e-08, equal_nan=False))
            if not np.isclose(line_slope(line), self.swath_slope, rtol=1e-05, atol=1e-08, equal_nan=False):
            #If the slope doesn't match the swath slope, then the line is a intermediate line that connects the swath, hence not a dispersing line.
                map.append(False)
            elif not self.parent.polygon.contains(line):
                #If the line isn't inside the polygon, then the line isn't a dispersing line
                map.append(False)
            elif self.parent.children:
                #If the line is inside of any internal polygons (e.g. lakes), then the line isn't a dispersing line
                if any([c.contains(line) for c in self.parent.children]):
                    map.append(False)
            else:
                map.append(True)
                
        self._disp_map = map
        
    @property
    def pathlength(self):
        return self.__pathlength
    
    @pathlength.setter
    def pathlength(self, value):
        """Returns the length of path in KM
        Note that the point coordinates in self.path are in unit of longtitude and latitude.
        """
        self.__pathlength = sum([linestring_dist(line) for line in self.path])
    
    @property
    def airtime(self):
        return self.__airtime
    
    @airtime.setter
    def airtime(self, value):
        """Returns the projected air time when executing the given path"""
        def mapper(index):
            return self.disp_velo if self.disp_map[index] else self.nondisp_velo
        
        #Construct each LineString into Segment instances
        airtime_list = []
        for index, line in enumerate(self.path):
            if index == 0:
                airtime_list.append(Segment(line, self, self.start_velo, mapper(index), mapper(index+1)))
            elif index == len(self.path) - 1:
                airtime_list.append(Segment(line, self, mapper(index-1), mapper(index), self.end_velo))
            else:
                airtime_list.append(Segment(line, self, mapper(index-1), mapper(index), mapper(index+1)))

        self.__airtime = sum([seg.time for seg in airtime_list])   
    
