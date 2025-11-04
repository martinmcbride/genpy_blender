import bpy
import sys
import math
import os

working_dir_path = os.path.abspath("/nas/martin/7-software-projects/genpy_blender/genpy_blender/")
sys.path.append(working_dir_path)

from mathutils import Vector
import make_image
import utils
import camera
import lighting
import graphs
from plots import Plot3dZofXY



def draw(pixel_width, pixel_height, frame_no, frame_count):

    camera_object = camera.create_plot_camera()

    axes = graphs.Axes()
    axes.draw()
    plot = Plot3dZofXY(axes, lambda x, y : x + y)
    plot.plot()

    ## Lights
    lighting.create_sun_light(rotation=(0.0, math.pi * 0.5, -math.pi * 0.1))

    return camera_object

make_image.make_blender_image("make_axes_test", draw, 100, 100)