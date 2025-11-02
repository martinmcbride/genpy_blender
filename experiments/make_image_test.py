# blender --background --python 02_suzanne.py --render-frame 1 -- </path/to/output/image> <resolution_percentage> <num_samples>

import bpy
import sys
import math
import os

working_dir_path = os.path.abspath("/nas/martin/7-software-projects/genpy_blender/genpy_blender/")
print("!!!", working_dir_path, "!!!")
sys.path.append(working_dir_path)

import make_image
import utils
import camera
import lighting
import make_image

def set_scene_objects() -> bpy.types.Object:
    num_suzannes = 1
    for index in range(num_suzannes):
        utils.create_smooth_monkey(location=((index - (num_suzannes - 1) / 2) * 3.0, 0.0, 0.0),
                                   name="Suzanne" + str(index))
    return bpy.data.objects["Suzanne" + str(int((num_suzannes - 1) / 2))]


def draw(pixel_width, pixel_height, frame_no, frame_count):

    camera_object = camera.create_camera(location=(10.0, -7.0, 0.0))

    center_suzanne = set_scene_objects()

    camera.add_track_to_constraint(camera_object, center_suzanne)
    camera.set_camera_params(camera_object.data, center_suzanne, lens=50.0)

    ## Lights
    lighting.create_sun_light(rotation=(0.0, math.pi * 0.5, -math.pi * 0.1))

    return camera_object

make_image.make_blender_image("make_image_test", draw, 100, 100)