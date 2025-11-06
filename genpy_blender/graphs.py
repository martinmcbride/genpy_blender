# Author:  Martin McBride
# Created: 2025-11-03
# Copyright (c) 2025, Martin McBride
# License: GNU GPL V 3
import math
from dataclasses import dataclass

import bpy

from mathutils import Vector

def align_perpendicular_to_camera(object, camera):
    view_vector = camera.matrix_world.to_quaternion() @ Vector((0, 0, 1))
    object.rotation_euler = view_vector.to_track_quat('Z', 'Y').to_euler()
    bpy.context.view_layer.update()

def create_diffuse_material(mesh, colour, name):
    material = bpy.data.materials.new(name = name)
    material.diffuse_color = colour
    mesh.data.materials.append(material)

class Axes():

    def __init__(self):
        self.xaxis_color = (1, 0, 0, 1)
        self.yaxis_color = (0, 1, 0, 1)
        self.zaxis_color = (0, 0, 1, 1)
        self.div_color = (0, 0, 0, 1)
        self.plane_color = (0.8, 0.8, 0.8, 1)
        self.div_radius = 0.01
        self.axis_radius = 0.02
        self.axis_start = (-1, -1, -1)
        self.axis_end = (1, 1, 1)
        self.start = (0, 0, 0)
        self.end = (1, 1, 1)
        self.step = (0.2, 0.2, 0.2)
        self.steps = ((0, 0.2, 0.4, 0.6, 0.8, 1.0), (0, 0.2, 0.4, 0.6, 0.8, 1.0), (0, 0.2, 0.4, 0.6, 0.8, 1.0))
        self.axis_steps = ((0, 0.2, 0.4, 0.6, 0.8, 1.0), (0, 0.2, 0.4, 0.6, 0.8, 1.0), (0, 0.2, 0.4, 0.6, 0.8, 1.0))

    def convert_points_graph_to_blender(self, x, y, z):
        xo = ((x - self.start[0]) * (self.axis_end[0] - self.axis_start[0]) / (
                    self.end[0] - self.start[0])) + self.axis_start[0]
        print(self.start[0], (self.axis_end[0] - self.axis_start[0]),
              (self.end[0] - self.start[0]), self.axis_start[0])
        yo = ((y - self.start[1]) * (self.axis_end[1] - self.axis_start[1]) / (
                    self.end[1] - self.start[1])) + self.axis_start[1]
        zo = ((z - self.start[2]) * (self.axis_end[2] - self.axis_start[2]) / (
                    self.end[2] - self.start[2])) + self.axis_start[2]
        #print(x, y, z, xo, yo, zo)
        return xo, yo, zo

    def convert_points_blender_to_graph(self, xo, yo, zo):
        x = ((xo - self.axis_start[0]) * (self.end[0] - self.start[0]) / (
                    self.axis_end[0] - self.axis_start[0])) + self.start[0]
        y = ((yo - self.axis_start[1]) * (self.end[1] - self.start[1]) / (
                    self.axis_end[1] - self.axis_start[1])) + self.start[1]
        z = ((zo - self.axis_start[2]) * (self.end[2] - self.start[2]) / (
                    self.axis_end[2] - self.axis_start[2])) + self.start[2]
        #print(x, y, z, xo, yo, zo)
        return x, y, z

    def add_axis_text(self, value, location):
        bpy.ops.object.text_add(enter_editmode=False, align='WORLD')
        obj = bpy.context.active_object
        obj.location = self.convert_points_graph_to_blender(*location)
        print("**", value, location, obj.location)
        text_data = obj.data
        text_data.body = value
        text_data.size = 0.12
        text = bpy.context.active_object
        align_perpendicular_to_camera(text, bpy.data.objects.get("Camera"))
        create_diffuse_material(text, (0, 0, 0, 1), "text_material")

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
        bpy.ops.mesh.primitive_plane_add()
        plane = bpy.context.active_object
        if orientation == "x":
            plane.location = Vector((0, 1, 0))
            angle = math.radians(90)
            plane.rotation_euler[0] = angle
            for p, pa in zip(self.steps[0], self.axis_steps[0]):
                self.cylinder_between(pa, self.axis_end[1], self.axis_start[2], pa, self.axis_end[1], self.axis_end[2], self.div_radius, self.div_color)
                self.add_axis_text(str(p), (p, 0, 0))
            for p, pa in zip(self.steps[2], self.axis_steps[2]):
                self.cylinder_between(self.axis_start[0], self.axis_end[1], pa, self.axis_end[0], self.axis_end[1], pa, self.div_radius, self.div_color)

        if orientation == "y":
            plane.location = Vector((-1, 0, 0))
            angle = math.radians(90)
            plane.rotation_euler[1] = angle
            for p, pa in zip(self.steps[1], self.axis_steps[1]):
                self.cylinder_between(self.axis_start[0], pa, self.axis_start[2], self.axis_start[0], pa, self.axis_end[2], self.div_radius, self.div_color)
                self.add_axis_text(str(p), (1, p, 0))
            for p, pa in zip(self.steps[2], self.axis_steps[2]):
                self.cylinder_between(self.axis_start[0], self.axis_start[1], pa, self.axis_start[0], self.axis_end[1], pa, self.div_radius, self.div_color)

        if orientation == "z":
            plane.location = Vector((0, 0, -1))
            for p, pa in zip(self.steps[0], self.axis_steps[0]):
                self.cylinder_between(pa, self.axis_start[1], self.axis_start[2], pa, self.axis_end[1], self.axis_start[2], self.div_radius, self.div_color)
            for p, pa in zip(self.steps[1], self.axis_steps[1]):
                self.add_axis_text(str(p), (1, 1, p))
                self.cylinder_between(self.axis_start[0], pa, self.axis_start[2], self.axis_end[0], pa, self.axis_start[2], self.div_radius, self.div_color)

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

    def draw_axes(self):
        r = self.axis_radius
        self.cylinder_between(-1, 1, -1, 1, 1, -1, r, color=self.xaxis_color)
        self.cylinder_between(-1, -1, -1, -1, 1, -1, r, color=self.yaxis_color)
        self.cylinder_between(-1, 1, -1, -1, 1, 1, r, color=self.zaxis_color)

    def draw(self):
        self.axis_steps = ((-1, -0.6, -0.2, 0.2, 0.6, 1),)*3
        self.plane("x")
        self.plane("y")
        self.plane("z")
        self.draw_axes()


