import numpy as np
from shapely.geometry import LineString, Point, LinearRing, MultiPoint, Polygon
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
    def curr_velo(self):
        """Determines the max velocity of the Segment within the Path within the Polygon.
        Note that lines that connects the swath are not dispersing lines.
        """
        if line_slope(self.line) != self.parent.swath_slope:
            #If the slope doesn't match the swath slope, then the line is a intermediate line that connects the swath, hence not a dispersing line.
            return self.parent.nondisp_velo
        if not self.parent.parent.polygon.contains(self.line):
            #If the line isn't inside the polygon, the the line isn't a dispersing line
            return self.parent.nondisp_velo
        if self.parent.parent.children:
            if any([c.contains(self.line) for c in self.parent.parent.children]):
                return self.parent.nondisp_velo
        return self.parent.disp_velo
    
    def time(self):
        """Gives the time it takes to cover this path, with acceleration / deceleration taken into consideration 
        """
        if any([self.prev_velo, self.curr_velo, self.next_velo]):
            raise ValueError("all velocities need to be assigned before time can be determined.")
        
        #Starting and ending velocity of this segment, assuming half of acc/deceleration are performed in this segment, and acceleration is linear
        seg_start_velo = (self.prev_velo + self.curr_velo) / 2
        seg_end_velo = (self.next_velo + self.curr_velo) / 2
        
        start_acc_time = (self.curr_velo ** 2 - seg_start_velo ** 2) / (2 * self.parent.turn_dist)
        end_acc_time = (seg_end_velo ** 2 - self.curr_velo ** 2) / (2 * self.parent.turn_dist)
        const_velo_time = (self.length - (2 * self.parent.turn_dist)) / self.curr_velo
        
        return start_acc_time + end_acc_time + const_velo_time