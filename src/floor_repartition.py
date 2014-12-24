import bpy
from bpy.props import *
import numpy as np

bl_info = {"name": "Easy City Addon", "category": "Object"}

def add_floor(context, width, height):
    verts = []
    faces = []
    w = width + 1
    h = height + 1
    for i in range(w):
        for j in range(h):
            verts.append((i, j, 0))
            if i > 0 and j > 0:
                faces.append(((i*h)+j, (i*h)+(j-1), ((i-1)*h)+(j-1), ((i-1)*h)+j))
    
    me = bpy.data.meshes.new("Floor")
    me.from_pydata(verts, [], faces)
    ob = bpy.data.objects.new("Floor", me)
    context.scene.objects.link(ob)
    context.scene.objects.active = ob
    return ob

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