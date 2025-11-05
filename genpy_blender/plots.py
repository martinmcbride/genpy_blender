# Author:  Martin McBride
# Created: 2025-11-03
# Copyright (c) 2025, Martin McBride
# License: GNU GPL V 3

import numpy as np
import bpy

class Plot3dZofXY:

    def __init__(self, axes, function):
        self.axes = axes
        self.function = function
        self.samples = 100

    def convert_points(self, x, y, z):
#        self.axes.end = [ex + s for ex, s in zip(self.axes.extent, self.axes.start)]
        xo = ((x - self.axes.start[0]) * (self.axes.axis_end[0] - self.axes.axis_start[0]) / (self.axes.end[0] - self.axes.start[0])) + self.axes.axis_start[0]
        yo = ((y - self.axes.start[1]) * (self.axes.axis_end[1] - self.axes.axis_start[1]) / (self.axes.end[1] - self.axes.start[1])) + self.axes.axis_start[1]
        zo = ((z - self.axes.start[2]) * (self.axes.axis_end[2] - self.axes.axis_start[2]) / (self.axes.end[2] - self.axes.start[2])) + self.axes.axis_start[2]
#        print("STEPS", zo, z, self.axes.start[1], self.axes.end[1], self.axes.axis_end[1], self.axes.axis_start[1])
        return xo, yo, zo

    def vert(self, i, j, x, y, z):
        """ Create a single vert """
        return (x[i, j], y[i, j], z[i, j])

    def face(self, column, row):
        """ Create a single face """
        return (column * self.samples + row, (column + 1) * self.samples + row, (column + 1) * self.samples + 1 + row, column * self.samples + 1 + row)

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

        vf = np.vectorize(self.convert_points)
        xx, yy, ff = vf(xx, yy, ff)
        # print("[[[[[[")
        # print(xx, yy, ff)
        # print("]]]]]]")
        verts = [self.vert(x, y, xx, yy, ff) for x in range(self.samples) for y in range(self.samples)]
        faces = [self.face(x, y) for x in range(self.samples - 1) for y in range(self.samples - 1)]

        # Create Mesh Datablock
        mesh = bpy.data.meshes.new("graph")
        mesh.from_pydata(verts, [], faces)

        # Create Object and link to scene
        obj = bpy.data.objects.new("graph", mesh)
        bpy.context.scene.collection.objects.link(obj)
