# src/optimization.py
from outline import *
from graph import *
from basic_functions import *
import time
import pandas as pd

"""
=====================
=== Optimizations ===
=====================

An aggregation of functions to find optimal Path instance given relevant weighting parameters.
"""

def construct_pathlist(coords, disp_diam, children=None, poly_offset=None, init_slope=-10, end_slope=10, num_path=10):
    #Start Runtime Calc
    start_time = time.time()
    
    if isinstance(children, Outline):
        children = [children]
    
    if poly_offset is None:
        poly_offset = disp_diam / 2
    
    outline = Outline('BasePoly', coords, children)
    offset_outline = outline.poly_offset(poly_offset)
    
    pathdata = []
    for invert in [False, True]:
        for slope in [x for x in np.linspace(init_slope, end_slope, num_path)] + ["vertical"]:
            path = offset_outline.swath_gen(disp_diam, slope, invert)
            data = [path, path.airtime, path.seeding_coverage_efficiency, path.spilled_area]
            pathdata.append(data)
    df = pd.DataFrame(pathdata, columns=['Path', 'Airtime', 'Seeding_Efficiency', 'Spill_Area'])
    end_time = time.time()
    runtime = end_time - start_time
    return df, runtime

def find_best_path(pathdf, optimizer:tuple):
    """finds the best path based on optimizer, which is a function that returns an index given a path.
    """
    def minmax_norm(col):
        """col is a DataFrame column"""
        #Use Max-min normalization
        col = (col - col.min()) / (col.max() - col.min())
        return col
    
    pathdf['Airtime'] = minmax_norm(pathdf['Airtime'])
    pathdf['Seeding_Efficiency'] = minmax_norm(pathdf['Seeding_Efficiency'])
    pathdf['Spill_Area'] = minmax_norm(pathdf['Spill_Area'])
    optimizer(pathdf)
    return pathdf, pathdf.loc[pathdf['Composite_Score'] == pathdf['Composite_Score'].max()]['Path'].values[0]


"""
========================
====== Optimizers ======
========================
"""
def airtime_coverage_weighted(airtime_weight, seeding_weight, spill_weight):
    """optimized based on an airtime:seed_coverage:spill_coverage weighting ratio"""
    # normalize and map airtime and coverage to a stochastic number
    assert airtime_weight + seeding_weight + spill_weight == 100.0, "total ratio should add up to 100"
    airtime_weight /= 100
    seeding_weight /= 100
    spill_weight /= 100
    def func_constructor(pathdf):
        pathdf['Composite_Score'] = 100 * (pathdf.Airtime * airtime_weight + pathdf.Seeding_Efficiency * seeding_weight - pathdf.Spill_Area * spill_weight)
    return func_constructor
    
