import bpy
from mathutils import Vector
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

def plane(orientation):
    bpy.ops.mesh.primitive_plane_add()
    plane = bpy.context.active_object
    if orientation=="x":
        plane.location = Vector((0, 1, 0))
        angle = math.radians(90)
        plane.rotation_euler[0] = angle
    if orientation=="y":
        plane.location = Vector((-1, 0, 0))
        angle = math.radians(90)
        plane.rotation_euler[1] = angle
    if orientation=="z":
        plane.location = Vector((0, 0, -1))
    plane.scale = Vector((1, 1, 1))

    mat = bpy.data.materials.new("col")
    if orientation=="x":
        mat.diffuse_color = (1, 0, 0, 1)
        plane.active_material = mat
    if orientation=="y":
        mat.diffuse_color = (0, 1, 0, 1)
        plane.active_material = mat
    if orientation=="z":
        mat.diffuse_color = (0, 0, 1, 1)
        plane.active_material = mat


def set_scene_objects() -> bpy.types.Object:
    num_suzannes = 1
    for index in range(num_suzannes):
        utils.create_smooth_monkey(location=((index - (num_suzannes - 1) / 2) * 3.0, 0.0, 0.0),
                                   name="Suzanne" + str(index))
    return bpy.data.objects["Suzanne" + str(int((num_suzannes - 1) / 2))]


def draw(pixel_width, pixel_height, frame_no, frame_count):

    camera_object = camera.create_camera(location=(10.0, -7.0, 0.0))

    centre = set_scene_objects()
    plane("x")
    plane("y")
    plane("z")

    camera.add_track_to_constraint(camera_object, centre)
    camera.set_camera_params(camera_object.data, centre, lens=50.0)

    ## Lights
    lighting.create_sun_light(rotation=(0.0, math.pi * 0.5, -math.pi * 0.1))

    return camera_object

make_image.make_blender_image("make_axes_test", draw, 100, 100)