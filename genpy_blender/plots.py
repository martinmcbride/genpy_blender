# Author:  Martin McBride
# Created: 2025-11-03
# Copyright (c) 2025, Martin McBride
# License: GNU GPL V 3
import math
import random

import numpy as np
import bpy
import bmesh

class Plot3dZofXY:

    def __init__(self, axes, function):
        self.axes = axes
        self.function = function
        self.samples = 100
        self.color = (0, 0, 1, 1)

    def plot(self):
        bpy.ops.mesh.primitive_grid_add(x_subdivisions=120, y_subdivisions=120, location=self.axes.start)
        bpy.ops.transform.resize(value=self.axes.end)

        bpy.ops.object.mode_set(mode='EDIT')

        obj = bpy.context.active_object
        mesh = obj.data

        bm = bmesh.from_edit_mesh(mesh)

        for v in bm.verts:
            x, y, _ = self.axes.convert_points_blender_to_graph(v.co.x, v.co.y, 0)
            z = self.function(x, y)
            v.co.z += self.axes.convert_points_graph_to_blender(x, y, z)[2]

        bmesh.update_edit_mesh(mesh)

        bpy.ops.object.mode_set(mode='OBJECT')

        # Get the active object (which is the cube)
        graph_object = bpy.context.active_object
        # Get the mesh data
        mesh = graph_object.data

        # Switch to Vertex Paint mode
        bpy.ops.object.mode_set(mode='VERTEX_PAINT')

        # Set the active vertex color layer
        active_vc_layer = graph_object.data.vertex_colors.active
        if active_vc_layer is None:
            active_vc_layer = graph_object.data.vertex_colors.new()

        # Loop through the vertices and set them to red
        for poly in graph_object.data.polygons:
            for loop_index in poly.loop_indices:
                loop = graph_object.data.loops[loop_index]
                vertex_index = loop.vertex_index
                vert = mesh.vertices[vertex_index]
                # color = color_map(vert.co.z, colormap, display_levels)
                color = [4*abs(vert.co.z), 0, 0, 1]  # Red color (RGBA)
                active_vc_layer.data[loop_index].color = color

        # Create a new material
        mat = bpy.data.materials.new(name="Vertex Color Material")
        graph_object.data.materials.append(mat)

        # Get a reference to the material
        mat = graph_object.data.materials[0]

        # Create a new node tree for the material
        mat.use_nodes = True
        nodes = mat.node_tree.nodes

        # Clear default nodes
        for node in nodes:
            nodes.remove(node)

        # Add a Vertex Color node
        vc_node = nodes.new(type='ShaderNodeVertexColor')
        vc_node.layer_name = 'Attribute'
        vc_node.location = (0, 0)  # Optional: Set the location of the node

        # Add a Principled BSDF shader node
        bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')
        bsdf_node.location = (400, 0)  # Optional: Set the location of the node

        # Add an Output node
        output_node = nodes.new(type='ShaderNodeOutputMaterial')
        output_node.location = (600, 0)  # Optional: Set the location of the node

        # Connect the nodes
        mat.node_tree.links.new(vc_node.outputs["Color"], bsdf_node.inputs["Base Color"])
        mat.node_tree.links.new(bsdf_node.outputs["BSDF"], output_node.inputs["Surface"])

        bpy.ops.object.mode_set(mode='OBJECT')
