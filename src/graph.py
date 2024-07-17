import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import animation
from matplotlib.animation import PillowWriter
from .basic_functions import *

"""
==========================
=== Graphing Utilities ===
==========================

Aggregation of all graphing related functions
"""

def showpoly(ax, polygons, label=None, color=None):
    """Plots polygon
    ax:         The axes to plot on
    polygon:    an Outline objects to be graphed
    """
    if polygons.children:
        for child in polygons.children.values():
            showpoly(ax, child, color="darkcyan")

    xx, yy = polygons.polygon.exterior.xy
    ax.plot(xx, yy, '-.', color=color, label=label, ms=4)
    return ax


def showpath(path):
    """plot all relevant information about the path
    path: a Path instance
    """
    fig1 = plt.figure(figsize=(16, 8))
    fig1.suptitle("Full Coverage Drone Flight Path", fontsize=16)
    ax1 = fig1.add_subplot(1, 2, 1)
    ax2 = fig1.add_subplot(1, 2, 2)

    path.path_display(ax1)             # plot path
    print(path.airtime_print())     # print airtime
    print(path.coverage_print())    # print coverage
    print(path.length_print())      # print path length
    
    path.coverage_disp(ax2)  # plot coverage

    plt.tight_layout()
    plt.show()


def showprojection(ax, full_path):
    """
    Plots the baseline and field projection on the XY plane.

    ax: The 3D axis object to plot on.
    full_path: a Path object. The .path attribute extracts the list of LineString that makes the Path object.
    """
    # plot projected path
    for lines in full_path.path:
        start, end = lines.coords[0], lines.coords[1]
        xx, yy = [start[0], end[0]], [start[1], end[1]]
        zz = [0, 0]  # Baseline at z=0
        ax.plot(xx, yy, zz, 'k--', ms=4, linewidth=1)

    # plot field outline
    if full_path.parent.offsetparent:
        x1, y1 = full_path.parent.offsetparent.polygon.exterior.xy
        ax.plot(x1, y1, 0, color="teal", linestyle="-.")
        x2, y2 = full_path.parent.polygon.exterior.xy
        ax.plot(x2, y2, 0, color="paleturquoise", linestyle=":")
    else:
        x1, y1 = full_path.parent.polygon.exterior.xy
        ax.plot(x1, y1, 0, color="teal", linestyle=":")


def show3Dpath(full_path, plottype="coarse", gif=False):
    """
    Plots the complete 3D path.

    full_path: a Path object. The .path attribute extracts the list of LineString that makes the Path object.
    plottype: 'dense' or 'coarse'
    """
    print()
    print("Generating 3D Plot of the Path. Ctrl-C to abort.")   
    
    if plottype == 'coarse':
        reference_line = full_path.path
        dispersion_map = full_path.disp_map
        elevation = full_path.critical_elevations
    elif plottype == 'dense':
        reference_line = full_path.waypoints_path
        dispersion_map = full_path.waypoints_disp_map
        elevation = full_path.waypoint_elevations
    else:
        raise ValueError(f"There isn't enough z-values to plot for the path. There are {len(full_path.coords)} points in path and only {len(elevation)} z-values.")
    
    label_helper_disp = False  # Create tracking variable so only 1 label appears on legend
    label_helper_nondisp = False
    
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    # Plot each LineString with its start and end points at the correct height
    for index, lines in enumerate(reference_line):
        
        start, end = lines.coords[0], lines.coords[1]
        xx, yy = [start[0], end[0]], [start[1], end[1]]
        zz = [elevation[index], elevation[index+1]]
        if dispersion_map[index]:
            if label_helper_disp:
                ax.plot(xx, yy, zz, color='g', linestyle='-',
                        marker=None, linewidth=2.5)
            else:
                ax.plot(xx, yy, zz, color='g', linestyle='-',
                        marker=None, linewidth=2.5, label='dispersing')
                label_helper_disp = True
        else:
            if label_helper_nondisp:
                ax.plot(xx, yy, zz, color='b', linestyle='-',
                        marker=None, linewidth=2.5)
            else:
                ax.plot(xx, yy, zz, color='b', linestyle='-',
                        marker=None, linewidth=2.5, label='non-dispersing')
                label_helper_nondisp = True
            ax.plot([start[0], start[0]], [start[1], start[1]], [
                0, elevation[index]], 'r-.', linewidth=1, alpha=0.25)
            ax.plot([end[0], end[0]], [end[1], end[1]], [
                0, elevation[index+1]], 'r-.', linewidth=1, alpha=0.25)

    showprojection(ax, full_path)

    ax.set_title("3D View with Elevation")
    ax.set_xlabel('x (m)')
    ax.set_ylabel('y (m)')
    ax.xaxis.set_major_locator(ticker.NullLocator())
    ax.yaxis.set_major_locator(ticker.NullLocator())
    ax.zaxis.set_major_locator(plt.MaxNLocator(4))
    ax.set_zlabel('Elevation (m)')
    ax.set_box_aspect((2, 2, 1.5))
    
    #Set background color of plot to bg_color
    """
    bg_color = "#F2F7CA"
    fig.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)
    ax.xaxis.set_pane_color(bg_color)
    ax.yaxis.set_pane_color(bg_color)
    ax.zaxis.set_pane_color(bg_color)
    """
    
    if gif:
        #Make a .gif animation file of the 3D plot
        def init():
            ax.view_init(elev=30., azim=0)
            return [fig]
        def animate(i):
            ax.view_init(elev=30., azim=i)
            return [fig]

        # Animate
        print("Generating .gif file in the directory...")
        anim = animation.FuncAnimation(fig, animate, init_func=init,
                                    frames=360, interval=10, blit=True)
        # Save
        #anim.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
        writer = PillowWriter(fps=30)
        anim.save('basic_animation.gif', writer=writer)
    else:
        ax.legend()
        plt.show()
