import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from basic_functions import *

"""
An aggregation of all graphing functions
"""
def showpoly(ax, polygons, label=None, color=None):
        """Plots polygon
        ax:         The axes to plot on
        polygon:    an Outline objects to be graphed
        """
        if polygons.children:
            for child in polygons.children:
                showpoly(ax, child, color="darkcyan")
     
        xx, yy = polygons.polygon.exterior.xy
        ax.plot(xx, yy, '-.', color=color, label=label, ms=4)
        return ax

def showprojection(ax, full_path):
    """
    Plots the baseline and field projection on the XY plane.
    
    ax: The 3D axis object to plot on.
    full_path: a Path object. The .path attribute extracts the list of LineString that makes the Path object.
    """
    #plot projected path
    for lines in full_path.path:
        start, end = lines.coords[0], lines.coords[1]
        xx, yy = [start[0], end[0]], [start[1], end[1]]
        zz = [0, 0]  # Baseline at z=0
        ax.plot(xx, yy, zz, 'k--', ms=4, linewidth=1)
    
    #plot field outline
    if full_path.parent.offsetparent:
        x1, y1 = full_path.parent.offsetparent.polygon.exterior.xy
        ax.plot(x1, y1, 0, color="teal", linestyle="-.")
        x2, y2 = full_path.parent.polygon.exterior.xy
        ax.plot(x2, y2, 0, color="paleturquoise", linestyle=":")
    else:
        x1, y1 = full_path.parent.polygon.exterior.xy
        ax.plot(x1, y1, 0, color="teal", linestyle=":")

def show3DPath(ax, full_path, z_values):
    """
    Plots the complete 3D path.
    
    full_path: a Path object. The .path attribute extracts the list of LineString that makes the Path object.
    values: an iterable (e.g., list, numpy array) with the same length as the number of lines in Path.
            Can represent velocity, height, etc.
    """
    #Determine what the z-parameter is
    name, z_val = z_values[0], z_values[1]
    
    # Plot each LineString with its start and end points at the correct height
    for lines, (start_value, end_value) in zip(full_path.path, z_val):
        start, end = lines.coords[0], lines.coords[1]
        xx, yy = [start[0], end[0]], [start[1], end[1]]
        zz = [start_value, end_value]
        ax.plot(xx, yy, zz, color='g', linestyle='-', marker=None, linewidth=2.5)
        
        # Plot vertical lines to connect path and baseline
        ax.plot([start[0], start[0]], [start[1], start[1]], [0, start_value], 'r-.', linewidth=1, alpha=0.5)
        ax.plot([end[0], end[0]], [end[1], end[1]], [0, end_value], 'r-.', linewidth=1, alpha=0.5)

    showprojection(ax, full_path)

    ax.set_title(f"3D View with {name.capitalize()}")
    ax.set_xlabel('x (m)')
    ax.set_ylabel('y (m)')
    ax.xaxis.set_major_locator(ticker.NullLocator())
    ax.yaxis.set_major_locator(ticker.NullLocator())
    ax.zaxis.set_major_locator(plt.MaxNLocator(4))
    ax.set_zlabel(f'{name} ({"KM/h" if name=="velocity" else "m"})')
    ax.set_box_aspect((2,2,1.5))