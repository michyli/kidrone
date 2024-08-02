## optimization
An aggregation of functions to find the optimal `Path` instance given relevant weighting parameters. These functions help in constructing and evaluating various path configurations to determine the best possible path based on specified criteria.

## Methods

### construct_pathlist(coords, disp_diam, children=None, poly_offset=None, init_slope=-10, end_slope=10, num_path=10)
Constructs a list of possible paths given the initial parameters and returns a DataFrame with the path data and the runtime.

> **Parameters:**
* **coords:** *list of tuples*
  * A list of (x, y) coordinates representing the vertices of the base polygon.
* **disp_diam:** *float*
  * Dispersion diameter of the drone.
* **children:** *list of `Outline`, optional*
  * A list of `Outline` instances that are children of the base polygon. Defaults to None.
* **poly_offset:** *float, optional*
  * The offset distance for the polygon. Defaults to half the dispersion diameter.
* **init_slope:** *float, optional*
  * The initial slope for generating paths. Defaults to -10.
* **end_slope:** *float, optional*
  * The final slope for generating paths. Defaults to 10.
* **num_path:** *int, optional*
  * The number of paths to generate. Defaults to 10.

> **Returns:**
* **df:** *pandas.DataFrame*
  * A DataFrame containing the generated paths and their respective data.
* **runtime:** *float*
  * The time taken to generate the paths.

### find_best_path(pathdf, optimizer)
Finds the best path based on the provided optimizer function, which returns an index given a path.

> **Parameters:**
* **pathdf:** *pandas.DataFrame*
  * A DataFrame containing the path data.
* **optimizer:** *function*
  * A function that returns an index for selecting the best path.

> **Returns:**
* **pathdf:** *pandas.DataFrame*
  * The updated DataFrame with normalized values and the best path identified.
* **best_path:** *Path*
  * The best `Path` instance based on the optimization criteria.

### minmax_norm(col)
Normalizes a DataFrame column using Min-Max normalization.

> **Parameters:**
* **col:** *pandas.Series*
  * A column of a DataFrame to be normalized.

> **Returns:**
* **normalized_col:** *pandas.Series*
  * The normalized column.

> **Usage:**
1. Use `construct_pathlist` to generate a list of possible paths based on initial parameters.
2. Apply `find_best_path` with an appropriate optimizer function to determine the best path from the generated list.

## Credits
This repository contains the work of *Michael Li*, *Jason Lee*, *Edward Cheng*, *Wendy Qi*, and *KiDrone*. Do not use or reference the contents of this repository without properly crediting its author.

<div align="center">
  <img src="https://github.com/user-attachments/assets/b0b72a19-e0f9-402d-aab6-2a135cb50f2f" alt="logo">
</div>
