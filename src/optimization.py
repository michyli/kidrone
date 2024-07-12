# src/optimization.py

from .outline import *
from .graph import *
from .basic_functions import *
import time

"""
==========================
====== Optimization ======
==========================
"""
def construct_best_path(coords, disp_diam, children=None, init_slope=-10, end_slope=10, num_path=2):
    """Construct the best path based on shortest airtime and measure runtime."""
    #Start Runtime Calc
    start_time = time.time()
    
    if isinstance(children, Outline):
        children = [children]
    
    outline = Outline('BasePoly', coords, children)
    offset_outline = outline.poly_offset(disp_diam / 2)
    best_path = None
    min_airtime = float('inf')
    
    for invert in [False, True]:
        for slope in np.linspace(init_slope, end_slope, num_path):
            path = offset_outline.swath_gen(disp_diam, slope, invert)
            if path.airtime < min_airtime:
                best_path = path
                min_airtime = path.airtime
        path = offset_outline.swath_gen(disp_diam, "vertical", invert)
        #Check for vertical slope
        if path.airtime < min_airtime:
                best_path = path
                min_airtime = path.airtime

    #Runtime Calc
    end_time = time.time()
    runtime = end_time - start_time
    return best_path, runtime




def weighted_runairtime(air_weigh, coverage_weigh):
    """optimized based on an airtime:coverage weighting ratio"""
    # normalize and map airtime and coverage to a stochastic number
    #! ON HOLD
    pass
