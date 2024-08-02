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
 
## Credits
This repository contains the work of *Michael Li*, *Jason Lee*, *Edward Cheng*, *Wendy Qi*, and *KiDrone*. Do not use or reference the contents of this repository without properly crediting its author.

<div align="center">
  <img src="https://github.com/user-attachments/assets/b0b72a19-e0f9-402d-aab6-2a135cb50f2f" alt="logo">
</div>
