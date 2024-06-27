from polygoncreate import *
from graph import *
from basic_functions import *
import random

"""
============================
====== Path Generator ======
============================
"""

def generate_path(points: list, disp_diam, baseline_slope, vis = False, invert = False) -> Path:
    """
    A compacted set of commands to generate a function based on all the necessary informations
    
    points:         points of the polygon outline (in sequence)
    disp_diam:      dispersion diameter of the drone (m)
    baseline_slope: slope of the baseline (line that swath are perpendicular to)
    vis:            True for visualization of path
    invert:         True to show inverted path with same swath
    """
    outline = Outline(points)
    offset_outline = outline.poly_offset(disp_diam / 2)
    outline.showpoly([offset_outline])
    
    path = offset_outline.swath_gen(disp_diam, baseline_slope, invert, show_baseline=True)
    
    #Visualization
    if vis:
        showswath(path)
        plt.show()
        
    return path
    
    
"""
=====================
====== Testing ======
=====================
"""
#Example run: change 'eg' to other sets of points to change output
#Note: slope (the third input of generate_path) can be either a float or the string "vertical"

#Quadualateral
""" eg1 = [(12, 10), (20, 10), (20, 20), (10, 20)] 
path = generate_path(eg1, 1, 1, vis=True)
path.airtime_disp()
"""

#Hexalateral
""" eg2 = [(5, 9), (30, 6), (40, 20), (35, 37), (27, 41), (12, 30)]
path = generate_path(eg2, 2, 0.1, vis=True) """

#More complicated shape
#Demonstration of flying outside of designated area
""" eg3 = [(20, 10), (36, 19), (50, 15), (55, 22), (60, 38), (40, 40), (30, 50), (20, 43), (27, 30), (21, 20)] #More complicated shape
path = generate_path(eg3, 3, 9, vis=True)
"""


""" eg4 = [(20, 10), (36, 19), (50, 15), (55, 22), (60, 38), (40, 40), (30, 50), (20, 43), (27, 30), (21, 20)] #More complicated shape
path = generate_path(eg4, 1.5, 0.2, vis=True)

# values = [random.randint(6,10) for i in range(63)]
values = generate_height_values(63, 10, 30)
show3DPath(path, values) """

eg5 = [[-120.1833426, 47.7411704],[
        -119.9911309, 47.7651762],[
        -119.8758039, 47.8979308],[
        -119.6671169, 47.9935979],[
        -119.3321193, 48.0193242],[
        -118.9861382, 48.0119751],[
        -118.9559335, 47.9089783],[
        -118.5605266, 47.8776708],[
        -118.4982865, 47.7294713],[
        -118.7728747, 47.4980293],[
        -119.1188558, 47.2152152],[
        -119.9645873, 47.1648199],[
        -120.2748719, 47.4404731],[
        -120.181512, 47.7387076],[
        -120.1833426, 47.7411704]]
coords, func = pcs_reset(gcs2pcs_batch(eg5))
path = generate_path(coords, 20, 1, vis=True)


#Demonstrates what the returned data type looks like (list of LineString object)
""" print(np.array(path)) """