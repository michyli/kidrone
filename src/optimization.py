# src/optimization.py

from outline import *
from graph import *
from basic_functions import *
import time

"""
============================
====== Path Generator ======
============================
"""


def generate_path(points: list, disp_diam, baseline_slope, invert=False, children: list = None) -> Path:
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


def check_airtime_and_update_best_path(coords, disp_diam, slope, invert, best_path, min_airtime):
    """Check airtime for a generated path and update the best path if it has a shorter airtime."""
    path = generate_path(coords, disp_diam, slope, invert)
    if path.airtime < min_airtime:
        return path, path.airtime
    return best_path, min_airtime


"""
==========================
====== Optimization ======
==========================
"""


def construct_best_path(coords, disp_diam, init_slope=-10, end_slope=10, num_path=2):
    """Construct the best path based on shortest airtime and measure runtime."""
    start_time = time.time()

    best_path = None
    min_airtime = float('inf')

    for slope in np.linspace(init_slope, end_slope, num_path):
        for invert in [False, True]:
            best_path, min_airtime = check_airtime_and_update_best_path(
                coords, disp_diam, slope, invert, best_path, min_airtime)

    for invert in [False, True]:
        best_path, min_airtime = check_airtime_and_update_best_path(
            coords, disp_diam, "vertical", invert, best_path, min_airtime)

    end_time = time.time()
    runtime = end_time - start_time

    return best_path, runtime


def weighted_runairtime(air_weigh, coverage_weigh):
    """optimized based on an airtime:coverage weighting ratio"""
    # normalize and map airtime and coverage to a stochastic number
    pass
