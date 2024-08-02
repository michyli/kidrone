# KiDrone Drone Path Planning

This Full-Stack application enables users to upload ShapeFiles containing real-world coordinates and generates an optimized drone flight path. The path is designed to maximize area coverage while minimizing overall air time. View the design intent of the overall application [here](https://docs.google.com/document/d/13txw84tOc-ipvObAjZp5-afF4HjbdMIu_Dmh2Kdlvos/edit#heading=h.3xltt7wt8ggh). 

All rights reserved by Ki.

## Overview

1. [Requirements](#requirements)
2. [Instructions](#instructions)
3. [Algorithm Description](#desctiption)
4. [Progress](#progress)
5. [Credits](#credits)

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
3. Install the LiveServer extension in VSCode__
   
4. cd into the directory of the repo
```
cd kidrone
```
5. View the raw HTML in ```electron/gui/pages```. Right click the page and click Open with LiveServer to start a static Front-End session__

6. Start the electron app by cd-ing into ```electron/gui```. Run ```npm install``` to download electron, and then ```npm start``` to start the application__

## Algorithm Description

The core algorithm classes can be located at ```electron/engine```. The overall algorithm is implemented using a **Boustrophedon Cellular Decomposition**. For further clarity on this algorithm, see the description [here](https://docs.google.com/document/d/13txw84tOc-ipvObAjZp5-afF4HjbdMIu_Dmh2Kdlvos/edit#heading=h.3xltt7wt8ggh) at the subheading **Method of Boustrophedon Path Generation**. Further details can be found at the directory ```Path Planner Papers```.

### Classes
- [Outline](Algorithm%20Documentation/outline.md)
- [Path](Algorithm%20Documentation/path.md)
- [Segment](Algorithm%20Documentation/segment.md)
- [basic_functions](Algorithm%20Documentation/basic_functions.md)
- [graph](Algorithm%20Documentation/graph.md)
- [optimization](Algorithm%20Documentation/optimisation.md)

## Progress
This project is currently **In Progress**. For those next working on the project, the front-end files can be located as ```electron/gui/pages```, and please see the KiDrone Figma Mockups to view the application's final desired look. The backend files are located at ```electron/gui```, and ```main.js``` controls the overall logic. For further details on the state of this project, please see the **Why Electron** and **Future Plans** subheading at the document [here](https://docs.google.com/document/d/13txw84tOc-ipvObAjZp5-afF4HjbdMIu_Dmh2Kdlvos/edit#heading=h.3xltt7wt8ggh). 

## Credits
This repository contains the work of *Michael Li*, *Jason Lee*, *Edward Cheng*, *Wendy Qi*, and *KiDrone*. Do not use or reference the contents of this repository without properly crediting its author.

<div align="center">
  <img src="https://github.com/user-attachments/assets/b0b72a19-e0f9-402d-aab6-2a135cb50f2f" alt="logo">
</div>

