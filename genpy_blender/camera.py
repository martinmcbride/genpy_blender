# Author:  Martin McBride
# Created: 2025-11-02
# Copyright (c) 2025, Martin McBride
# License: GNU GPL V 3
# Based on part on https://github.com/yuki-koyama/blender-cli-rendering

import bpy
from typing import Tuple


def create_camera(location: Tuple[float, float, float]) -> bpy.types.Object:
    bpy.ops.object.camera_add(location=location)

    return bpy.context.object

def add_track_to_constraint(camera_object: bpy.types.Object, track_to_target_object: bpy.types.Object) -> None:
    constraint = camera_object.constraints.new(type='TRACK_TO')
    constraint.target = track_to_target_object
    constraint.track_axis = 'TRACK_NEGATIVE_Z'
    constraint.up_axis = 'UP_Y'

def set_camera_params(camera: bpy.types.Camera,
                      focus_target_object: bpy.types.Object,
                      lens: float = 85.0,
                      fstop: float = 1.4) -> None:
    # Simulate Sony's FE 85mm F1.4 GM
    camera.sensor_fit = 'HORIZONTAL'
    camera.sensor_width = 36.0
    camera.sensor_height = 24.0
    camera.lens = lens
    camera.dof.use_dof = True
    camera.dof.focus_object = focus_target_object
    camera.dof.aperture_fstop = fstop
    camera.dof.aperture_blades = 11
