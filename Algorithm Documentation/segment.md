### Segment
***class* Segment(line, parent, prev_velo=None, curr_velo=None, next_velo=None, prev_angle=None, next_angle=None)**
The `Segment` class represents a singular line segment of a `Path` instance. It stores information about the segment's coordinates and the velocities at which the drone will travel at various points along the segment. The class also calculates the time required to traverse the segment, considering acceleration and deceleration curves at the start and end of the segment. It provides methods for managing and analyzing the segment's attributes and its relationship with the parent Path instance. 

> **Parameters:**
* **line:** *`LineString`*
  * A `LineString` object that contains the coordinates of the segment.
* **parent:** *`Path` instance*
  * The parent `Path` object the segment belongs to.
* **prev_velo:** *float, optional*
  * The velocity of the previous segment in the path.
* **curr_velo:** *float, optional*
  * The velocity of the current segment in the path.
* **next_velo:** *float, optional*
  * The velocity of the next segment in the path.
* **prev_angle:** *float, optional*
  * The angle of the previous segment in the path.
* **next_angle:** *float, optional*
  * The angle of the next segment in the path.

> **Attributes:**
* **line:** *`LineString`*
  * The `LineString` object representing the segment's coordinates.
* **parent:** *`Path`*
  * The parent `Path` instance the segment belongs to.
* **prev_velo:** *float*
  * The velocity of the previous segment in the path.
* **curr_velo:** *float*
  * The velocity of the current segment in the path.
* **next_velo:** *float*
  * The velocity of the next segment in the path.
* **prev_angle:** *float*
  * The angle of the previous segment in the path.
* **next_angle:** *float*
  * The angle of the next segment in the path.
* **length:** *float*
  * The length of the segment in kilometers.

***method* calculate_travel_time(self)**
Calculates the travel time required to cover the segment based on the drone's velocities and acceleration/deceleration curves.

***method* display_segment(self, show=True)**
Displays the segment on a map.

> **Parameters:**
* **show:** *bool*
  * Determines whether to display the segment immediately. Defaults to `True`.

***method* save_segment(self, filename)**
Saves the segment information to a file.

> **Parameters:**
* **filename:** *string*
  * Name of the file to save the segment information.

***method* load_segment(self, filename)**
Loads segment information from a file.

> **Parameters:**
* **filename:** *string*
  * Name of the file to load the segment information from.


### basic_functions
A collection of general-purpose functions used throughout the algorithm to manipulate Shapely datatypes and vectors. These functions are essential for various operations related to polygons, vectors, and line segments.

> **Functions:**

***function* extractGeoTypes(geometry)**
Takes a Shapely geometry instance and returns the individual polygons in a list.

> **Parameters:**
* **geometry:** *Shapely geometry*
  * A Shapely geometry instance (e.g., `MultiPolygon`, `Polygon`).

> **Returns:**
* **polygons:** *list of `Polygon`*
  * A list of individual polygons extracted from the input geometry.

***function* normalizeVec(x, y, z=0)**
Normalizes a vector (x, y) or (x, y, z).

> **Parameters:**
* **x:** *float*
  * The x-coordinate of the vector.
* **y:** *float*
  * The y-coordinate of the vector.
* **z:** *float, optional*
  * The z-coordinate of the vector. Defaults to 0.

> **Returns:**
* **normalized vector:** *tuple of float*
  * The normalized vector components.

***function* line_slope(line)**
Returns the slope of a `LineString` based on its boundary points.

> **Parameters:**
* **line:** *`LineString`*
  * A `LineString` object.

> **Returns:**
* **slope:** *float or str*
  * The slope of the line or "vertical" if the line is vertical.

***function* pt_to_line(point, line)**
Projects a point onto a line and returns the projected point.

> **Parameters:**
* **point:** *`Point`*
  * A `Point` object to be projected.
* **line:** *`LineString`*
  * A `LineString` object on which the point will be projected.

> **Returns:**
* **projected_point:** *`Point`*
  * The point projected onto the line.

***function* line_intersection(p1, slope1, p2, slope2)**
Finds the intersection point of two lines given their points and slopes.

> **Parameters:**
* **p1:** *`Point`*
  * A `Point` object on the first line.
* **slope1:** *float*
  * The slope of the first line.
* **p2:** *`Point`*
  * A `Point` object on the second line.
* **slope2:** *float*
  * The slope of the second line.

> **Returns:**
* **intersection:** *`Point`*
  * The intersection point of the two lines.

***function* reverse_line(line)**
Reverses the direction of a `LineString`.

> **Parameters:**
* **line:** *`LineString`*
  * A `LineString` object to be reversed.

> **Returns:**
* **reversed_line:** *`LineString`*
  * The reversed `LineString`.

***function* split_line(line, interval)**
Splits a `LineString` into segments of a given interval length.

> **Parameters:**
* **line:** *`LineString`*
  * A `LineString` object to be split.
* **interval:** *float*
  * The length of each segment.

> **Returns:**
* **segments:** *list of `LineString`*
  * A list of `LineString` segments.

***function* break_line(line)**
Breaks a `LineString` into individual two-point segments.

> **Parameters:**
* **line:** *`LineString`*
  * A `LineString` object to be broken into two-point segments.

> **Returns:**
* **segments:** *list of `LineString`*
  * A list of two-point `LineString` segments.

***function* check_continuity(path)**
Checks the continuity of a path composed of `LineString` segments.

> **Parameters:**
* **path:** *list of `LineString`*
  * A list of `LineString` segments representing the path.

> **Returns:**
* **is_continuous:** *bool*
  * `True` if the path is continuous, `False` otherwise.