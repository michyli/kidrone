import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import LineString, Point, LinearRing, MultiPoint
from math import acos, sqrt, pi

"""
=============================================
=== Basic Functions independent of Classes===
=============================================
"""
def normalizeVec(x, y):
    """Normalize a vector (x, y)"""
    norm = 1 / np.sqrt(x ** 2 + y ** 2)
    return x * norm, y * norm

def line_intersection(point1, slope1, point2, slope2):
    """Finds the point of intersection between two straight lines given the point and slope of both lines.
    Returns a Point object.
    
    point1: Point object
    slope1: float or "vertical"
    point2: Point object
    slope2: float or "vertical"
    """
    if slope1 == "vertical" and slope2 == "vertical":
        if point1 == point2:
            raise ValueError("two inputted lines are the same")
        else:
            raise ValueError("No intersections, two inputted lines are parallel")
    if slope1 == "vertical":
        return Point([point1.x, point2.y + slope2 * (point1.x - point2.x)])
    if slope2 == "vertical":
        return Point([point2.x, point1.y + slope1 * (point2.x - point2.x)])
        
    b1 = point1.y - slope1 * point1.x
    b2 = point2.y - slope2 * point2.x
    
    x = (b2 - b1) / (slope1 - slope2)
    y = slope1 * x + b1
    return Point([x, y])

def line_angle(line1, line2):
    """Returns the smaller angle formed by two line segments.
    both inputs are LineString objects, and direction of the LineString objects matters.
    Two line segments should be consecutive, meaning that they should intersect at at least one point.
    output should be angle in degree.
    """
    #Check for continuity
    #TODO end of line 1 is start of line 2, and also vice versa. Otherwise raise an error "The lines are not continuous"
    #vectorize two LineStrings
    vec1 = (line1.coords[1][0] - line1.coords[0][0], line1.coords[1][1] - line1.coords[0][1])
    vec2 = (line2.coords[1][0] - line2.coords[0][0], line2.coords[1][1] - line2.coords[0][1])

    dot_product = (vec1[0] * vec2[0]) + (vec1[1] * vec2[1])
    angle = acos(dot_product / (sqrt(vec1[0] ** 2 + vec1[1] ** 2) + sqrt(vec2[0] ** 2 + vec2[1] ** 2))) * (180 / pi)
    print(angle)
    if angle > 180:
        angle = 360 - angle
    angle = 180 - angle
    return angle

def pt_to_line(point, line):
    """Orthogonally projects a point onto a line
    returns the projected point as a Point object
    
    point:  a Point object
    line:   a LineString object
    """
    x = np.array(point.coords[0])

    u = np.array(line.coords[0])
    v = np.array(line.coords[len(line.coords)-1])

    n = v - u
    n /= np.linalg.norm(n, 2)

    P = u + n*np.dot(x - u, n) #datatype if np.array
    return Point([P[0], P[1]])

def split_line(line, interval):
    """Splits a line into equal distances
        if a line can't be split into the given interval distance, and there are less than 20% of interval as excess,
            then it expands the interval slightly
        if the excess is more than 20% of the interval,
            then it shrinks the interval to add in another split
   
    line:       a LineString object
    interval:   the desired distance between points
    
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
    """Reverses the order of points in the LineString
    line: a LineString object with two or more points
    """
    line_list = np.array(line.coords)
    return LineString(line_list[::-1])
    
def linestring_dist(line):
    """Returns the distance in KM given a LineString as an input
    
    The more accurate calculation involves Haversin Formula.
    But for the purpose here, a rough estimate is sufficient.
    """
    # 1° of latitude is always 111.32 km
    dx = (line.coords[1][0] - line.coords[0][0]) * 111.32
    # 1° of longitude is 40075 km * cos(latitude) / 360
    dy = 40075 * np.cos((line.coords[1][1] - line.coords[0][1])) / 360
    length = np.sqrt(dx**2 + dy**2)
    return length

def showswath(full_path):     
    """Plots the complete swath
    full_path: a Path object
    """
    for lines in full_path.path:
        start, end = lines.coords[0], lines.coords[1]
        xx, yy = [start[0], end[0]], [start[1], end[1]]
        plt.plot(xx, yy, 'go-', ms=6, linewidth=2.5)