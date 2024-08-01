# src/outline.py

from shapely.geometry import LineString, Point, LinearRing, MultiPoint, Polygon
from basic_functions import *
from path import *

"""
=====================
=== Outline Class ===
=====================

Description of the Outline class, its attributes, and methods.

#TL:DR
Outline instance has all the information about the polygon it describes.
An Outline instance can store other Outline instances as its children if they are all fully contained within it.
Outline instance generates a Path instance with the 'swath_gen()' function.
"""

class Outline:
    def __init__(self, name: str, points: list, children=[], offsetparent=None):
        """
        points:         list of (x, y) coordinates, in EPSG:3857 (meters)
        children:       a list of Outline Objects
        offsetparent:   an Outline object. If self is a polygon offsetted from another, it shows its parent here.
        """
        # Initialize basic polygon information from given points
        self.xcoord = [i[0] for i in points]
        self.ycoord = [i[1] for i in points]
        self.xmax, self.xmin = max(self.xcoord), min(self.xcoord)
        self.ymax, self.ymin = max(self.ycoord), min(self.ycoord)
        self.name = name

        # define basic polygon information in shapely objects, necesary for executing Shapely functions
        self.points = [Point(i[0], i[1]) for i in points]
        self.ring = LinearRing(tuple(self.points))
        self.polygon = Polygon(tuple(self.points))

        self.centroid = self.polygon.centroid
        self.area = self.polygon.area / 1000**2  # KM^2

        self.offsetparent = offsetparent
        self.children = self.children_setter(children)
        
        #*If the attribute you are looking for isn't in __init__, look for it at the bottom in @cached_properties
        
    def poly_offset(self, offset):
        """Returns an offsetted polygon as an Outline object.

        offset: offset distance, in unit of meters
        * Positive = inward offset, negative = outward offset
        """
        newpoly = self.polygon.buffer(-offset, quad_segs=3)
        assert isinstance(newpoly, Polygon), "Offseting polygon has caused discontinuity in the field area. Try setting poly-offset parameter in construct_pathlist parameter"
        x, y = newpoly.exterior.xy
        coord_set = [(x[i], y[i]) for i in range(len(x))]
        if not coord_set:
            raise ValueError("Unable to offset the existing polygon. Either try not adding an offset when constructing Path, or double check if the Outline is big enough (minimum width at any point is at least dispersion diameter)")
        inherit_children = list(self.children.values()) if self.children else None
        return Outline('offset', coord_set, children=inherit_children, offsetparent=self)

    def extrapolate_line(self, point: Point, slope):
        """Construct a line from a point and a slope, then extend a line to the maximum boundary of the polygon.
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
                coord_R = Point(
                    (self.xmax, (point.y + slope * (self.xmax - point.x))))
            else:
                coord_R = Point(
                    ((point.x + (self.ymax - point.y) / slope), self.ymax))
            if (point.y + slope * (self.xmin - point.x)) > self.ymin:
                coord_L = Point(
                    (self.xmin, (point.y + slope * (self.xmin - point.x))))
            else:
                coord_L = Point(
                    ((point.x + (self.ymin - point.y) / slope), self.ymin))

        return LineString([coord_L, coord_R])

    def span_line(self, line: LineString):
        """ Crops part of the LineString that exceeds the boundary of the polygon.
        Also crops a line to segments if it intersects with any children polygon of the self polygon.
        Returns the new cropped LineString (direction of linestring is not determined).

        line: a LineString object. It is necessary that 'line' intersects the polygon already.
              Otherwise use extrapolate_line() first before calling span_line()
        """
        # Check if the input line intersects with the polygon
        if not self.ring.intersects(line):
            raise ValueError(
                "The line doesn't intersect with the polygon. Call extrapolate_line() first before using span_line()")

        intersection_list = [self.ring.intersection(line)]
        if self.children:
            newlist = [excluded.ring.intersection(line) for excluded in self.children.values()]
            intersection_list += [excluded.ring.intersection(line) for excluded in self.children.values()]
        
        intersection_points = []
        for shp in intersection_list:
            intersection_points.extend(extract_coords(shp))
        intersection_points = list(set(intersection_points))

        if line_slope(line) == "vertical":
            intersection_points = sorted(
                intersection_points, key=lambda pt: pt[1])
        else:
            intersection_points = sorted(
                intersection_points, key=lambda pt: pt[0])

        return LineString(intersection_points) if len(intersection_points) >= 2 else Point(intersection_points[0])

    def swath_gen(self, interval, slope, invert=False, _F_single_point=False, _R_single_point=False):
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
                """returns the direction (vector form) of the input line"""
                start, end = line.boundary.geoms[0], line.boundary.geoms[1]
                return np.array([end.x - start.x, end.y - start.y])
            base_direction = _dir(swath[0])

            for lines in swath[1:]:
                if np.dot(base_direction, _dir(lines)) < 0:
                    swath[swath.index(lines)] = reverse_line(lines)
            return swath

        # Determines slope of the swaths (swaths are all perpendicular to baseline)
        if slope == "vertical":
            opp_slope = 0
        elif slope == 0:
            opp_slope = "vertical"
        else:
            opp_slope = -(1 / slope)

        # generate baseline
        # * This method finds the minimum bounding box of the polygon in the direction of the baseline, and find max and min point baseline can extend to.
        # * this implementation will ensure that no corners of the mapped area are left out in the constructed path (essentially addressing for edge cases)
        proj_pt = []
        baseline = self.extrapolate_line(self.centroid, slope)
        for point in self.points:
            # project all vertices of polygon onto the extrapolated line
            proj_pt.append(pt_to_line(point, baseline))
        # find the points on either end of the extrapolated line
        if slope == "vertical":
            topmostpoint = [max(proj_pt, key=lambda pt: pt.y)]
            bottommostpoint = [min(proj_pt, key=lambda pt: pt.y)]

            baseline = LineString([topmostpoint[0], bottommostpoint[0]])
        else:
            rightmostpoint = [max(proj_pt, key=lambda pt: pt.x)]
            leftmostpoint = [min(proj_pt, key=lambda pt: pt.x)]
            if slope > 0:
                max_point = max(rightmostpoint, key=lambda pt: pt.y)
                min_point = min(leftmostpoint, key=lambda pt: pt.y)
            else:
                max_point = min(rightmostpoint, key=lambda pt: pt.y)
                min_point = max(leftmostpoint, key=lambda pt: pt.y)

            baseline = LineString([line_intersection(self.centroid, slope, min_point, opp_slope), line_intersection(
                self.centroid, slope, max_point, opp_slope)])

        # generate evenly spaced points on the baseline
        inter_points = split_line(baseline, interval)

        # Generate swath if it intersects with the polygon.
        swath = [self.extrapolate_line(i, opp_slope) for i in inter_points if self.ring.intersects(
            self.extrapolate_line(i, opp_slope))]
        swath = [self.span_line(i) for i in swath]

        # Check if there are single-point intersections (instead of Multi-point intersections)
        # Note that single-point intersections will only occur at Front (F) or Rear (R) or the whole path.
        if any([isinstance(i, Point) for i in swath]):
            if isinstance(swath[0], Point):
                _F_single_point = True
                first_point = swath[0]
            if isinstance(swath[-1], Point):
                _R_single_point = True
                last_point = swath[-1]
        swath = [i for i in swath if isinstance(i, LineString)]

        # Align all swath path into the same orientation using swath_align
        swath = swath_align(swath)
        for i in range(1, len(swath), 2):
            swath[i] = reverse_line(swath[i])

        # Check if the default path or inverted path should be generated
        if invert:
            for i in range(len(swath)):
                swath[i] = reverse_line(swath[i])

        # Create intermediate lines that connects all swaths
        inter_lines = []
        for i in range(len(swath) - 1):
            inter_lines.append(LineString(
                (swath[i].boundary.geoms[1], swath[i+1].boundary.geoms[0])))

        # Weave intermediate lines into swath to form the complete path
        complete_path = []
        for i in range(len(inter_lines)):
            complete_path.append(swath[i])
            complete_path.append(inter_lines[i])
        complete_path.append(swath[-1])

        # Add front or back single-point intersections (if there are any) to complete the ends of the path
        if _F_single_point:
            first_line = LineString([first_point, swath[0].boundary.geoms[0]])
            complete_path.insert(0, first_line)
        if _R_single_point:
            last_line = LineString([swath[-1].boundary.geoms[1], last_point])
            complete_path.append(last_line)

        # Break multi-point swath into multiple 2-point LineStrings
        final_path = []
        for line in complete_path:
            final_path.extend(break_line(line))

        check_continuity(final_path)

        return Path(final_path, self, interval, opp_slope)

    """
    ===========================
    === Children Management ===
    ===========================
    """

    def children_setter(self, children):
        """Populate children in a hashmap"""
        #children defaults to []
        children_dict = {}
        if children:
            for c in children:
                children_dict[c.name] = c
        # Check if children are contained in the field
        """ for c in children_dict.values():
            if not c.polygon.within(self.polygon.buffer(1e-8)):
                raise AssertionError("The children are not fully contained in the overall polygon.") """
        return children_dict

    def show_children(self):
        """Output points of children"""
        for c in self.children:
            print(c.points)

    def add_child(self, child):
        """Adds a child to the polygon's list of children

        child: Outline object
        """
        if not isinstance(child, Outline):
            raise ValueError("input must be an Outline object")
        self.children[child.name] = child

    def remove_child(self, child):
        """Removes a child from the polygon's list of children

        child: Outline object
        """
        if not isinstance(child, Outline):
            raise ValueError("input must be an Outline object")
        if self.children is None:
            print("There are no children to remove.")
        else:
            self.children.pop(child.name)
