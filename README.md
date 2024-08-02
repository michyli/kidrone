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

## Credits
This repository contains the work of *Michael Li*, *Jason Lee*, *Edward Cheng*, *Wendy Qi*, and *KiDrone*. Do not use or reference the contents of this repository without properly crediting its author.

<div align="center">
  <img src="./Algorithm\ Documentation/Documentation\ Assets/kidrone_logo.jpeg" alt="logo">
</div>

