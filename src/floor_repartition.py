import bpy
from bpy.props import *
import numpy as np

bl_info = {"name": "Easy City Addon", "category": "Object"}

def add_floor(context, width, height):
	bpy.ops.mesh.primitive_grid_add(x_subdivisions=width*2, y_subdivisions=height*2, enter_editmode=True)
	floor = bpy.data.objects['Grid']
	floor.name = "Floor"
	bpy.context.scene.objects.active = floor

	floor.scale.x = width
	floor.scale.y = height

	return floor

class MESH_OT_primitive_floor_add(bpy.types.Operator):
    '''Add a floor'''
    bl_idname = "mesh.primitive_floor_add"
    bl_label = "Add floor"
    bl_options = {'REGISTER', 'UNDO'}
 
    width = IntProperty(name="Width",
            description="Width of the plane",
            default=5, min=2, max=500)
    height = IntProperty(name="Height",
            description="Height of the plane",
            default=5, min=2, max=500)
 
    def execute(self, context):
        ob = add_floor(context, self.width, self.height)
        return {'FINISHED'}
 
def menu_func(self, context):
    self.layout.operator("mesh.primitive_floor_add", 
        text="Floor", 
        icon='MESH_GRID')
 
def register():
   bpy.utils.register_module(__name__)
   bpy.types.INFO_MT_mesh_add.prepend(menu_func)
 
def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_mesh_add.remove(menu_func)
 
if __name__ == "__main__":
    register()