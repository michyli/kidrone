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

* [Matplotlib](https://matplotlib.org/)

* [NumPy](https://numpy.org/)

* [Shapely](https://pypi.org/project/shapely/)

* [pyproj](https://pyproj4.github.io/pyproj/stable/index.html)

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

#### Outline
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
* **point:** *`Point`*
* 
* **slope:** *`int`*
A number in meter indicating how much to inwardly-offset the polygon.
*Use negative number for outward offset*


#### Path

#### Segment

#### basic_functions

#### graph

#### optimization

#### run & .csv
* 


## Credits
This repository contains the work of *Michael Li*, *Jason Lee*, *Edward Cheng*, *Wendy Qi*, and *KiDrone*. Do not use or reference the contents of this repository without properly crediting its author.