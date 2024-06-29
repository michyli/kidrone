from outline import *
from graph import *
from basic_functions import *

"""
============================
====== Path Generator ======
============================
"""
def generate_path(points: list, disp_diam, baseline_slope, invert = False, children:list=None) -> Path:
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
    
    return path


"""
==========================
====== Optimization ======
==========================
"""
def path_list_constructor(coords, disp_diam, init_slope=-10, end_slope=10, num_path=50):
    """construct a list of path to iterate through"""
    pathlist = []
    for slope in np.linspace(init_slope, end_slope, num_path):
        path_uninv = generate_path(coords, disp_diam, slope, invert=False)
        path_inv = generate_path(coords, disp_diam, slope, invert=True)
        pathlist.append(path_uninv)
        pathlist.append(path_inv)
    return pathlist

def optimizer(pathlist, op_func):
    """returns and visualizes the path with minimal optimizing parameter"""
    min_time_path = min(pathlist, key=op_func)
    return min_time_path

def shortest_airtime():
    """optimize based on shortest airtime"""
    return lambda path: path.airtime

def weighted_runairtime(air_weigh, coverage_weigh):
    """optimized based on an airtime:coverage weighting ratio"""
    #normalize and map airtime and coverage to a stochastic number
    pass

