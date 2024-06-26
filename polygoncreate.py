import numpy as np
import matplotlib.pyplot as plt
from pyproj import Geod
from shapely.geometry import LineString, Point, LinearRing, MultiPoint, Polygon
from basic_functions import *
from path import *

"""
===================
====== Class ======
===================
"""
class PolygonCreate:
    """
    Creates a polygon object with inherit attributes.
    """
    def __init__(self, points, children=None, offsetparent=None):
        """ Initialization of Polygon object.
        
        points:     tuple / list of (x, y) coordinates
        >>> points = [(10, 10), (30, 10), (10, 30)]
        #* In later implementation, x should represent latitude and y should represent longtitude.
        children:   a list of PolygonCreate Objects
        """
        #Initialization of basic polygon information from given points
        self.xcord = [i[0] for i in points]
        self.ycord = [i[1] for i in points]
        self.xmax, self.xmin = max(self.xcord), min(self.xcord)
        self.ymax, self.ymin = max(self.ycord), min(self.ycord)
        self.xcentroid = sum(self.xcord) / len(self.xcord)
        self.ycentroid = sum(self.ycord) / len(self.ycord)
        self.centroid = Point(self.xcentroid, self.ycentroid)
        
        #Basic polygon information defined in shapely objects, necesary for executing Shapely functions
        self.points = [Point(i[0], i[1]) for i in points]
        self.edges = [LineString([self.points[i], self.points[i+1]]) for i in range(len(points) - 1)]
        self.ring = LinearRing(tuple(self.points))
        self.polygon = Polygon(tuple(self.points))

        #Defining children
        if isinstance(children, list):
            for c in children:
                if not c.within(self.polygon):
                    raise AssertionError("The children are not fully contained in the overall polygon.")
        self.children = children
        self.offsetparent = offsetparent

    def poly_offset(self, offset):
        """ Returns a new PolygonCreate object of the offsetted polygon, where
        all the edges are offsetted inward.
        By default, positive offset is inward-offset.
        
        offset: perpendicular distance between new edge and original edge.
        
        example execution:
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
        return PolygonCreate(new_points, self.children, self)

    def extrapolate_line(self, point: Point, slope):
        """ Construct a line from a point and a slope, then extend a line to the maximum boundry of the polygon.
        Returns the new extrapolated line as LineString object.
        
        point: a Point object that anchors the line
        slope: a float or "vertical" that fully defines the line
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

    def span_line(self, line: LineString):
        """ Crops part of the LineString that exceeds the boundary of the polygon.
        Also crops a line to segments if it intersects with any children polygon of the self polygon.
        Returns the new cropped LineString (direction of linestring is not determined).

        line: a LineString object. It is necessary that 'line' intersects the polygon already.
              Otherwise use extrapolate_line() first before calling span_line()
        """
        #Check if the input line intersects with the polygon
        if not self.ring.intersects(line):
            raise ValueError("The line doesn't intersect with the polygon. Call extrapolate_line() first before using span_line()")

        intersection_list = [self.ring.intersection(line)]
        if self.children:
            intersection_list += [enc.ring.intersection(line) for enc in self.children]
        intersection_points = []
        for shp in intersection_list:
            intersection_points.extend(extract_coords(shp))
        intersection_points = list(set(intersection_points))
        
        if line_slope(line) == "vertical":
            intersection_points = sorted(intersection_points, key=lambda pt: pt[1])
        else:
            intersection_points = sorted(intersection_points, key=lambda pt: pt[0])
        return LineString(intersection_points) if len(intersection_points) >= 2 else Point(intersection_points[0])

    def swath_gen(self, interval, slope, invert = False, show_baseline = False, _F_single_point = False, _R_single_point = False):
        """Generates evenly spaced swath lines based on a baseline.
        The baseline is a line that passes through the centroid with the input slope.
        Returns a complete path, which is a list of LineStrings
        
        interval:           dispersion diameter of the drone
        slope:              the slope of the baseline (wind direction) in respect to the horizontal line
        invert:             determines whether the path generated goes in the default (False) direction or an inverted (True) direction
        show_baseline:      determines whether to display baseline in matplotlib graph
        
        _F_single_point:    determines whether there is a single-point-intersection between swath line and polygon at the Front of the path
        _R_single_point:    determines whether there is a single-point-intersection between swath line and polygon at the Rear of the path
        """
        def swath_align(swath):
            """ Aligns all LineStrings inside a swath based on the first one, so that the
            starting point are on one side of the baseline, and the ending points are on the other
            #* .intersection() arranges the two intersection points randomly, and hence the direction of swaths is random without rearranging
            
            swath: a list of LineStrings
            """
            def _dir(line):
                start, end = line.boundary.geoms[0], line.boundary.geoms[1]
                return np.array([end.x - start.x, end.y - start.y])
            base_direction = _dir(swath[0])
            
            for lines in swath[1:]:
                if np.dot(base_direction, _dir(lines)) < 0:
                    swath[swath.index(lines)] = reverse_line(lines)
            return swath
        
        #Determines slope of the swaths (swaths are all perpendicular to baseline)
        if slope == "vertical":
            opp_slope = 0
        elif slope == 0:
            opp_slope = "vertical"
        else:
            opp_slope = -(1 / slope)
        
        #generate baseline
        #* baseline is extrapolated to the minimum bounding box that is slanted according to the desired slope of the baseline
        #* this implementation will ensure that no corners of the mapped area are left out in the constructed path (essentially addressing for edge cases)
        proj_pt = []
        baseline = self.extrapolate_line(self.centroid, slope)
        for point in self.points:
            proj_pt.append(pt_to_line(point, baseline))
        rightmostpoint = [max(proj_pt, key=lambda pt: pt.x)]
        leftmostpoint = [min(proj_pt, key=lambda pt: pt.x)]
        if slope > 0:
            max_point = max(rightmostpoint, key=lambda pt: pt.y)
            min_point = min(leftmostpoint, key=lambda pt: pt.y)
        else:
            max_point = min(rightmostpoint, key=lambda pt: pt.y)
            min_point = max(leftmostpoint, key=lambda pt: pt.y)
                        
        baseline = LineString([line_intersection(self.centroid, slope, min_point, opp_slope), line_intersection(self.centroid, slope, max_point, opp_slope)])
        inter_points = split_line(baseline, interval)
        
        #Visualizing Baseline
        if show_baseline:
            """
            for i in inter_points:
                plt.plot(i.x, i.y, 'ko', ms=4, alpha=0.2)
            """
            plt.plot([baseline.boundary.geoms[0].x, baseline.boundary.geoms[1].x], [baseline.boundary.geoms[0].y, baseline.boundary.geoms[1].y], 'ko:', ms=4, alpha=0.2)           
        
        #Generate swath if it intersects with the polygon.
        swath = [self.extrapolate_line(i, opp_slope) for i in inter_points if self.ring.intersects(self.extrapolate_line(i, opp_slope))]
        swath = [self.span_line(i) for i in swath]
        
        #Check if there are single-point intersections (instead of Multi-point intersections)
        #Note that single-point intersections will only occur at Front (F) or Rear (R) or the whole path.
        if any([isinstance(i, Point) for i in swath]):
            if isinstance(swath[0], Point):
                _F_single_point = True
                first_point = swath[0]
            if isinstance(swath[-1], Point):
                _R_single_point = True
                last_point = swath[-1]
        swath = [i for i in swath if isinstance(i, LineString)]
        
        #Align all swath path into the same orientation using swath_align
        swath = swath_align(swath)
        for i in range(1, len(swath), 2):
            swath[i] = reverse_line(swath[i])
        
        #Check if the default path or inverted path should be generated
        if invert:
            for i in range(len(swath)):
                swath[i] = reverse_line(swath[i])
        
        #Create intermediate lines that connects all swaths    
        inter_lines = []
        for i in range(len(swath) - 1):
            inter_lines.append(LineString((swath[i].boundary.geoms[1], swath[i+1].boundary.geoms[0])))
            
        #Weave intermediate lines into swath to form the complete path
        complete_path = []
        for i in range(len(inter_lines)):
            complete_path.append(swath[i])
            complete_path.append(inter_lines[i])
        complete_path.append(swath[-1])
        
        #Add front or back single-point intersections (if there are any) to complete the ends of the path
        if _F_single_point:
            first_line = LineString([first_point, swath[0].boundary.geoms[0]])
            complete_path.insert(0, first_line)
        if _R_single_point:
            last_line = LineString([swath[-1].boundary.geoms[1], last_point])
            complete_path.insert(-1, last_line)
            
        #Break multi-point swath into multiple 2-point LineStrings
        final_path = []
        for line in complete_path:
            final_path.extend(break_line(line))
        
        print(np.array(final_path))
        return Path(final_path, self, opp_slope)

    def showpoly(self, polys = None):
        """Plots the polygon, with the option to plot additional polygon on the same plot
        
        poly: a list of CreatePolygon objects that will be plotted in addition to 'self'

        example execution of plotting one polygon
        >>> points = [(10, 10), (30, 10), (10, 30)]
        >>> tri = PolygonCreate(points)
        >>> tri.showpoly()
        
        example execution of plotting more than one polygon
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
        
        #Plotting additional polygons if there are any
        if polys:
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

    def show_children(self):
        """Output points of children"""
        
        for c in self.children:
            print(c.points)

    def add_child(self, child):
        """Adds a child to the polygon's list of children

        child: PolygonCreate object

        """
        self.children.append(child)
    
    def remove_child(self, child):
        """Removes a child from the polygon's list of children

        child: PolygonCreate object

        """
        for i in range(len(self.children)):
            if self.children[i] == child:
                self.children = self.children.splice(i, i)
                break
        
