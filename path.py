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
        self.default_turn_velo = 50 #%, max percentage of current velocity the drone can travel when performing a 90 degree turn
        self.turn_dist = 0.1 #KM, minimum distance for drone to accelerate or decelerate to disp_velo
        
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
            if not np.isclose(line_slope(line), self.swath_slope, rtol=1e-05, atol=1e-08, equal_nan=False):
            #If the slope doesn't match the swath slope, then the line is a intermediate line that connects the swath, hence not a dispersing line.
                map.append(False)
            elif not self.parent.polygon.buffer(1e-8).contains(line):
                #If the line isn't inside the polygon, then the line isn't a dispersing line
                #Note that .buffer is used to account for Python rounding error
                map.append(False)
            elif self.parent.children:
                #If the line is inside of any internal polygons (e.g. lakes), then the line isn't a dispersing line
                if any([c.buffer(1e-8).contains(line) for c in self.parent.children]):
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
        """Returns the projected airtime when executing the given path"""
        def mapper(index):
            """Returns the velocity of the segment depending on whether 
            the number 'index' path in self.path is a dispersing of non-dispersing path.
            """
            return self.disp_velo if self.disp_map[index] else self.nondisp_velo
                
        def angle_to_velo(line1, line2, velo1):
            """Returns the turning velocity given two consecutive LineStrings
            Assuming linear acc/deceleration -> Drone slows down to self.default_turn_velo if turning 90 degrees,
            and fully stops if turning 180 degrees. Assume acc/deceleration as a linear function in between.
            
            velo1: velocity of the drone before changing travel direction
            """
            delta_angle = line_angle(line1, line2)-90
            if delta_angle == 90:
                return self.default_turn_velo
            if delta_angle > 90:
                return velo1 * self.default_turn_velo + (delta_angle-90) * ((velo1 - velo1 * self.default_turn_velo) / 90)
            if delta_angle < 90:
                return velo1 * self.default_turn_velo + (delta_angle-90) * ((velo1 * self.default_turn_velo) / 90)
        
        #Construct each LineString into Segment instances
        airtime_list = []
        for index, line in enumerate(self.path):
            if index == 0:
                #define the first line of the path
                airtime_list.append(Segment(self.path[0], self, self.start_velo, mapper(0), angle_to_velo(self.path[0], self.path[1], mapper(0))))
                continue
            if index == len(self.path)-1:
                #define the last line of the path
                airtime_list.append(Segment(self.path[-1], self, angle_to_velo(self.path[-2], self.path[-1], mapper(-2)), mapper(-1), self.end_velo))
                continue
            start_turn_velo = angle_to_velo(self.path[index-1], line, mapper(index-1))
            end_turn_velo = angle_to_velo(line, self.path[index+1], mapper(index))
            airtime_list.append(Segment(line, self, start_turn_velo, mapper(index), end_turn_velo))

        tot_hour = sum([seg.time for seg in airtime_list])
        
        self.__airtime = tot_hour
    
    def airtime_disp(self):
        time_disp = disp_time(self.airtime)
        print(time_disp)