import bpy

# Create a new mesh
ob_name = "triangles"
mesh = bpy.data.meshes.new(ob_name + "_mesh")

# Create a new object with the mesh
ob = bpy.data.objects.new(ob_name, mesh)

# Define the geometry
verts = [
        (0,0,0), (0,2,0), (0,1,2) ,
        (0,3,2)
        ]
edges = [
        (0,1), (1,2), (2,0),
        (1,3), (3, 2)
        ]
faces = [ (0,1,2), (1,3,2) ]

# Add the geometry to the mesh
mesh.from_pydata(verts, edges, faces)

# Link the object to the Scene collection
bpy.context.scene.collection.objects.link(ob)

# This is to reference the vertex color layer later
vertex_colors_name = "vert_colors"

# Here the color layer is made on the mesh
mesh.vertex_colors.new(name=vertex_colors_name)

# We define a variable that is used to easily reference
# the color layer in code later
color_layer = mesh.vertex_colors[vertex_colors_name]

# We list a color for every vertex in every polygon in the loop order
vert_colors = [
        [1,0,0,1], [0,1,0,1] , [0,0,1,1]  ,
        [1,0,0,1], [0,0,1,1] , [0,1,0,1]
        ]

# We loop over all the polygons
for poly in mesh.polygons:
    # We get the polygon index and the corresponding mesh index
    for vert_i_poly, vert_i_mesh in enumerate(poly.vertices):
        # We get the loop index from the polygon index
        vert_i_loop = poly.loop_indices[vert_i_poly]
        # We set the color for the vertex
        color_layer.data[vert_i_loop].color = vert_colors[vert_i_loop]
        # A print statement to see how the indices relate to each other
        print(vert_i_poly, vert_i_mesh, vert_i_loop)