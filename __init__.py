#----------------------------------------------------------
# File __init__.py
#----------------------------------------------------------
 
#    Addon info
bl_info = {
    'name': 'Easy City Addon',
    'author': 'Goeminne Colas, Barthel Xavier',
    'location': 'View3D > UI panel',
    'category': 'Object'
    }
 
# To support reload properly, try to access a package var, 
# if it's there, reload everything
if "bpy" in locals():
    import imp
    imp.reload(floor_repartition)
    print("Reloaded multifiles")
else:
    from . import floor_repartition	
    print("Imported multifiles")
 
import bpy
from bpy.props import *
import os

bpy.types.Scene.city_size = IntProperty(name="Size", default=20)
bpy.types.Scene.max_block_size = IntProperty(name="Block Size", default=7)
bpy.types.Scene.park_mean = FloatProperty(name="Proportion of parks", default=0.1, min=0.0, max=1.0)
bpy.types.Scene.height_mean = FloatProperty(name="Mean building height", default=50.0, min=10.0, max=100.0)
bpy.types.Scene.height_std = FloatProperty(name="Standard deviation building height", default=10.0, min=5.0, max=50.0)

matrice=[]

#
#   class EasyCityPanel(bpy.types.Panel):
#
class EasyCityPanel(bpy.types.Panel):
    bl_label = "Easy City Generator"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'City'

    def draw(self, context):
        layout = self.layout
        layout.label(text="City Parameters:")

        # split = layout.split()
        # col = split.column(align=True)

        # col.operator("mesh.primitive_plane_add", text="Plane", icon='MESH_PLANE')
        # col.operator("mesh.primitive_torus_add", text="Torus", icon='MESH_TORUS')
        
        scene = context.scene
        row = layout.row()
        row.prop(scene, 'city_size')
        row.prop(scene, 'max_block_size')
        row = layout.row()
        row.prop(scene, 'park_mean')
        row = layout.row()
        row.prop(scene, 'height_mean')
        row.prop(scene, 'height_std')
        row = layout.row()
        row.operator('city.generate')
        row.operator('city.delete')
        row = layout.row()
        row.operator('city.day')
        row.operator('city.night')


class OBJECT_OT_Day(bpy.types.Operator):
    bl_idname = "city.day"
    bl_label = "Day Light"
    bl_description = "Set day light environment"
    def execute(self,context):
        floor_repartition.setDayLight(matrice)
        return {'FINISHED'}

class OBJECT_OT_Night(bpy.types.Operator):
    bl_idname = "city.night"
    bl_label = "Night Light"
    bl_description = "Set night light environment"
    def execute(self,context):
        floor_repartition.setNightLight(matrice)
        return {'FINISHED'}



class OBJECT_OT_GenerateCity(bpy.types.Operator):
    bl_idname = "city.generate"
    bl_label = "Generate"
    bl_description = "Generates the city based on the given parameters."

    def execute(self, context):

        directory = os.path.dirname(__file__)
        roadfilepath = os.path.join(directory, "models/road.blend")
        with bpy.data.libraries.load(roadfilepath, link=True) as (data_from, data_to):
            data_to.objects = [name for name in data_from.objects if name.startswith("road")]

        buildingsfilepath = os.path.join(directory, "models/buildings.blend")
        with bpy.data.libraries.load(buildingsfilepath, link=True) as (data_from, data_to):
            data_to.objects = [name for name in data_from.objects if (name.startswith("building") or name.startswith("house"))]

        parksfilepath = os.path.join(directory, "models/parks.blend")
        with bpy.data.libraries.load(parksfilepath, link=True) as (data_from, data_to):
            data_to.objects = [name for name in data_from.objects if name.startswith("park")]
        
        carsfilepath = os.path.join(directory, "models/cars.blend")
        with bpy.data.libraries.load(carsfilepath, link=True) as (data_from, data_to):
            data_to.objects = [name for name in data_from.objects if name.startswith("car")]

        urbanfilepath = os.path.join(directory, "models/urban.blend")
        with bpy.data.libraries.load(urbanfilepath, link=True) as (data_from, data_to):
            data_to.objects = [name for name in data_from.objects if name.startswith("street") or name.startswith("mail")]

        worldfilepath = os.path.join(directory, "models/sky.blend")
        with bpy.data.libraries.load(worldfilepath, link=True) as (data_from, data_to): 
            data_to.worlds = [name for name in data_from.worlds if name.startswith("myWorld")]

        worldNightfilepath = os.path.join(directory, "models/skyNight.blend")
        with bpy.data.libraries.load(worldNightfilepath, link=True) as (data_from, data_to): 
            data_to.worlds = [name for name in data_from.worlds if name.startswith("myWorld")]

        scene = context.scene
        
        # Remove previous city (if any)
        bpy.ops.city.delete()

        # Add an empty that will serve as the parent of all buildings
        bpy.ops.object.add(type='EMPTY')
        empty = bpy.context.object
        empty.name = 'City'

        # # Get the template objects (name starting with '_'
        # objs = [obj for obj in bpy.data.objects if obj.name[0] == '_']
        # # Get the mesh from the template object
        # meshes = [obj.data for obj in objs]
        
        size = scene.city_size
        max_block_size = scene.max_block_size
        park_mean = scene.park_mean
        height_mean = scene.height_mean
        height_std = scene.height_std

        roads = {	"straight": bpy.data.objects['roadStraight'],
        			"roadL": bpy.data.objects['roadL'],
        			"roadT": bpy.data.objects['roadT'],
                    "roadX": bpy.data.objects['roadX']}

        buildings = [obj for obj in bpy.data.objects if ("building" in obj.name or "house" in obj.name)]
        parks = [obj for obj in bpy.data.objects if "park" in obj.name] 
        cars = [obj for obj in bpy.data.objects if "car" in obj.name]
        streetLamp=[obj for obj in bpy.data.objects if "street" in obj.name]
        mailBox=[obj for obj in bpy.data.objects if "mail" in obj.name]
        print("taille cars : ",len(cars))

        bpy.context.scene.render.engine = 'CYCLES'


        matrice=floor_repartition.draw_roads_and_buildings(size, roads, buildings, max_block_size, parks, park_mean, height_mean, height_std)
        floor_repartition.setDayLight(matrice)
        floor_repartition.setNightLight(matrice)
        floor_repartition.setUrban(matrice,streetLamp,mailBox)
        floor_repartition.carsAnim(matrice, cars)
        
        # # Create a duplicate linked object of '_Building1'
        # for x in np.linspace(-size/2, size/2, size):
        #     for y in np.linspace(-size/2, size/2, size):

        #         height = 2 + np.random.rand() * 8                       # Random height
        #         mesh = meshes[np.random.random_integers(len(meshes))-1] # Random mesh from templates
        #         new_obj = bpy.data.objects.new('Building.000', mesh)    # Create new object linked to same mesh data
        #         new_obj.location = (x*2,y*2,0)                          # Set its location
        #         new_obj.scale = (1,1,height)                            # Set its scale
        #         scene.objects.link(new_obj)                             # Link new object to scene
        #         new_obj.parent = empty                                  # Link new object to empty

        return {'FINISHED'}

class OBJECT_OT_DeleteCity(bpy.types.Operator):
    bl_idname = "city.delete"
    bl_label = "Delete"
 
    def execute(self, context):
        scene = context.scene
        
        # Remove previous city
        city = bpy.data.objects.get('City')                         # Get 'City' object
        if not city is None:                                        # If exists
            bpy.ops.object.select_all(action='DESELECT')            # Deselect all
            city.select = True                                      # Select City
            bpy.ops.object.select_hierarchy(direction='CHILD',      # Select all children of City
                                            extend=True)
            bpy.ops.object.select_hierarchy(direction='CHILD', extend=True)

            bpy.ops.object.delete(use_global=False)                 # Delete selection
    
        return {'FINISHED'}

#
#    Registration
#
def register():
    bpy.utils.register_module(__name__)
 
def unregister():
    bpy.utils.unregister_module(__name__)
 
if __name__ == "__main__":
    register()