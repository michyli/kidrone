import numpy as np
import matplotlib.pyplot as plt
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
    def __init__(self, points):
        """ Initialization of Polygon object.
        
        points: tuple / list of (x, y) coordinates
        >>> points = [(10, 10), (30, 10), (10, 30)]
        #* In later implementation, x should represent latitude and y should represent longtitude.
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

    def poly_offset(self, offset):
        """ Returns a set of new coordinates of an offsetted polygon, where
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
        
        return PolygonCreate(new_points)

    def extrapolate_line(self, point, slope):
        """ Construct a line from a point and a slope, then extend a line to the maximum
        boundry of the polygon. Returns the new extrapolated line.
        
        point: a Point object -- Point([x, y])
        slope: a float or "vertical"
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
        """ Crops part of the LineString that exceeds the boundary of the polygon
        Returns the new cropped LineString.

        line: a LineString object. It is necessary that 'line' intersects the polygon already.
              Otherwise use extrapolate_line() first before calling span_line()
        """
        #Check if the input line intersects with the polygon
        if not self.ring.intersects(line):
            raise ValueError("The line doesn't intersect with the polygon. Call extrapolate_line() first before using span_line()")
        
        intersection_points = self.ring.intersection(line)
        if isinstance(intersection_points, Point):
            #Case where line and polygon intersects only at a point
            return intersection_points
        if isinstance(intersection_points, MultiPoint):
            #Case where line and polygon intersects at more than one point
            if len(intersection_points.geoms) > 2:
                new_point_coords = list(intersection_points.geoms)
                #Extract the left-most and right-most intersection points
                #Note that points returned from .intersection() in NOT ordered
                coord1, coord2 = max(new_point_coords, key=lambda i: i.x), min(new_point_coords, key=lambda i: i.x)
                new_point_coords = [coord1, coord2]
            else:
                new_point_coords = list(intersection_points.geoms)
                new_point_coords = [new_point_coords[0], new_point_coords[-1]]
            return LineString(new_point_coords)
        if isinstance(intersection_points, LineString):
            #Case where the line is co-linear with one of the polygon's edge
            return intersection_points

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
        
        return Path(complete_path, self)

    def showpoly(self, polys = None):
        """ Plots the polygon, with the option to plot additional polygon on the same plot
        
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