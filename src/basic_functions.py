import numpy as np
import matplotlib.pyplot as plt
from pyproj import Transformer
from shapely.geometry import LineString, Point, MultiPoint, Polygon, MultiPolygon
import geopandas as gpd
import random
import csv
import requests
import urllib

"""
======================
=== Basic Functions===
======================

Here is a list of general functions used in the rest of the algorithm.
They are very helpful to manipulate Shapely datatypes and vectors to gear towards a general purpose.
"""

"""
===============================
=== Shapely Polygon Related ===
===============================
"""


def extractPolygons(multipolygon):
    "Takes a shapely multipolygon instance and returns the individual polygons in a list"
    polygons = []
    if isinstance(multipolygon, MultiPolygon):
        for polys in multipolygon.geoms:
            polygons.append(polys)
        return polygons
    else:
        print("The argument to function 'extractPolygons' is not a multipolygon")
        return


"""
======================
=== Vector Related ===
======================
"""


def normalizeVec(x, y, z=0):
    """Normalize a vector (x, y)"""
    if x == 0:
        assert y != 0, "Zero vector cannot be normalized"
    if y == 0:
        assert x != 0, "Zero vector cannot be normalized"

    if z:
        norm = 1 / np.sqrt(x ** 2 + y ** 2 + z ** 2)
        return x * norm, y * norm, z*norm
    else:
        norm = 1 / np.sqrt(x ** 2 + y ** 2)
        return x * norm, y * norm


"""
==========================
=== LineString Related ===
==========================
"""


def line_slope(line: LineString):
    """Returns the slope of a LineString based on the boundary of the LineString"""
    assert isinstance(line, LineString), "input should be a LineString object"
    if (line.boundary.geoms[1].x - line.boundary.geoms[0].x) != 0:
        slope = (line.boundary.geoms[1].y - line.boundary.geoms[0].y) / (line.boundary.geoms[1].x - line.boundary.geoms[0].x)
    else:
        slope = "vertical"
    return slope


def line_angle(line1: LineString, line2: LineString):
    """Returns the smaller angle formed by two line segments.
    Note that the direction of the LineString objects matters.
    Two line segments should be consecutive, meaning that they should intersect at at least one point.
    Output angle is in degrees.
    """
    assert all(isinstance(i, LineString)
               for i in [line1, line2]), "input lines should be Line objects"

    # Check for continuity
    if line1.coords[-1] != line2.coords[0] and line2.coords[-1] != line1.coords[0]:
        raise ValueError("The lines are not continuous")

    if line2.coords[-1] == line1.coords[0]:
        # if line sequence is 2 -> 1, swap them
        temp = line1
        line1 = line2
        line2 = temp

    # vectorize two LineStrings
    vec1 = (line1.coords[1][0] - line1.coords[0][0],
            line1.coords[1][1] - line1.coords[0][1])
    vec2 = (line2.coords[1][0] - line2.coords[0][0],
            line2.coords[1][1] - line2.coords[0][1])
    vec1n = normalizeVec(vec1[0], vec1[1])
    vec2n = normalizeVec(vec2[0], vec2[1])
    
    #Account for python rounding error, else you get "RuntimeWarning: invalid value encountered in arccos"
    dot = np.dot(vec1n, vec2n)
    if dot > 1 and dot < 1+1e-8:
        dot = 1
    elif dot < -1 and dot > -1-1e-8:
        dot = -1
    
    angle = np.rad2deg(np.arccos(dot))
    #Range of arccos() is (0, pi) or (0, 180)
    return angle


def line_intersection(point1: Point, slope1, point2: Point, slope2):
    """Finds the point of intersection between two straight lines given the point and slope of both lines.

    slope1 and slope2 can be either given as number or "vertical"
    """

    assert all(isinstance(i, Point)
               for i in [point1, point2]), "input point should be Point objects"
    assert isinstance(
        slope1, (int, float)) or slope1 == "vertical", "input slope1 should be a number or 'vertical'"
    assert isinstance(
        slope2, (int, float)) or slope2 == "vertical", "input slope2 should be a number or 'vertical'"

    if slope1 == "vertical" and slope2 == "vertical":
        if point1 == point2:
            raise ValueError("two inputted lines are the same")
        else:
            raise ValueError(
                "No intersections, two inputted lines are parallel")
    if slope1 == "vertical":
        return Point([point1.x, point2.y + slope2 * (point1.x - point2.x)])
    if slope2 == "vertical":
        return Point([point2.x, point1.y + slope1 * (point2.x - point2.x)])

    b1 = point1.y - slope1 * point1.x
    b2 = point2.y - slope2 * point2.x

    x = (b2 - b1) / (slope1 - slope2)
    y = slope1 * x + b1
    return Point([x, y])


def split_line(line: LineString, interval) -> list[Point]:
    """Splits a line into equal distances
        if a line can't be split into the given interval distance, and there are less than 20% of interval as excess,
            then it expands the interval slightly
        if the excess is more than 20% of the interval,
            then it shrinks the interval to add in another split

    line:       a LineString object to be split
    interval:   the desired distance between points

    return a list of Point objects
    """
    assert isinstance(
        line, LineString), "input line should be a LineString object"
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


def reverse_line(line: LineString):
    """Reverses the order of points in the LineString
    line: a LineString object with two or more points to be reversed in direction
    """
    assert isinstance(
        line, LineString), "input line should be a LineString object"
    line_list = np.array(line.coords)
    return LineString(line_list[::-1])

def create_line(points: list[Point]) -> list[LineString]:
    """Create a list of 2-point LineString from a list of waypoints
    """
    linelist = []
    for i in range(len(points)-1):
        linelist.append(LineString([points[i], points[i+1]]))
    return linelist
    

def break_line(line: LineString) -> list[LineString]:
    """Break a multi-point LineString into a list of multiple 2-point LineStrings
    Returns a list of LineString objects

    line: a LineString object to be broken down
    """
    assert isinstance(
        line, LineString), "input line should be a LineString object"
    coords = list(line.coords)
    return [LineString([coords[i], coords[i+1]]) for i in range(len(coords)-1)]


def merge_line(linelist: list[LineString]):
    """Merge a list of continuous 2-point LineStrings into one single multi-point LineString
    Returns a single LineString object
    """
    coords = []
    start_coord = None
    for line in linelist:
        firstpoint = line.boundary.geoms[0]
        secondpoint = line.boundary.geoms[1]
        if not start_coord:
            coords.append(firstpoint)
            coords.append(secondpoint)
            start_coord = secondpoint
        else:
            assert firstpoint == start_coord, "Lines are not continuous"
            coords.append(secondpoint)
            start_coord = secondpoint
    return LineString(coords)


def check_continuity(lines: list[LineString]):
    """check if the list of lines are continuous

    lines: a list of LineStrings to be checked
    """
    count = 1
    for i in range(1, len(lines)-1):
        assert lines[i -
                     1].boundary.geoms[1] == lines[i].boundary.geoms[0], f"line{i-1} and line{i} are not continuous"
        count += 1
    return True


"""
================================
=== Coordinates Manipulation ===
================================
"""


def pt_to_line(point: Point, line: LineString):
    """Orthogonally projects a point onto a line
    returns the projected point as a Point object

    point:  the point being projected
    line:   the line being projected onto
    """
    assert isinstance(point, Point) and isinstance(
        line, LineString), "input should be a Point object and a LineString object"

    x = np.array(point.coords[0])

    u = np.array(line.coords[0])
    v = np.array(line.coords[len(line.coords)-1])

    n = v - u
    n /= np.linalg.norm(n, 2)

    P = u + n*np.dot(x - u, n)  # datatype if np.array
    return Point([P[0], P[1]])


"""
==============================
=== Coordinates Extraction ===
==============================
"""


def extract_coords(shape: Point | MultiPoint | LineString | Polygon) -> list[tuple]:
    """Extracts Shapely geometry (Point, MultiPoint, LineString) coordinates into a list of tuples.
    Returns the extracted list of coordinates

    shape: a Point, MultiPoint, or LineString object to be flattened
    """
    assert isinstance(shape, (Point, MultiPoint, LineString, Polygon)
                      ), "input must be a Point, MultiPoint, LineString, or Polygon object"

    if isinstance(shape, Point):
        return [(shape.x, shape.y)]
    if isinstance(shape, MultiPoint):
        return [(pt.x, pt.y) for pt in shape.geoms]
    if isinstance(shape, LineString):
        return [(pt[0], pt[1]) for pt in shape.coords]
    if isinstance(shape, Polygon):
        return [(x, y) for x, y in zip(shape.exterior.xy[0], shape.exterior.xy[1])]


def csv2coords(csvfile):
    """extract coordinate from a .csv file"""
    with open(csvfile, 'r') as csvfile:
        next(csvfile)
        csv_reader = csv.reader(csvfile)
        coords = [(row[0], row[1]) for row in csv_reader]
    return coords


def shp2coords(shapefile_path):
    "Takes a path to a shapefile and returns a list of longitude and latitude coordinates, where each element is a polygon's coordinates"
    "Reads in the coordinate system from the shapefile and converts it to "
    # Example shapefile path
    gdf = gpd.read_file(shapefile_path)

    # Print the CRS
    print("CRS:", gdf.crs)
    print("\n")

    # Get all the geometries in the geometry column
    geometries = gdf['geometry']
    # For each geometry make a list to store it's polygons
    # Each element in the list is a list of polygons, representing the polygons of a geo
    geo_poly_list = []
    for geo in geometries:
        polygons = extractPolygons(geo)
        geo_poly_list.append(polygons)
    # For each polygon extract the coordinates
    coordinates = []
    for poly_list in geo_poly_list:
        for polygon in poly_list:
            coordinates.append(extract_coords(polygon))

    transformed_coordinates = [bccs2gcs_batch(coord) for coord in coordinates]
    # Convert to EPSG 3857 coordinates and return
    return transformed_coordinates


"""
===============================
=== Coordinates Conversions ===
===============================
"""
def gcs2pcs(lon, lat):
    """Converts EPSG:4326 (lon&lat) to EPSG:3857 (meters)
    """
    transformer = Transformer.from_crs(
        "EPSG:4326", "EPSG:3857", always_xy=True)
    x, y = transformer.transform(lon, lat)
    if x == np.inf or y == np.inf:
        raise ValueError(
            "input should be in sequence of (Longtitude, Latitude), it may be currently reversed")
    return x, y


def pcs2gcs(x, y):
    """Converts EPSG:3857 (meters) to EPSG:4326 (lon&lat)
    """
    transformer = Transformer.from_crs(
        "EPSG:3857", "EPSG:4326", always_xy=True)
    lon, lat = transformer.transform(x, y)
    return lon, lat


def bccs2pcs(x, y):
    """Converts EPSG:3005 (meters) to EPSG:3857 (meters)
    """
    transformer = Transformer.from_crs(
        "EPSG:3005", "EPSG:3857", always_xy=True)
    x, y = transformer.transform(x, y)
    if x == np.inf or y == np.inf:
        raise ValueError(
            "input should be in sequence of (Longtitude, Latitude), it may be currently reversed")
    return x, y


def gcs2pcs_batch(coords):
    """Converts EPSG:4326 (lon&lat) to EPSG:3857 (meters)
    but input is a whole list of EPSG:4326 coordinates
    """
    return [list(gcs2pcs(pt[0], pt[1])) for pt in coords]


def pcs2gcs_batch(coords):
    """Converts EPSG:3857 (meters) to EPSG:4326 (lon&lat)
    but input is a whole list of EPSG:3857 coordinates
    """
    return [list(pcs2gcs(pt[0], pt[1])) for pt in coords]


def bccs2gcs_batch(coords):
    """Converts EPSG:3005 (meters) to EPSG:3875 (meters)
    but input is a whole list of EPSG:3005 coordinates
    """
    return [list(bccs2pcs(pt[0], pt[1])) for pt in coords]


"""
==============
=== Others ===
==============
"""
def get_elevation(coordinates):
    """Uses the usgs api to obtain elevation data
    coordinate: tuple of (longtitude, latitude)
    """
    url = r'https://epqs.nationalmap.gov/v1/json?'
    elevation=[]
    
    num_pts = len(coordinates)
    print(f"Note: Accessing elevation data takes time on public API. Estimated time {int(num_pts/2//60)} mins {int(num_pts/2%60)} secs")
    for coord in print_progress(coordinates):       
        # define rest query params
        params = {
            'output': 'json',
            'x': coord[0],
            'y': coord[1],
            'units': 'Meters'
        }
        # format query string and return query value
        result = requests.get((url + urllib.parse.urlencode(params)))
        #elevations.append(result.json()['USGS_Elevation_Point_Query_Service']['Elevation_Query']['Elevation'])
        #new 2023:
        elevation.append(result.json()['value'])
    return elevation

def arbit_list(num, min, max):
    """
    Function used for generating test data for show3DPath
    Generate a list of tuples representing heights for each line segment.

    num_lines:  The number of LineString objects.
    min_height: The minimum height value.
    max_height: The maximum height value.
    """
    heights = np.linspace(min, max, num)
    values = [(heights[i], heights[i+1]) for i in range(len(heights)-1)]
    return values

def disp_time(hour):
    """Convert inputed hours to the format of day:hour:minute"""
    return f"This path is projected to take {int(hour//24)} days, {int(hour%24//1)} hours, and {round(hour%1*60, 1)} minutes"

def print_progress(iterable, prefix = ' Progress:', suffix = 'Complete', decimals = 1, length = 50, fill = '█', printEnd = "\r"):
    """
    @params:
        iterable    - Required  : iterable object (Iterable)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        
    example usage:
    >>> for item in progressBar(items):
    >>>     # Do stuff...
    >>>     time.sleep(0.1)
    where 'items' is the list to be iterated through
    """
    total = len(iterable)
    # Progress Bar Printing Function
    def printProgressBar (iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Initial Call
    printProgressBar(0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)
    # Print New Line on Complete
    print()