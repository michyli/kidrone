### graph
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
 
## Credits
This repository contains the work of *Michael Li*, *Jason Lee*, *Edward Cheng*, *Wendy Qi*, and *KiDrone*. Do not use or reference the contents of this repository without properly crediting its author.

<div align="center">
  <img src="https://github.com/user-attachments/assets/b0b72a19-e0f9-402d-aab6-2a135cb50f2f" alt="logo">
</div>
