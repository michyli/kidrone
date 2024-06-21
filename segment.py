import numpy as np
from shapely.geometry import LineString, Point, LinearRing, MultiPoint
from basic_functions import *

class Segment:
    """
    A Segment object contains information about a segment of a path, and stores the velocity at which
    the drone will be traveling the current, previous, and next path in.
    
    This stored information is necessary to calculate airtime as there will be an acceleration / deceleration
    curve at the start and end of each path.
    """
    def __init__(self, line, parent, prev_velo=None, next_velo=None):
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
        self.acc = 0.1/100 #KM/h^2
        self.dec = - self.acc #KM/h^2
        """
        line: a LineString object that contains the coordinates of the line
        parent: the parent Path object 'line' belongs to
        prev_velo: a float that indicates the velocity of the previous Segment in the Path
        next_velo : a float that indicates the velocity of the next Segment in the Path
        """
        self.line = line
        self.parent = parent
        self.prev_velo = prev_velo
        self.next_velo = next_velo
        
    @property
    def velo(self):
        if len(self.parent.parent.intersection(self.line)) == 2:
            pass
        
    def time(self):
        """Gives the time it takes to cover this path, with acceleration / deceleration taken into consideration 
        """
        pass