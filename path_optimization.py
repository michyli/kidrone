from path_generation import *

class Path:
    """
    Path class processes the path object and extracts information about the path.
    """
    def __init__(self, path):
        """      
        path: a list of LineStrings. Usually the output of generate_path() function
        """
        self.path = path
        self.length = sum([i.length for i in self.path])
    
    def air_time(self):
        """Returns the projected air time when executing the given path
        
        Parameters used:
        1) Dispersing velocity:                         100km/h
        2) Max non-dispersing velocity:                 200km/h
        3) Turning velocity:                             50km/h
        4) Min. acceleration / Deceleration distance:   0.1km (100m)
        5) Acceleration / Deceleration:                 Linear
        """
        airtime = 0
        
        return airtime
        
    def offset_path(self, wind_dir, height, seed_weight):
        """Returns an offsetted path based on the wind direction, drone height, and seed weight.
        
        wind_dir:       a tuple containing the x and y components of the wind vector
        height:         constant height the drone aims to travel at (m)
        seed_weight:    weight of the seed (kg)
        """
        

