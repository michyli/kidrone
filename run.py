from polygoncreate import *
from basic_functions import *

"""
============================
====== Path Generator ======
============================
"""

def generate_path(points, disp_diam, baseline_slope, vis = False, invert = False):
    """
    A compacted set of commands to generate a function based on all the necessary informations
    """
    outline = PolygonCreate(points)
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
path = generate_path(eg1, 1, 1, vis=True)  """

#Hexalateral
""" eg2 = [(5, 9), (30, 6), (40, 20), (35, 37), (27, 41), (12, 30)]
path = generate_path(eg2, 2, 0.1, vis=True) """

#More complicated shape
#Demonstration of flying outside of designated area
""" eg3 = [(20, 10), (36, 19), (50, 15), (55, 22), (60, 38), (40, 40), (30, 50), (20, 43), (27, 30), (21, 20)] #More complicated shape
path = generate_path(eg3, 3, 9, vis=True) """

eg4 = [(20, 10), (36, 19), (50, 15), (55, 22), (60, 38), (40, 40), (30, 50), (20, 43), (27, 30), (21, 20)] #More complicated shape
path = generate_path(eg4, 0.8, 0.5, vis=True)

#Demonstrates what the returned data type looks like (list of LineString object)
"""print(np.array(path))"""

"""
#Test line_angle function

#Expected 168.69...
line1 = LineString([(0, 0), (1, 1)])
line2 = LineString([(1, 1), (3, 4)])
print(line_angle(line1, line2))

#Expected 65.22...
line1 = LineString([(0, 0), (-1, -2)])
line2 = LineString([(4, -5), (0, 0)])
print(line_angle(line1, line2))

#Expected ValueError
line1 = LineString([(0, 0), (1, 1)])
line2 = LineString([(2, 2), (3, 4)])
print(line_angle(line1, line2))

"""

