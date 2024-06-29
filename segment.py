from basic_functions import *

class Segment:
    """
    A Segment object contains information about a segment of a path, and stores the velocity at which
    the drone will be traveling the current, previous, and next path in.
    
    This stored information is necessary to calculate airtime as there will be an acceleration / deceleration
    curve at the start and end of each path.
    """
    def __init__(self, line, parent, prev_velo=None, curr_velo=None, next_velo=None, prev_angle=None, next_angle=None):
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
        self.prev_angle = prev_angle
        self.next_angle = next_angle
        self.start_velo = self.start_velo_setter()
        self.end_velo = self.end_velo_setter()
        
        
        self.length = line.length / 1000 #KM

        self.time = self.time_setter() #hours
    
    """
    ========================
    === Attribute Setter ===
    ========================    
    """
    def start_velo_setter(self):
        #determine starting velocity of the initial acc/deeleration
        if self.prev_angle:
            init_velo = (self.prev_velo + self.curr_velo) / 2 if self.prev_angle <= 90 else 0
        else:
            init_velo = self.prev_velo
        return init_velo
        
    def end_velo_setter(self):
        #determine ending velocity of the initial acc/deeleration
        if self.next_angle:
            end_velo = (self.curr_velo + self.next_velo) / 2 if self.next_angle <= 90 else 0
        else:
            end_velo = self.next_velo
        return end_velo

    def time_setter(self):
        """Gives the time it takes to cover this path, with acceleration / deceleration taken into consideration """
        #double check if all velocities are assigned
        if any(i is None for i in [self.prev_velo, self.curr_velo, self.next_velo]):
            raise ValueError("all velocities need to be assigned before time can be determined.")
        
        if self.length > 2 * self.parent.turn_dist:
            #determine the acc/deceleration time
            init_time = (2 * self.parent.turn_dist) / (self.start_velo + self.curr_velo)
            end_time = (2 * self.parent.turn_dist) / (self.curr_velo + self.end_velo)
            #determine constant velocity time
            curr_time = (self.length - 2 * self.parent.turn_dist) / self.curr_velo
            
            tot_time = init_time + end_time + curr_time
        else:
            tot_time = (2 * self.length) / (self.prev_velo + self.next_velo)  
        
        return tot_time #hours