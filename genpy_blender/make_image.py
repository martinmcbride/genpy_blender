# Author:  Martin McBride
# Created: 2025-11-02
# Copyright (c) 2025, Martin McBride
# License: GNU GPL V 3

import bpy
import math
import utils
import camera
import lighting

def make_blender_image(outfile, draw, width, height):
    print("MBI HERE")
    output_file_path = bpy.path.relpath(outfile)
    resolution_percentage = 100
    num_samples = 128
    utils.clean_objects()

    # camera_object = draw(width, height, 0, 1)
    num_suzannes = 3
    for index in range(num_suzannes):
        utils.create_smooth_monkey(location=((index - (num_suzannes - 1) / 2) * 3.0, 0.0, 0.0),
                                   name="Suzanne" + str(index))
    center_suzanne = bpy.data.objects["Suzanne" + str(int((num_suzannes - 1) / 2))]

    ## Camera
    camera_object = camera.create_camera(location=(10.0, -7.0, 0.0))

    camera.add_track_to_constraint(camera_object, center_suzanne)
    camera.set_camera_params(camera_object.data, center_suzanne, lens=50.0)

    ## Lights
    lighting.create_sun_light(rotation=(0.0, math.pi * 0.5, -math.pi * 0.1))

    scene = bpy.data.scenes["Scene"]
    print("}}}}}}}}}}}}}}}}", output_file_path, resolution_percentage, num_samples)
    utils.set_output_properties(scene, resolution_percentage, output_file_path)
    utils.set_cycles_renderer(scene, camera_object, num_samples)
    print(">>>>>MBI DONE")

def example_blender_draw_function(pixel_width, pixel_height, frame_no, frame_count):
    pass