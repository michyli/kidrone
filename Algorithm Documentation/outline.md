### Outline
***class* Outline(name, points, children=[])**
An `Outline` instance contains all the necessary information about the polygon constructed from the given points. It also contains all the methods required to generate a flight path to fully cover it. Using `swath_gen` method, a `Path` instance will be returned.
> **Parameters:**
* **name:** *string*
A string that represents the name of the Outline instance
* **points:** *list of iterables*
A list of points in (x, y) format, representing x, y coordinates of the vertices of a polygon, in the coordinate system of EPSG:3857.
* **children:** *list of `Outline` instances*
A list that has all the polygons that are fully contained within the Outline instance.
*Defaults to an empty list*
* **_offsetparent:** *an `Outline` instance*
Stores the `Outline` instance that the current `Outline` was offsetted from.
*Defaults to None*
> **Attributes:**
* **xcoord:** *list[int]*
A list of all the x-coordinates in sequence
* **ycoord:** *list[int]*
A list of all the y-coordinates in sequence
* **points:** *`Point`*
A list of Point instances (Shapely) constructed with given points
* **ring:** *`LineString`*
A LinearRing instance (Shapely) constructed with given points
* **polygon:** *`Polygon`*
A Polygon instance (Shapely) constructed with given points
* **cenctroid:** *`Point`*
A Point instance that represents the geometric center of the polygon
* **area:** *unit: km^2*
Area of the polygon in kilometers squared.

***method* poly_offset(self, offset)**
Offsets the polygon by a specific amount to create a buffer area. Returns a new `Outline` instance with a link back to the original `Outline` via the attribute `offsetparent`.
> **Parameters:**
* **offset:** *unit: m*
A distance in meters indicating how much to inwardly-offset the polygon.
*Use negative number for outward offset*

***method* extrapolate_line(self, point, slope)**
Creates and extends a line to the minimum bounding box of the polygon based on the given point and the slope
> **Parameters:**
* **point:** *`Point`*:
A `Point` object that anchors the line
* **slope:** *`int`*
A number in meter indicating how much to inwardly-offset the polygon.
*Use negative number for outward offset*

***method* span_line(self, line)**
Crops part of the LineString that exceeds the boundary of the polygon. Also crops a line to segments if it intersects with any children polygons of the self polygon. Returns the new cropped `LineString`
> **Parameters:**
* **line** *`LineString`*
A `LineString` object that intersects the polygon

***method* swath_gen(self, interval, slope, invert=False, _F_single_point=False, _R_single_point=False)**
Generates evenly spaced swatch lines based on a baseline. The baseline is a line that passes through the centroid with the input slope. Returns a complete path, which is a list of `LineString`s
> **Parameters:**
* **interval** *`float`*
Dispersion diameter of the drone
* **slope** *`float`*
The slope of the baseline (wind direction) in respect to the horizontal line
* **invert** *`boolean`*
Determines whether the path generated goes in the default direction (False) or inverted direction (True)
* **_F_single_point** *`boolean`*
Determines whether there is a single-point intersection between the swath line and the polygon at the front of the path
* **_R_single_point** *`boolean`*
Determines whether there is a single-point intersection between the swath line and the polygon at the rear of the path

***method* children_setter(self, children)**
Populates children polygons of Outline instances in a hashmap. The children of an Outline are always completely contained within its borders
> **Parameters:**
* **children** *`Outline`*
A list of children `Outline` instances to be set

***method* show_children(self)**
Output the name of every single children contained within an Outline instance

***method* add_child(self, child)**
Adds a child to the polygon's list of children
> **Parameters:**
* **child** *`Outline`*
An `Outline` object to be added as a child

***method* remove_child(self, child)**
Removes a child from the polygon's list of children
> **Parameters:**
* **child** *`Outline`*
An `Outline` object to be removed from this instance of an `Outline`

## Credits
This repository contains the work of *Michael Li*, *Jason Lee*, *Edward Cheng*, *Wendy Qi*, and *KiDrone*. Do not use or reference the contents of this repository without properly crediting its author.

<div align="center">
  <img src="https://github.com/user-attachments/assets/b0b72a19-e0f9-402d-aab6-2a135cb50f2f" alt="logo">
</div>
