# Author:  Martin McBride
# Created: 2025-11-03
# Copyright (c) 2025, Martin McBride
# License: GNU GPL V 3
import random

import numpy as np
import bpy

class Plot3dZofXY:

    def __init__(self, axes, function):
        self.axes = axes
        self.function = function
        self.samples = 100
        self.color = (0, 0, 1, 1)

    def vert(self, i, j, x, y, z):
        """ Create a single vert """
        return (x[i, j], y[i, j], z[i, j])

    def face(self, column, row):
        """ Create a single face """
        return (column * self.samples + row, (column + 1) * self.samples + row, (column + 1) * self.samples + 1 + row, column * self.samples + 1 + row)

    def set_vertex_colors(self, mesh):
        for i, v in enumerate(mesh.vertex_colors[0].data):
            mesh.vertex_colors[0].data[i] = (1, 0, 1, 1)

    def plot(self):
        # print("*****************", self.axes.start[0], self.axes.end[0], self.axes.steps[0])
        x = np.linspace(self.axes.start[0], self.axes.end[0], self.samples)
        y = np.linspace(self.axes.start[1], self.axes.end[1], self.samples)
        xx, yy = np.meshgrid(x, y)
        vf = np.vectorize(self.function)
        ff = vf(xx, yy)
        # print("{{{{{{")
        # print(x, y)
        # print("}}}}}}")
        # print("<<<<<<")
        # print(xx, yy, ff)
        # print(">>>>>>")

        vf = np.vectorize(self.axes.convert_points_graph_to_blender)
        xx, yy, ff = vf(xx, yy, ff)
        # print("[[[[[[")
        # print(xx, yy, ff)
        # print("]]]]]]")
        verts = [self.vert(x, y, xx, yy, ff) for x in range(self.samples) for y in range(self.samples)]
        faces = [self.face(x, y) for x in range(self.samples - 1) for y in range(self.samples - 1)]

        # Create Mesh Datablock
        mesh = bpy.data.meshes.new("graph")
        mesh.from_pydata(verts, [], faces)
        mat = bpy.data.materials.new("graph")
        mat.diffuse_color = self.color
        mesh.materials.append(mat)

        color_layer = mesh.vertex_colors.new(name="graph_colors")

        for poly in mesh.polygons:
            for i in range(len(poly.vertices)):
                color_layer.data[poly.loop_indices[i]].color = [1, 1, 0, 1]
                #print(poly.vertices[i])

        # mesh.vertex_colors.new()
        # self.set_vertex_colors(mesh)

        # bpy.ops.object.mode_set(mode='VERTEX_PAINT')
        #
        # # Create Object and link to scene
        # obj = bpy.data.objects.new("graph", mesh)
        # obj.visible_shadow = False
        # #bpy.ops.object.shade_smooth = True
        # bpy.context.scene.collection.objects.link(obj)
        # bpy.ops.object.mode_set(mode='OBJECT')
