from outline import *
from graph import *
from basic_functions import *
import random
import csv

"""
============================
====== Path Generator ======
============================
"""

def generate_path(points: list, disp_diam, baseline_slope, vis = False, invert = False, children:list=None) -> Path:
    """
    A compacted set of commands to generate a function based on all the necessary informations
    
    points:         points of the polygon outline in a list of (longtitude, latitude)
    disp_diam:      dispersion diameter of the drone (m)
    baseline_slope: slope of the baseline (line that swath are perpendicular to)
    vis:            True for visualization of path
    invert:         True to show inverted path with same swath
    """
    coords = gcs2pcs_batch(points)
    if children:
        children = [Outline(gcs2pcs_batch(child)) for child in children]
    
    outline = Outline('outline', coords, children=children)
    offset_outline = outline.poly_offset(disp_diam / 2)
    path = offset_outline.swath_gen(disp_diam, baseline_slope, invert)
    
    #1st figure
    if vis:
      fig1 = plt.figure(figsize=(16, 8))
      fig1.suptitle("Full Coverage Drone Flight Path", fontsize=16)
      ax1 = fig1.add_subplot(1, 3, 1)
      ax2 = fig1.add_subplot(1, 3, 2, projection='3d')
      ax3 = fig1.add_subplot(1, 3, 3)
      
      path.path_disp(ax1)       #plot path
      path.airtime_print()      #print airtime
      path.coverage_print()     #print coverage
      path.length_print()       #print path length
      
      heights = randnum_list(len(path.path), 10, 30)
      velocity = [seg.curr_velo for seg in path.segment_list]
      show3DPath(ax2, path, ("height", heights))
      path.coverage_disp(ax3)   #plot coverage
      
      plt.tight_layout()
      plt.show()
    return path
    
    
"""
=====================
====== Testing ======
=====================
"""

""" lake1 =[[-119.3234427, 47.6949743],
            [-119.3014756, 47.349989],
            [-118.9774616, 47.52462],
            [-119.3069674, 47.6949743]] """

with open('coordinates.csv', 'r') as csvfile:
    next(csvfile)
    csv_reader = csv.reader(csvfile)
    coords = [(row[0], row[1]) for row in csv_reader]
path = generate_path(coords, 100, 0.2, vis=True, invert=True)


  





#Demonstrates what the returned data type looks like (list of LineString object)
""" print(np.array(path)) """