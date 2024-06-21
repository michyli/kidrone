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
    def __init__(self, line, parent, prev_velo=None, curr_velo=None, next_velo=None):
        """
        line: a LineString object that contains the coordinates of the line
        parent: the parent Path object 'line' belongs to
        prev_velo: a float that indicates the velocity of the previous Segment in the Path
        curr_velo: a float that indicates the velocity of the current Segment (self) in the Path
        next_velo : a float that indicates the velocity of the next Segment in the Path
        """
        self.line = line
        self.parent = parent
        self.prev_velo = prev_velo
        self.curr_velo = curr_velo
        self.next_velo = next_velo
        
        self.length = linestring_dist(line)
        
    @property
    def velo(self):
        if len(self.parent.parent.intersection(self.line)) == 2:
            pass
        
    def time(self):
        """Gives the time it takes to cover this path, with acceleration / deceleration taken into consideration 
        """
        