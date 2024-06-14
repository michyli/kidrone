import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import LineString, Point, LinearRing, MultiPoint

"""
===========================
====== Polygon Class ======
===========================
"""
class PolygonCreate:
    """
    Creates a polygon object given a list of points in tuple
    """
    def __init__(self, points):
        """
        initialization of Polygon object. Points are given in tuples
        >>> points = [(10, 10), (30, 10), (10, 30)]
        x should represent latitude and y should represent longtitude
        """
        
        #Initialization of basic polygon information
        self.xcord = [i[0] for i in points]
        self.ycord = [i[1] for i in points]
        self.xmax, self.xmin = max(self.xcord), min(self.xcord)
        self.ymax, self.ymin = max(self.ycord), min(self.ycord)
        
        #Define Centroid of polygon
        self.xcentroid = sum(self.xcord) / len(self.xcord)
        self.ycentroid = sum(self.ycord) / len(self.ycord)
        self.centroid = Point(self.xcentroid, self.ycentroid)

        #Shapely definitions useful for executing Shapely functions
        self.points = [Point(i[0], i[1]) for i in points]
        self.edges = [LineString([self.points[i], self.points[i+1]]) for i in range(len(points) - 1)]
        self.polygon = LinearRing(tuple(self.points))

    def poly_offset(self, offset):
        """
        return a set of new coordinates of the offset polygon.
        by default, positive offset is inward-offset

        **offset is in unit of latitude / longtitude

        >>> points = [(10, 10), (30, 10), (10, 30)]
        >>> tri = PolygonCreate(points)
        >>> new_tri = tri.poly_offset(1)

        using the method here: https://stackoverflow.com/a/54042831/25136494
        """
        oldX = self.xcord
        oldY = self.ycord
        
        newX = []
        newY = []

        num_points = len(oldX)

        for curr in range(num_points):
            prev = (curr + num_points - 1) % num_points
            next = (curr + 1) % num_points

            #Find the normalized vector of an edge
            vnX =  oldX[next] - oldX[curr]
            vnY =  oldY[next] - oldY[curr]
            vnnX, vnnY = normalizeVec(vnX,vnY)
            #Find the orthogonal vector to the edge
            nnnX = -vnnY
            nnnY = vnnX

            #Find the normalized vector to the other adjacent edge
            vpX =  oldX[curr] - oldX[prev]
            vpY =  oldY[curr] - oldY[prev]
            vpnX, vpnY = normalizeVec(vpX,vpY)
            #Find the orthogonal vector to the edge
            npnX = -vpnY
            npnY = vpnX

            #Bisector is the sum of two vectors orthogonal to the edges
            bisX = (nnnX + npnX)
            bisY = (nnnY + npnY)

            #Determine length of bisector based on the needed offset
            bisnX, bisnY = normalizeVec(bisX,  bisY)
            bislen = offset / np.sqrt((1 + nnnX*npnX + nnnY*npnY)/2)

            #Create the new offset polygon coordinates
            newX.append(oldX[curr] + bislen * bisnX)
            newY.append(oldY[curr] + bislen * bisnY)

            new_points = [(newX[i], newY[i]) for i in range(len(newX))]
        
        return PolygonCreate(new_points)

    def extrapolate_line(self, point, slope):
        """
        Construct a line from a point and a slope, then
        extend a line to the maximum boundry of the polygon.
        returns the extrapolated line
        
        'point' is a Point object
        """
        if slope == "vertical":
            return LineString([Point((point.x, self.ymin)), Point((point.x, self.ymax))])
        elif slope == 0:
            return LineString([Point((self.xmin, point.y)), Point((self.xmax, point.y))])
        else:
            if (point.y + slope * (self.xmax - point.x)) < self.ymax:
                coord_R = Point((self.xmax, (point.y + slope * (self.xmax - point.x))))
            else:
                coord_R = Point(((point.x + (self.ymax - point.y) / slope), self.ymax))
            if (point.y + slope * (self.xmin - point.x)) > self.ymin:
                coord_L = Point((self.xmin, (point.y + slope * (self.xmin - point.x))))
            else:
                coord_L = Point(((point.x + (self.ymin - point.y) / slope), self.ymin))
        
        return LineString([coord_L, coord_R])

    def span_line(self, line):
        """
        crop a linestring to the edge of the polygon if it extends outside of the polygon
        returns the cropped linestring

        'line' is a LineString object
        """
        intersection_points = self.polygon.intersection(line)
        if isinstance(intersection_points, Point):
            return intersection_points
        if isinstance(intersection_points, MultiPoint):
            if len(intersection_points.geoms) > 2:
                new_point_coords = list(intersection_points.geoms)
                #Extract the left-most and right-most intersection points
                coord1, coord2 = max(new_point_coords, key=lambda i: i.x), min(new_point_coords, key=lambda i: i.x)
                new_point_coords = [coord1, coord2]
            else:
                new_point_coords = list(intersection_points.geoms)
                new_point_coords = [new_point_coords[0], new_point_coords[-1]]
            return LineString(new_point_coords)
        if isinstance(intersection_points, LineString):
            return intersection_points

    def swath_gen(self, interval, slope, invert = False, show_baseline = False, _F_single_point = False, _R_single_point = False):
        """
        generates evenly spaced swath lines perpendicular to wind direction
        optimized so that average length of the highest
        """
        def swath_align(swath):
            """
            align all LineStrings inside a swath so that the starting point are on one side, and the ending point on the other
            * .intersection arranges the two intersection points randomly
            swath is a list of LineStrings
            """
            def _dir(line):
                start, end = line.boundary.geoms[0], line.boundary.geoms[1]
                return np.array([end.x - start.x, end.y - start.y])
            base_direction = _dir(swath[0])
            
            for lines in swath[1:]:
                if np.dot(base_direction, _dir(lines)) < 0:
                    swath[swath.index(lines)] = reverse_line(lines)
            return swath
        
        #generate baseline
        baseline = self.extrapolate_line(self.centroid, slope)
        inter_points = split_line(baseline, interval)
        
        #Visualizing Baseline
        if show_baseline:
            """
            for i in inter_points:
                plt.plot(i.x, i.y, 'ko', ms=4, alpha=0.2)
            """
            plt.plot([baseline.boundary.geoms[0].x, baseline.boundary.geoms[1].x], [baseline.boundary.geoms[0].y, baseline.boundary.geoms[1].y], 'ko:', ms=4, alpha=0.2)           
        
        #Determine slope of the swaths (swaths are all perpendicular to baseline)
        if slope == "vertical":
            opp_slope = 0
        elif slope == 0:
            opp_slope = "vertical"
        else:
            opp_slope = -(1 / slope)
        
        #Generate swath if it is within the polygon. swath is a list with LineString elements
        swath = [self.extrapolate_line(i, opp_slope) for i in inter_points if self.polygon.intersects(self.extrapolate_line(i, opp_slope))]
        swath = [self.span_line(i) for i in swath]
        
        #Check if there are single-point intersections (instead of 2-point intersections)
        #Note that single-point intersections will only occur at Front (F) or Rear (R) or the whole path.
        if any([isinstance(i, Point) for i in swath]):
            if isinstance(swath[0], Point):
                _F_single_point = True
                first_point = swath[0]
            if isinstance(swath[-1], Point):
                _R_single_point = True
                last_point = swath[-1]
        swath = [i for i in swath if isinstance(i, LineString)]
        
        #Align all swath path into the same orientation
        swath = swath_align(swath)
        for i in range(1, len(swath), 2):
            swath[i] = reverse_line(swath[i])
        
        if invert:
            for i in range(len(swath)):
                swath[i] = reverse_line(swath[i])
        
        #Create lines that connects all swaths    
        inter_lines = []
        for i in range(len(swath) - 1):
            inter_lines.append(LineString((swath[i].boundary.geoms[1], swath[i+1].boundary.geoms[0])))
            
        #Weave inter_lines into swath to form the complete path
        complete_swath = []
        for i in range(len(inter_lines)):
            complete_swath.append(swath[i])
            complete_swath.append(inter_lines[i])
        complete_swath.append(swath[-1])
        
        #Add front or back single-point intersection to complete swath path
        if _F_single_point:
            first_line = LineString([first_point, swath[0].boundary.geoms[0]])
            complete_swath.insert(0, first_line)
        if _R_single_point:
            last_line = LineString([swath[-1].boundary.geoms[1], last_point])
            complete_swath.insert(-1, last_line)
        
        return complete_swath

    def showpoly(self, polys = None):
        """
        plots the polygon, with the option to plot additional polygon on the same plot
        poly should be given in a list

        >>> points = [(10, 10), (30, 10), (10, 30)]
        >>> tri = PolygonCreate(points)
        >>> tri.showpoly()
        OR
        >>> points_2 = [(10, 10), (30, 10), (10, 40), (15, 30)]
        >>> quad = PolygonCreate(points_2)
        >>> new_tri = tri.poly_offset(1)
        >>> tri.showpoly([new_tri, quad])
        """
        x, y = list(self.xcord), list(self.ycord)
        x.append(x[0])
        y.append(y[0])
        fig, ax = plt.subplots()
        ax.plot(x, y, "ro-.", ms=4)
        
        if polys is not None:
            for poly in polys:
                x, y = list(poly.xcord), list(poly.ycord)
                x.append(x[0])
                y.append(y[0])
                plt.plot(x, y, "ro:", ms=4)    
        
        plt.title("Full Coverage Drone Flight Path")
        plt.xlabel("Latitude")
        plt.ylabel("Longtitude")
        buffer = 0.2 * max(self.xmax - self.xmin, self.ymax - self.ymin)
        plt.xlim(min(self.xmin, self.ymin) - buffer, max(self.xmax, self.ymax) + buffer)
        plt.ylim(min(self.xmin, self.ymin) - buffer, max(self.xmax, self.ymax) + buffer)


"""
==============================
====== General Function ======
==============================
"""
def normalizeVec(x, y):
    #Normalize a vector (x, y)
    norm = 1 / np.sqrt(x ** 2 + y ** 2)
    return x * norm, y * norm

def split_line(line, interval):
    """
    split a line into equal distances
        if a line can't be split into the given interval distance, and there are less than 20% of interval as excess,
            then it expands the interval
        if the excess is more than 20% of the interval,
            then it shrinks the interval to add in another split
    line is a LineString object
    
    return a list of Point objects
    """
    num_div = line.length / interval
    if num_div % 1 < 0.2 and num_div % 1 > 0:
        pass
    else:
        num_div += 1
    
    distances = np.linspace(0, line.length, int(num_div))
    points = [line.interpolate(distance) for distance in distances] + [line.boundary.geoms[-1]]
    if points[-1] == points[-2]:
        points.pop(-1)
    return points

def reverse_line(line):
    """
    reverse the order of points in the line
    'line' is a LineString object with multiple points
    """
    line_list = np.array(line.coords)
    return LineString(line_list[::-1])
    
    """ for i in range(len(line.coords)):
        x = np.array(line.coords)[i][0]
        y = np.array(line.coords)[i][1]
    print(x)
    print(y)
    x = x[::-1]
    y = y[::-1]
    return LineString(zip(x, y)) """
    
def showswath(full_path):     
    """
    plot the complete swath
    'full_path' is a list of LineStrings
    """
    for lines in full_path:
        start, end = lines.coords[0], lines.coords[1]
        xx, yy = [start[0], end[0]], [start[1], end[1]]
        plt.plot(xx, yy, 'go-', ms=6, linewidth=2.5)

"""
============================================
====== Path Generator & Optimizations ======
============================================
"""
def path_length(path):
    """
    returns the total length of the input path
    'path' is a list of LineStrings
    """
    return sum([i.length for i in path])

def generate_path(points, disp_diam, baseline_slope):
    """
    A compacted set of commands to generate a function based on all the necessary informations
    """
    outline = PolygonCreate(points)
    offset_outline = outline.poly_offset(disp_diam / 2)
    outline.showpoly([offset_outline])
    
    #Find out the shortest path between inverted and uninverted versions
    path_uninv = offset_outline.swath_gen(disp_diam, baseline_slope, show_baseline=True, invert=False)
    path_inv = offset_outline.swath_gen(disp_diam, baseline_slope, show_baseline=True, invert=True)
    if path_length(path_uninv) > path_length(path_inv):
        path = path_inv
    else:
        path = path_uninv
    
    showswath(path)
    plt.show()
    return path
    
    
"""
=====================
====== Testing ======
=====================
"""
#Example run: change 'points' to other sets of points to change output
#Note: slope (the third input of generate_path) can be either a float or "vertical"

#Quadualateral
#swath not fully perpendicular to baseline cuz inverted version is shorter in path length
""" eg1 = [(12, 10), (20, 10), (20, 20), (10, 20)] 
path = generate_path(eg1, 1, 1)  """


#Hexalateral
""" eg2 = [(5, 9), (30, 6), (40, 20), (35, 37), (27, 41), (12, 30)]
path = generate_path(eg2, 2, 9) """

#More complicated shape
#Flying outside of designated area
""" eg3 = [(20, 10), (36, 19), (50, 15), (55, 22), (60, 38), (40, 40), (30, 50), (20, 43), (27, 30), (21, 20)] #More complicated shape
path = generate_path(eg3, 3, 9) """

eg4 = [(20, 10), (36, 19), (50, 15), (55, 22), (60, 38), (40, 40), (30, 50), (20, 43), (27, 30), (21, 20)] #More complicated shape
path = generate_path(eg4, 2, 0.2)



#* 100km/h during flight
#? Fuel efficiency vs speed vs payload, etc.
#! Need max flight speed
#! Need turn radius & turn speed

#TODO swath offset




