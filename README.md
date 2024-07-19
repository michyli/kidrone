# KiDrone Drone Path Planning

This is an algorithm that generates the optimal flight path for a drone over a terrain with given constrains.

- [KiDrone Drone Path Planning](#kidrone-drone-path-planning)
  - [Requirements](#requirements)
  - [Instructions](#instructions)
  - [Structures](#structures)
      - [Outline](#outline)
      - [Path](#path)
      - [Segment](#segment)
      - [basic\_functions](#basic_functions)
      - [graph](#graph)
      - [optimization](#optimization)
      - [run \& .csv](#run--csv)
  - [Credits](#credits)

## Requirements

For running the code:
* [Python (>v3.9)](https://www.python.org/downloads/)

* [Matplotlib](https://matplotlib.org/)

* [NumPy](https://numpy.org/)

* [pandas](https://pandas.pydata.org/)

* [Shapely](https://pypi.org/project/shapely/)

* [pyproj](https://pyproj4.github.io/pyproj/stable/index.html)

* [Flask](https://flask.palletsprojects.com/en/3.0.x/)

For development:

* [pytest](https://docs.pytest.org/en/8.2.x/) (for unit tests)

* [mypy](https://mypy-lang.org/) (for type checks)


## Instructions
1. Clone this repo
```
git clone https://github.com/michyli/kidrone.git
```
2. Install the required libraries
```
pip install -r requirements.txt
```
3. cd into the directory of the repo
```
cd kidrone
```
4. Generate coordinates from [here](https://www.keene.edu/campus/maps/tool/), and paste them into *coordinates.csv*
5. Test using the `run.py` file
```
py run.py
```

## Structures
* *class* Outline - `outline.py`
  * `poly_offset`
  * `extrapolate_line`
  * `span_line`
  * `swath_gen`
* *class* Path - `path.py`
  * `path_offset`
  * `path_disp`
  * `coverage`
  * `coverage_disp`
  * `coverage_print`
  * `airtime_print`
  * `length_print`
* *class* Segment - `segment.py`
  * `time_setter`

<br>

* `basic_functions.py`
* `graph.py`
* `optimization.py`
* `run.py` & `test_coordinates.csv`

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

### Path
***class* Path(path, parent, disp_diam, swath_slope, start_velo=0, end_velo=0)**
A `Path` instance contains all necessary information about the flight path and is contructed from a series of `LineString` objects. This class allows for the generation of waypoints, calculation of flight duration, and path optimization based on drone velocity and acceleration. Additionally, it offers capabilities to visualize, save, and load the path, making it a comprehensive tool for drone flight path management.

> **Parameters:**
* **path:** *list of `LineString`s*
  * A list of `LineString`s. Usually the output of the `generate_path()` function.
* **parent:** *`Outline` instance*
  * The polygon object the path belongs to.
* **disp_diam:** *float*
  * Dispersion diameter of the drone.
* **swath_slope:** *float*
  * The slope of the swath lines of this `Path` instance.
* **start_velo:** *float*
  * Starting velocity of this path, static (0) by default.
* **end_velo:** *float*
  * Ending velocity of this path, static (0) by default.

***method* generate_waypoints(self, interval)**
Generates waypoints along the path at specified intervals.

> **Parameters:**
* **interval:** *float*
  * Distance between waypoints in meters.

***method* calculate_duration(self)**
Calculates the duration required to traverse the path based on drone velocities.

***method* optimize_path(self)**
Optimizes the path for the shortest duration considering drone's acceleration and deceleration capabilities.

***method* get_segments(self)**
Breaks the path into smaller segments for detailed analysis.

> **Attributes:**
* **segments:** *list of `Segment`*
  * A list of `Segment` instances that make up the path.

***method* display_path(self, show=True)**
Displays the path on a map.

> **Parameters:**
* **show:** *bool*
  * Determines whether to display the path immediately. Defaults to `True`.

***method* save_path(self, filename)**
Saves the path to a file.

> **Parameters:**
* **filename:** *string*
  * Name of the file to save the path.

***method* load_path(self, filename)**
Loads a path from a file.

> **Parameters:**
* **filename:** *string*
  * Name of the file to load the path from.

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


###graph
A collection of functions used for graphing and visualizing various elements such as polygons and paths. These utilities help in plotting and animating drone flight paths and related geometries.

> **Functions:**

***function* showpoly(ax, polygons, label=None, color=None)**
Plots a polygon on the given axes.

> **Parameters:**
* **ax:** *matplotlib.axes.Axes*
  * The axes to plot on.
* **polygons:** *Outline*
  * An `Outline` object to be graphed.
* **label:** *str, optional*
  * A label for the polygon. Defaults to None.
* **color:** *str, optional*
  * Color for the polygon. Defaults to None.

> **Returns:**
* **ax:** *matplotlib.axes.Axes*
  * The axes with the plotted polygon.

***function* showpath(path)**
Plots all relevant information about a path, including the path itself, airtime, coverage, and path length.

> **Parameters:**
* **path:** *Path*
  * A `Path` instance to be plotted.

***function* showprojection(ax, full_path)**
Plots the baseline and field projection on the XY plane.

> **Parameters:**
* **ax:** *matplotlib.axes._subplots.Axes3DSubplot*
  * The 3D axis object to plot on.
* **full_path:** *Path*
  * A `Path` object. The `.path` attribute extracts the list of `LineString`s that make up the `Path` object.

***function* animatepath(path, interval=200)**
Animates the drone flight path over time.

> **Parameters:**
* **path:** *Path*
  * A `Path` instance to be animated.
* **interval:** *int, optional*
  * Interval between frames in milliseconds. Defaults to 200.

***function* saveanimation(anim, filename)**
Saves the animation to a file.

> **Parameters:**
* **anim:** *matplotlib.animation.FuncAnimation*
  * The animation object to be saved.
* **filename:** *str*
  * Name of the file to save the animation.

***function* plot3Dsurface(X, Y, Z, title="3D Surface Plot")**
Plots a 3D surface plot.

> **Parameters:**
* **X:** *array-like*
  * The X coordinates of the surface.
* **Y:** *array-like*
  * The Y coordinates of the surface.
* **Z:** *array-like*
  * The Z values of the surface.
* **title:** *str, optional*
  * Title of the plot. Defaults to "3D Surface Plot".

***function* plot3Dscatter(X, Y, Z, title="3D Scatter Plot")**
Plots a 3D scatter plot.

> **Parameters:**
* **X:** *array-like*
  * The X coordinates of the scatter plot.
* **Y:** *array-like*
  * The Y coordinates of the scatter plot.
* **Z:** *array-like*
  * The Z values of the scatter plot.
* **title:** *str, optional*
  * Title of the plot. Defaults to "3D Scatter Plot".

***function* plot2Dcontour(X, Y, Z, title="2D Contour Plot")**
Plots a 2D contour plot.

> **Parameters:**
* **X:** *array-like*
  * The X coordinates of the contour plot.
* **Y:** *array-like*
  * The Y coordinates of the contour plot.
* **Z:** *array-like*
  * The Z values of the contour plot.
* **title:** *str, optional*
  * Title of the plot. Defaults to "2D Contour Plot".
``` &#8203;:citation[oaicite:0]{index=0}&#8203;

### optimization

### run & .csv
* 


## Credits
This repository contains the work of *Michael Li*, *Jason Lee*, *Edward Cheng*, *Wendy Qi*, and *KiDrone*. Do not use or reference the contents of this repository without properly crediting its author.
