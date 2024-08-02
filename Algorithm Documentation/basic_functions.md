## basic_functions
A collection of general-purpose functions used throughout the algorithm to manipulate Shapely datatypes and vectors. These functions are essential for various operations related to polygons, vectors, and line segments.

## Methods

### extractGeoTypes(geometry)
Takes a Shapely geometry instance and returns the individual polygons in a list.

> **Parameters:**
* **geometry:** *Shapely geometry*
  * A Shapely geometry instance (e.g., `MultiPolygon`, `Polygon`).

> **Returns:**
* **polygons:** *list of `Polygon`*
  * A list of individual polygons extracted from the input geometry.

### normalizeVec(x, y, z=0)
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

### line_slope(line)
Returns the slope of a `LineString` based on its boundary points.

> **Parameters:**
* **line:** *`LineString`*
  * A `LineString` object.

> **Returns:**
* **slope:** *float or str*
  * The slope of the line or "vertical" if the line is vertical.

### pt_to_line(point, line)
Projects a point onto a line and returns the projected point.

> **Parameters:**
* **point:** *`Point`*
  * A `Point` object to be projected.
* **line:** *`LineString`*
  * A `LineString` object on which the point will be projected.

> **Returns:**
* **projected_point:** *`Point`*
  * The point projected onto the line.

### function* line_intersection(p1, slope1, p2, slope2)
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

### reverse_line(line)
Reverses the direction of a `LineString`.

> **Parameters:**
* **line:** *`LineString`*
  * A `LineString` object to be reversed.

> **Returns:**
* **reversed_line:** *`LineString`*
  * The reversed `LineString`.

### split_line(line, interval)**
Splits a `LineString` into segments of a given interval length.

> **Parameters:**
* **line:** *`LineString`*
  * A `LineString` object to be split.
* **interval:** *float*
  * The length of each segment.

> **Returns:**
* **segments:** *list of `LineString`*
  * A list of `LineString` segments.

### break_line(line)**
Breaks a `LineString` into individual two-point segments.

> **Parameters:**
* **line:** *`LineString`*
  * A `LineString` object to be broken into two-point segments.

> **Returns:**
* **segments:** *list of `LineString`*
  * A list of two-point `LineString` segments.

### check_continuity(path)**
Checks the continuity of a path composed of `LineString` segments.

> **Parameters:**
* **path:** *list of `LineString`*
  * A list of `LineString` segments representing the path.

> **Returns:**
* **is_continuous:** *bool*
  * `True` if the path is continuous, `False` otherwise.

## Credits
This repository contains the work of *Michael Li*, *Jason Lee*, *Edward Cheng*, *Wendy Qi*, and *KiDrone*. Do not use or reference the contents of this repository without properly crediting its author.

<div align="center">
  <img src="https://github.com/user-attachments/assets/b0b72a19-e0f9-402d-aab6-2a135cb50f2f" alt="logo">
</div>
