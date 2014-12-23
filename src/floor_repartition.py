import bpy
import numpy as np

def create_plane(width, height):
	bpy.ops.mesh.primitive_plane_add()
	floor = bpy.data.objects['Plane']
	floor.name = "Floor"
	bpy.context.scene.objects.active = floor

	floor.scale.x = width
	floor.scale.y = height

	bpy.ops.object.mode_set(mode='EDIT')
	bpy.ops.mesh.subdivide(number_cuts=height)

	return floor

if __name__ == "__main__":

	create_plane(10,20)