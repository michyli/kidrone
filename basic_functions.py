import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import LineString, Point, LinearRing, MultiPoint, Polygon
from math import acos, sqrt, pi

"""
======================
=== Basic Functions===
======================

Here is a list of general functions used in the rest of the algorithm.
They are very helpful to manipulate Shapely datatypes and vectors to gear towards a general purpose.
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

def line_slope(line):
    """Returns the slope of a LineString based on the boundary of the LineString
    Returns a float or "vertical"
    
    line: a LineString object
    """
    try:
        slope = (line.boundary.geoms[1].y - line.boundary.geoms[0].y) / (line.boundary.geoms[1].x - line.boundary.geoms[0].x)
    except ZeroDivisionError:
        slope = "vertical"
    return slope

def line_angle(line1, line2):
    """Returns the smaller angle formed by two line segments.
    both inputs are LineString objects, and direction of the LineString objects matters.
    Two line segments should be consecutive, meaning that they should intersect at at least one point.
    output should be angle in degree.
    """
    #Check for continuity
    if line1.coords[-1] != line2.coords[0] and line2.coords[-1] != line1.coords[0]:
        raise ValueError("The lines are not continuous")
    
    #vectorize two LineStrings
    vec1 = (line1.coords[1][0] - line1.coords[0][0], line1.coords[1][1] - line1.coords[0][1])
    vec2 = (line2.coords[1][0] - line2.coords[0][0], line2.coords[1][1] - line2.coords[0][1])

    dot_product = (vec1[0] * vec2[0]) + (vec1[1] * vec2[1])
    magnitude1 = sqrt(vec1[0] ** 2 + vec1[1] ** 2)
    magnitude2 = sqrt(vec2[0] ** 2 + vec2[1] ** 2)

    angle_rad = acos(dot_product / (magnitude1 * magnitude2))
    angle_deg = angle_rad * (180 / pi)

    if angle_deg > 180:
        angle_deg = 360 - angle_deg

    angle_deg = 180 - angle_deg
    return angle_deg

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

def extract_coords(shape):
    """Extracts Shapely geometry (Point, MultiPoint, LineString) coordinates into a list of tuples.
    Returns the extracted list of coordinates
    
    shape: a Point, MultiPoint, or LineString object
    """
    if isinstance(shape, Point):
        return (shape.x, shape.y)
    if isinstance(shape, MultiPoint):
        return [(pt.x, pt.y) for pt in shape.geoms]
    if isinstance(shape, LineString):
        return [(pt[0], pt[1]) for pt in shape.coords]

def break_line(line):
    """Break a multi-point LineString into a list of multiple 2-point LineStrings
    Returns a list of LineString objects
    
    line: a LineString object
    """
    coords = list(line.coords)
    return [LineString([coords[i], coords[i+1]]) for i in range(len(coords)-1)]

def showswath(full_path):     
    """Plots the complete swath
    full_path: a Path object. the .path attribute extracts the list of LineString that makes the Path object
    """
    for lines in full_path.path:
        start, end = lines.coords[0], lines.coords[1]
        xx, yy = [start[0], end[0]], [start[1], end[1]]
        plt.plot(xx, yy, 'go-', ms=6, linewidth=2.5)