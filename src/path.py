# src/path.py

from .basic_functions import *
from .segment import *
from .graph import *
import math
from shapely.geometry import LineString


class Path:
    """
    Path class processes the path object and extracts information about the path.
    """

    def __init__(self, path: list[LineString], parent, disp_diam, swath_slope, start_velo=0, end_velo=0):
        """
        path:           a list of LineStrings. Usually the output of generate_path() function
        parent:         the polygon object the path belongs to
        swath_slope:    the slope of the swath lines of this path instance
        start_velo:     starting velocity of this path, static (0) by default
        end_velo:     ending velocity of this path, static (0) by default
        """
        self.path = path
        self.parent = parent
        self.disp_diam = disp_diam
        self.swath_slope = swath_slope

        # Assuming drone starts from and ends on static
        self.start_velo = start_velo  # KM/h
        self.end_velo = end_velo  # KM/h

        """
        Parameters used:
        1) Dispersing velocity:                         100km/h
        2) Max non-dispersing velocity:                 200km/h
        3) Turning velocity (90deg):                    50km/h
            *Scales linearly with angle
        4) Min. acceleration / Deceleration distance:   0.1km (100m)
        5) Acceleration / Deceleration:                 Linear
        """
        self.disp_velo = 100  # KM/h
        self.nondisp_velo = 200  # KM/h
        # KM, minimum distance for drone to accelerate or decelerate to disp_velo
        self.turn_dist = 0.1

        self.disp_map = self.disp_map_setter()
        self.pathlength = self.pathlength_setter()
        self.segment_list = self.segment_list_setter()
        self.airtime = self.airtime_setter()

    def to_coordinates(self):
        """
        Transforms projected coordinates to geographic coordinates and returns a detailed list of
        dictionaries, each representing a line segment with its start and end geographic coordinates.
        """
        detailed_coords = []
        path_coords = []  # List to hold all coordinates for batch transformation

        for line in self.path:
            # Extract and collect all points for transformation
            start_point = line.coords[0]
            end_point = line.coords[-1]
            path_coords.extend([start_point, end_point])

        # Convert all collected points from EPSG:3857 to EPSG:4326
        # transformed_coords = pcs2gcs_batch(coords_to_transform)

        # Iterate over transformed coordinates in pairs (start, end)
        for i in range(0, len(path_coords), 2):
            start_geo = path_coords[i]
            end_geo = path_coords[i + 1]
            detailed_coords.append({
                'start': {'x': start_geo[0], 'y': start_geo[1]},
                'end': {'x': end_geo[0], 'y': end_geo[1]}
            })

        return detailed_coords

    def path_offset(self, wind_dir, height, seed_weight):
        """Returns an offsetted path based on the wind direction, drone height, and seed weight.

        wind_dir:       a tuple containing the x and y components of the wind vector
        height:         constant height the drone aims to travel at (m)
        seed_weight:    weight of the seed (kg)
        """
        # Constants
        g = 9.81  # Acceleration due to gravity (m/s^2)

        # Time it takes for the seed to fall from the given height
        fall_time = math.sqrt((2 * height) / g)

        # Wind displacement during the fall time
        wind_displacement_x = wind_dir[0] * fall_time
        wind_displacement_y = wind_dir[1] * fall_time

        # Offset the path by the wind displacement
        offset_x = wind_displacement_x
        offset_y = wind_displacement_y

        offset_path = []
        for line in self.path:
            offset_coords = [(x + offset_x, y + offset_y)
                             for x, y in line.coords]
            offset_path.append(LineString(offset_coords))

        return offset_path

    """
    ===============
    === Display ===
    ===============
    """

    def path_disp(self, ax):
        """Plots the complete path
        full_path:  a Path object. the .path attribute extracts the list of LineString that makes the Path object
        ax:         The axes to plot on
        """
        showpoly(ax, self.parent, color="lightcyan")
        if self.parent.offsetparent:
            showpoly(ax, self.parent.offsetparent,
                     label="Field Outline", color="teal")

        label_helper_disp = False  # Create tracking variable so only 1 label appears on legend
        label_helper_nondisp = False
        for i, lines in enumerate(self.path):
            start, end = lines.coords[0], lines.coords[1]
            xx, yy = [start[0], end[0]], [start[1], end[1]]
            if i == 0:
                # store starting point
                x_s, y_s = lines.boundary.geoms[0].x, lines.boundary.geoms[0].y
            if i == len(self.path) - 1:
                # store ending point
                x_e, y_e = lines.boundary.geoms[1].x, lines.boundary.geoms[1].y
            if self.disp_map[i]:
                if label_helper_disp:
                    ax.plot(xx, yy, 'go-', ms=6, linewidth=2.5)
                else:
                    ax.plot(xx, yy, 'go-', label='dispersing',
                            ms=6, linewidth=2.5)
                    label_helper_disp = True
            else:
                if label_helper_nondisp:
                    ax.plot(xx, yy, 'bo-', ms=6, linewidth=2.5)
                else:
                    ax.plot(xx, yy, 'bo-', label='non-dispersing',
                            ms=6, linewidth=2.5)
                    label_helper_nondisp = True
        # Plot starting and ending points
        ax.plot(x_s, y_s, label="Start", ms=12, marker="*",
                mec="darkgoldenrod", mfc="goldenrod")
        ax.plot(x_e, y_e, label="End", ms=8, marker="8",
                mec="firebrick", mfc="lightcoral")

        ax.set_title("2D Aerial View")
        ax.set_xlabel("x (m)")
        ax.set_ylabel("y (m)")
        ax.xaxis.set_major_locator(plt.MaxNLocator(2))
        ax.yaxis.set_major_locator(plt.MaxNLocator(2))
        ax.set_aspect('equal', adjustable="box")
        ax.legend()
        return ax

    def coverage(self) -> Polygon:
        linepath = merge_line(self.path)
        return linepath.buffer(self.disp_diam / 2, quad_segs=3)

    def coverage_disp(self, ax):
        """displays the coverage of the path along with the area to be covered.
        """
        if self.parent.offsetparent:
            showpoly(ax, self.parent, label="Field Offset",
                     color="paleturquoise")
            showpoly(ax, self.parent.offsetparent,
                     label="Field Outline", color="teal")
        else:
            showpoly(ax, self.parent, label="Field Outline", color="teal")
        x, y = self.coverage().exterior.xy
        ax.fill(x, y, color="salmon", alpha=0.3)

        ax.set_title(f"2D Coverage\n({self.disp_diam}m Dispersion Diameter)")
        ax.set_xlabel("x (m)")
        ax.set_ylabel("y (m)")
        ax.xaxis.set_major_locator(plt.NullLocator())
        ax.yaxis.set_major_locator(plt.NullLocator())
        ax.set_aspect('equal', adjustable="box")
        ax.legend()

    def coverage_print(self):
        covered_area = self.coverage().area / 1000**2
        poly = self.parent.offsetparent if self.parent.offsetparent else self.parent
        covered_area_desired = self.coverage().intersection(
            poly.polygon).area / 1000**2  # KM^2
        perc = covered_area_desired / poly.area * 100
        print(
            f"This path covers {round(covered_area_desired,2)} KM^2 within the field of {round(poly.area,2)} KM^2 ({round(perc,2)}%)")
        return f"This path covers {round(covered_area_desired,2)} KM^2 within the field of {round(poly.area,2)} KM^2 ({round(perc,2)}%)"

    def airtime_print(self):
        time_disp = disp_time(self.airtime)
        print(time_disp)
        return time_disp

    def length_print(self):
        print(f"This path is {round(self.pathlength, 2)} KM long.")
        return f"This path is {round(self.pathlength, 2)} KM long."

    """
    ========================
    === Attribute Setter ===
    ========================    
    """

    def disp_map_setter(self) -> list[bool]:
        """Determines the max velocity of each corresponding Segment within the Path within the Polygon.
        Note that lines that connects the swath are not dispersing lines.
        """
        map = []
        for line in self.path:
            if (line_slope(line) == "vertical" and self.swath_slope != "vertical"):
                map.append(False)
            elif (line_slope(line) != "vertical" and self.swath_slope == "vertical"):
                map.append(False)
            elif (line_slope(line) == "vertical" and self.swath_slope == "vertical"):
                map.append(True)
            elif not np.isclose(line_slope(line), self.swath_slope, rtol=1e-05, atol=1e-08, equal_nan=False):
                # If the slope doesn't match the swath slope, then the line is a intermediate line that connects the swath, hence not a dispersing line.
                map.append(False)
            elif not self.parent.polygon.buffer(1e-8).contains(line):
                # If the line isn't inside the polygon, then the line isn't a dispersing line
                # Note that .buffer is used to account for Python rounding error
                map.append(False)
            elif self.parent.children:
                # If the line is inside of any internal polygons (e.g. lakes), then the line isn't a dispersing line
                if any([c.buffer(1e-8).contains(line) for c in self.parent.children]):
                    map.append(False)
            else:
                map.append(True)
        return map

    def pathlength_setter(self):
        """Returns the length of path in KM
        Note that the point coordinates in self.path are in unit of longtitude and latitude.
        """
        return sum([line.length for line in self.path]) / 1000

    def segment_list_setter(self) -> list[Segment]:
        """Returns the projected airtime when executing the given path"""
        def velo_mapper(index):
            """Returns the velocity of the segment depending on whether 
            the number 'index' path in self.path is a dispersing of non-dispersing path.
            e.g. mapper(2) -> 'dispersing_velocity' if the 3rd line in self.path is a dispersing path, 'nondispersing_velocity' if not.
            """
            return self.disp_velo if self.disp_map[index] else self.nondisp_velo

        # Construct each LineString into Segment instances
        airtime_list = []
        for index in range(len(self.path)):
            if index == 0:
                # define the first segment of the path
                airtime_list.append(Segment(self.path[0], self, self.start_velo, velo_mapper(0), velo_mapper(1),
                                            prev_angle=None, next_angle=line_angle(self.path[0], self.path[1])))
                continue
            if index == len(self.path)-1:
                # define the last segment of the path
                airtime_list.append(Segment(self.path[-1], self, velo_mapper(-2), velo_mapper(-1), self.end_velo,
                                            prev_angle=line_angle(self.path[-2], self.path[-1]), next_angle=None))
                continue
            # define all the segments in between
            airtime_list.append(Segment(self.path[index], self, velo_mapper(index-1), velo_mapper(index), velo_mapper(index+1),
                                        prev_angle=line_angle(self.path[index-1], self.path[index]), next_angle=line_angle(self.path[index], self.path[index+1])))

        return airtime_list

    def airtime_setter(self):
        # compute total path time from all segment instances
        tot_hour = sum([seg.time for seg in self.segment_list])
        return tot_hour
