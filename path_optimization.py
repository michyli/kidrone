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
    
    def length(self):
        """Returns the length of path in KM
        Note that the point coordinates in self.path are in unit of longtitude and latitude.
        
        The more accurate calculation involves Haversin Formula.
        But for the purpose here, a rough estimate is sufficient.
        """
        length = []
        for line in self.path:
            # 1° of latitude is always 111.32 km
            dx = (line.coords[1][0] - line.coords[0][0]) * 111.32
            # 1° of longitude is 40075 km * cos(latitude) / 360
            dy = 40075 * np.cos((line.coords[1][1] - line.coords[0][1])) / 360
            length.append(np.sqrt(dx**2 + dy**2))
        return round(sum(length), 5)
    
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
        pass