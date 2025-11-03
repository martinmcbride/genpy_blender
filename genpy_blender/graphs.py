# Author:  Martin McBride
# Created: 2025-11-03
# Copyright (c) 2025, Martin McBride
# License: GNU GPL V 3
import math
from dataclasses import dataclass

import bpy

from mathutils import Vector

class Axes():

    def __init__(self):
        self.xaxis_color = (1, 0, 0, 1)
        self.yaxis_color = (0, 1, 0, 1)
        self.zaxis_color = (0, 0, 1, 1)
        self.div_color = (0, 0, 0, 1)
        self.plane_color = (0.8, 0.8, 0.8, 1)
        self.div_radius = 0.01
        self.axis_radius = 0.02

    def cylinder_between(self, x1, y1, z1, x2, y2, z2, r, color):

        dx = x2 - x1
        dy = y2 - y1
        dz = z2 - z1
        dist = math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)

        bpy.ops.mesh.primitive_cylinder_add(
            radius=r,
            depth=dist,
            location=(dx / 2 + x1, dy / 2 + y1, dz / 2 + z1)
        )

        phi = math.atan2(dy, dx)
        theta = math.acos(dz / dist)

        bpy.context.object.rotation_euler[1] = theta
        bpy.context.object.rotation_euler[2] = phi

        mat = bpy.data.materials.new("col")
        mat.diffuse_color = color
        bpy.context.object.active_material = mat

    def plane(self, orientation):
        start = (0, 0, 0)
        end = (1, 1, 1)
        step = (5, 4, 6)

        bpy.ops.mesh.primitive_plane_add()
        plane = bpy.context.active_object
        if orientation == "x":
            plane.location = Vector((0, 1, 0))
            angle = math.radians(90)
            plane.rotation_euler[0] = angle
            for i in range(step[0]):
                self.cylinder_between(i * 0.4 - 1, 1, -1, i * 0.4 - 1, 1, 1, self.div_radius, self.div_color)
            for i in range(step[2]):
                self.cylinder_between(-1, 1, i * 0.3333 - 1, 1, 1, i * 0.3333 - 1, self.div_radius, self.div_color)

        if orientation == "y":
            plane.location = Vector((-1, 0, 0))
            angle = math.radians(90)
            plane.rotation_euler[1] = angle
            for i in range(step[1]):
                self.cylinder_between(-1, i * 0.5 - 1, -1, -1, i * 0.5 - 1, 1, self.div_radius, self.div_color)
            for i in range(step[2]):
                self.cylinder_between(-1, -1, i * 0.3333 - 1, -1, 1, i * 0.3333 - 1, self.div_radius, self.div_color)

        if orientation == "z":
            plane.location = Vector((0, 0, -1))
            for i in range(step[0]):
                self.cylinder_between(i * 0.4 - 1, -1, -1, i * 0.4 - 1, 1, -1, self.div_radius, self.div_color)
            for i in range(step[1]):
                self.cylinder_between(-1, i * 0.5 - 1, -1, 1, i * 0.5 - 1, -1, self.div_radius, self.div_color)

        plane.scale = Vector((1, 1, 1))

        mat = bpy.data.materials.new("col")
        if orientation == "x":
            mat.diffuse_color = self.plane_color
            plane.active_material = mat
        if orientation == "y":
            mat.diffuse_color = self.plane_color
            plane.active_material = mat
        if orientation == "z":
            mat.diffuse_color = self.plane_color
            plane.active_material = mat

    def axes(self):
        r = self.axis_radius
        self.cylinder_between(-1, 1, -1, 1, 1, -1, r, color=self.xaxis_color)
        self.cylinder_between(-1, -1, -1, -1, 1, -1, r, color=self.yaxis_color)
        self.cylinder_between(-1, 1, -1, -1, 1, 1, r, color=self.zaxis_color)

    def draw(self):
        self.plane("x")
        self.plane("y")
        self.plane("z")
        self.axes()


