# Author:  Martin McBride
# Created: 2025-11-02
# Copyright (c) 2025, Martin McBride
# License: GNU GPL V 3
# Based on part on https://github.com/yuki-koyama/blender-cli-rendering

from typing import Tuple, Optional

import bpy

def clean_objects() -> None:
    for item in bpy.data.objects:
        bpy.data.objects.remove(item)

def set_smooth_shading(mesh: bpy.types.Mesh) -> None:
    for polygon in mesh.polygons:
        polygon.use_smooth = True

def add_subdivision_surface_modifier(mesh_object: bpy.types.Object, level: int, is_simple: bool = False) -> None:
    '''
    https://docs.blender.org/api/current/bpy.types.SubsurfModifier.html
    '''

    modifier: bpy.types.SubsurfModifier = mesh_object.modifiers.new(name="Subsurf", type='SUBSURF')

    modifier.levels = level
    modifier.render_levels = level
    modifier.subdivision_type = 'SIMPLE' if is_simple else 'CATMULL_CLARK'

def set_output_properties(scene: bpy.types.Scene,
                          resolution_percentage: int = 100,
                          output_file_path: str = "",
                          res_x: int = 1920,
                          res_y: int = 1080) -> None:
    scene.render.resolution_percentage = resolution_percentage
    scene.render.resolution_x = res_x
    scene.render.resolution_y = res_y

    if output_file_path:
        scene.render.filepath = output_file_path

def set_cycles_renderer(scene: bpy.types.Scene,
                        camera_object: bpy.types.Object,
                        num_samples: int,
                        use_denoising: bool = True,
                        use_motion_blur: bool = False,
                        use_transparent_bg: bool = False,
                        prefer_cuda_use: bool = True,
                        use_adaptive_sampling: bool = False) -> None:
    scene.camera = camera_object

    scene.render.image_settings.file_format = 'PNG'
    scene.render.engine = 'CYCLES'
    scene.render.use_motion_blur = use_motion_blur

    scene.render.film_transparent = use_transparent_bg
    scene.view_layers[0].cycles.use_denoising = use_denoising

    scene.cycles.use_adaptive_sampling = use_adaptive_sampling
    scene.cycles.samples = num_samples

    # Enable GPU acceleration
    # Source - https://blender.stackexchange.com/a/196702
    if prefer_cuda_use:
        bpy.context.scene.cycles.device = "GPU"

        # Change the preference setting
        bpy.context.preferences.addons["cycles"].preferences.compute_device_type = "CUDA"

    # Call get_devices() to let Blender detects GPU device (if any)
    bpy.context.preferences.addons["cycles"].preferences.get_devices()

    # Let Blender use all available devices, include GPU and CPU
    for d in bpy.context.preferences.addons["cycles"].preferences.devices:
        d["use"] = 1

    # Display the devices to be used for rendering
    print("----")
    print("The following devices will be used for path tracing:")
    for d in bpy.context.preferences.addons["cycles"].preferences.devices:
        print("- {}".format(d["name"]))
    print("----")


def create_smooth_monkey(location: Tuple[float, float, float] = (0.0, 0.0, 0.0),
                         rotation: Tuple[float, float, float] = (0.0, 0.0, 0.0),
                         subdivision_level: int = 2,
                         name: Optional[str] = None) -> bpy.types.Object:
    bpy.ops.mesh.primitive_monkey_add(location=location, rotation=rotation, calc_uvs=True)

    current_object = bpy.context.object

    if name is not None:
        current_object.name = name

    set_smooth_shading(current_object.data)
    add_subdivision_surface_modifier(current_object, subdivision_level)

    return current_object

