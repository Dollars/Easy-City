# Principe : Parcours classique de la matrice.
# Quand m[i][j]=0, creation d'un bloc de building (m[][]=1), de largeur 2 (ou 1 quand ce n'est pas possible autrement) et de taille random (entre 2 et tailleMaxBloc) positionner
# horizontalement ou verticalement.
# Le bloc est ensuite entoure de rue (m[][]=1). Repete jusqu'au remplissage de la matrice.

import bpy
from bpy.props import *
import numpy as np
import bmesh
import random
from math import *
import math

# def add_floor(context, width, height):
#     verts = []
#     faces = []
#     w = width + 1
#     h = height + 1
#     for i in range(w):
#         for j in range(h):
#             verts.append((i, j, 0))
#             if i > 0 and j > 0:
#                 faces.append(((i*h)+(j-1), (i*h)+j, ((i-1)*h)+j, ((i-1)*h)+(j-1)))
    
#     me = bpy.data.meshes.new("Floor")
#     me.from_pydata(verts, [], faces)
#     ob = bpy.data.objects.new("Floor", me)
#     context.scene.objects.link(ob)
#     context.scene.objects.active = ob
#     return ob

# bpy.ops.object.mode_set(mode='EDIT')
# floor = bpy.data.meshes['Floor']
# bm = bmesh.from_edit_mesh(floor)

# floor_faces = np.array(bm.faces)
# floor_faces = floor_faces.reshape(5,5)
# for i in range(len(floor_faces)):
#     floor_faces[i][i].select = True

# bmesh.update_edit_mesh(floor)
# bpy.ops.mesh.split()
# bpy.ops.mesh.separate(type='SELECTED')
# bm.free()  # free and prevent further access



def floor_repartition(matrice, size, tailleMaxBloc):
    for i in range (0, size):
        j = 0
        while j < size:
            if matrice[i][j] == 0:
                longueur = random.randint(2, tailleMaxBloc)
                
                # Si 3 cases vides, pas de bloc vertical, sinon route de largeur 2. Donc, d'office horizontal et d'office de longueur 3
                cntLong = 0
                for k in range(j, size):
                    if matrice[i][k] == 0:
                        cntLong += 1
                    else:
                        break
                if cntLong == 3:
                    longueur = 3
                    horizontal = 1
                else:
                    horizontal = random.randint(0, 1)
                   
                # Creation building m[][]=1 entoure de route m[][]=2
                
                # Longueur horizontal
                if horizontal:
                    if cntLong >= longueur:
                        if j+longueur+1 < size:
                            if matrice[i][j+longueur+1] == 2 and matrice[i][j+longueur] == 0:
                                longueur += 1
                    else:
                        longueur = cntLong
                           
                    iPlus1 = i+1 < size 
                    iPlus2 = i+2 < size
                    iMoins1 = i-1 > 0
                    tempLongueur = longueur
                    tempJ = j
                    while j < size and longueur > 0:
                        matrice[i][j] = 1
                        if iPlus1:
                            matrice[i+1][j] = 1
                        if iPlus2:
                            matrice[i+2][j] = 2
                        if iMoins1:
                            matrice[i-1][j] = 2
                        longueur -= 1
                        j += 1
                    if tempJ-1 > 0:
                        matrice[i][tempJ-1] = 2
                        if iPlus1:
                            matrice[i+1][tempJ-1] = 2
                        if iPlus2:
                            matrice[i+2][tempJ-1] = 2
                        if iMoins1:
                            matrice[i-1][tempJ-1] = 2
                    if j < size:
                        matrice[i][j] = 2
                        if iPlus1:
                            matrice[i+1][j] = 2
                        if iPlus2:
                            matrice[i+2][j] = 2
                        if iMoins1:
                            matrice[i-1][j] = 2
                else: #longueur vertical
                    jPlus1 = j+1 < size
                    jPlus2 = j+2 < size
                    jMoins1 = j-1 > 0
                    tempLongueur = longueur
                    tempI = i
                    while i < size and longueur > 0:
                        matrice[i][j] = 1
                        if jPlus1:
                            if matrice[tempI][j+1] == 2:
                                matrice[i][j+1] = 2
                            else:
                                matrice[i][j+1] = 1
                                if jPlus2:
                                    matrice[i][j+2] = 2
                        if jMoins1:
                            matrice[i][j-1] = 2
                        longueur -= 1
                        i += 1
                    i = tempI
                    if i+tempLongueur < size:
                        matrice[i+tempLongueur][j] = 2
                        if jPlus1:
                            if matrice[i+tempLongueur-1][j+1] == 2:
                                matrice[i+tempLongueur][j+1] = 2
                            else:
                                matrice[i+tempLongueur][j+1] = 2
                                if jPlus2:
                                    matrice[i+tempLongueur][j+2] = 2
                        if jMoins1:
                            matrice[i+tempLongueur][j-1]=2
                    if i-1 > 0:
                        matrice[i-1][j] = 2
                        if jPlus1:
                            if matrice[i][j+1] == 2:
                                matrice[i-1][j+1] = 2
                            else:
                                matrice[i-1][j+1] = 2
                                if jPlus2:
                                    matrice[i-1][j+2] = 2
                        if jMoins1:
                            matrice[i-1][j-1] = 2
                    j += 2
            else:
                 j += 1

def road_direction(matrice):
    # Direction aux routes : Vertical=30; Horizontal=31; T=40 41 42 43; L=50 51 52 53 54 Croisement=60
    size = len(matrice)
    for i in range (0, size):
        for j in range (0, size):
            up = 0
            down = 0
            left = 0
            right = 0
            if matrice[i][j] == 2:
                if j > 0:
                    if matrice[i][j-1] > 1:
                        left = 1
                if j+1 < size:
                    if matrice[i][j+1] > 1:
                        right = 1
                if i > 0:
                    if matrice[i-1][j] > 1:
                        up = 1
                if i+1 < size:
                    if matrice[i+1][j] > 1:
                        down = 1
                
                if up and down and left and right:
                    matrice[i][j]=60
                elif up and down and right:
                    matrice[i][j]=40
                elif up and down and left:
                    matrice[i][j]=41
                elif up and left and right:
                    matrice[i][j]=42
                elif down and left and right:
                    matrice[i][j]=43
                elif up and right:
                    matrice[i][j]=50
                elif right and down:
                    matrice[i][j]=51
                elif down and left:
                    matrice[i][j]=52
                elif left and up:
                    matrice[i][j]=53
                elif up or down:
                    matrice[i][j]=30
                elif right or left:
                    matrice[i][j]=31

def test_right_neighbor(matrice, val, return_bool=True):
    matriceMap = (matrice == val).astype(int)
    matriceMapHoriz = np.roll(matriceMap, -1, 1)
    matriceMapHoriz[:,-1:].fill(0)
    matriceMapHoriz += matriceMap
    if (return_bool):
        return (matriceMapHoriz >= 2)
    else:
        return matriceMapHoriz

def test_below_neighbor(matrice, val, return_bool=True):
    matriceMap = (matrice == val).astype(int)
    matriceMapVert = np.roll(matriceMap, -1, 0)
    matriceMapVert[-1:].fill(0)
    matriceMapVert += matriceMap
    if (return_bool):
        return (matriceMapVert >= 2)
    else:
        return matriceMapVert

def find_first_pattern(matrice, pattern):
    out = np.zeros_like(matrice)
    coord = np.transpose(np.nonzero(matrice))
    shape = np.transpose(np.nonzero(pattern))

    for i in coord:
        slicex = i[0] + pattern.shape[0]
        slicey = i[1] + pattern.shape[1]
        sub_m = matrice[i[0]:slicex, i[1]:slicey]
        found_shape = ((sub_m == pattern).all() and sub_m.shape == pattern.shape)
        if found_shape:
            out[i[0]:slicex, i[1]:slicey] = 2
            out[i[0]][i[1]] = 1
            break

    return out

def mark_all_patterns(matrice, pattern, pattern_val=1, pos_val=-1, fill_val=10):
    while pattern_val != pos_val:
        grid = (matrice == pattern_val).astype(int)
        m = find_first_pattern(grid, pattern)
        if m.any():
            matrice[m == 1] = pos_val
            matrice[m == 2] = fill_val
        else:
            break

def mark_pattern(matrice, pattern, pattern_val=1, pos_val=-1, fill_val=10):
    if pattern_val != pos_val:
        grid = (matrice == pattern_val).astype(int)
        m = find_first_pattern(grid, pattern)
        if m.any():
            matrice[m == 1] = pos_val
            matrice[m == 2] = fill_val
            return True
    return False

#Parks in the city
def park_creation(matrice, park_mean):
    size = len(matrice)
    pcPark = park_mean
    nbrOfBuildings = sum(sum(matrice == 1))
    nbrOfParks = floor(nbrOfBuildings*pcPark)

    for i in range (0, nbrOfParks):
        keepSearching = True
        x = random.randint(0,size-1)
        y = random.randint(0,size-1)
        while keepSearching:
            if matrice[x][y] == 1:
                matrice[x][y] = -1
                keepSearching = False
            else:
                y += 1
                if y == size:
                    y = 0
                    x += 1
                    if x == size:
                        x = 0

    mark_all_patterns(matrice, np.array([[1,1], [1,1]]), -1, -20, 10)
    mark_all_patterns(matrice, np.array([[1,1]]), -1, -10, 10)
    mark_all_patterns(matrice, np.array([[1], [1]]), -1, -15, 10)

def find_nearest(array, value):
    idx = (np.abs(array-value)).argmin()
    return array[idx]

def building_repartition(matrice, buildings, height_mean, height_std):
    heightmap = {(b.dimensions[2]*6):i for i,b in enumerate(buildings)}
    block_wide = {(b.dimensions[2]*6):np.sum(np.array(b['shape'])) for b in buildings}
    distrib = np.array([], dtype=int)
    heights = np.array(list(block_wide.keys()))

    blocks = (matrice == 1).astype(int)
    free_space = blocks.sum()

    while free_space > 0:
        val = random.normalvariate(height_mean, height_std)
        key = find_nearest(heights, val)
        if free_space - block_wide[key] >= 0:
            distrib = np.append(distrib, heightmap[key])
            free_space = free_space - block_wide[key]
        else:
            heights = np.delete(heights, np.nonzero((heights == key)))

    for key in distrib:
        shape = np.array(buildings[key]['shape'])
        mark_pattern(matrice, shape, 1, buildings[key]['index'], 10)


def draw_roads_and_buildings(size, roads, buildings, max_block_size, parks, park_mean, height_mean, height_std):
    scene = bpy.context.scene

    """bpy.ops.mesh.primitive_plane_add(location=(size, size, 0))    # add plane
    floor = bpy.context.object                              # just added object
    floor.name = 'Terrain'                                  # change name
    floor.scale = (size, size, 1)                           # resize
    """

    roadStraight = roads["straight"]
    roadT = roads["roadT"]
    roadL = roads["roadL"]
    roadX = roads["roadX"]

    city = bpy.data.objects['City']

    bpy.ops.object.add(type='EMPTY')
    road = bpy.context.object
    road.name = 'Road'
    road.parent = city

    bpy.ops.object.add(type='EMPTY')
    b_rep = bpy.context.object
    b_rep.name = 'Buildings'
    b_rep.parent = city

    bpy.ops.object.add(type='EMPTY')
    p_rep = bpy.context.object
    p_rep.name = 'parks'
    p_rep.parent = city

    matrice = np.zeros((size, size), int)
    floor_repartition(matrice, size, max_block_size)
    road_direction(matrice)
    park_creation(matrice, park_mean)
    building_repartition(matrice, buildings, height_mean, height_std)

    buildings_index = {b['index']:i for i,b in enumerate(buildings)}

    #np.savetxt("C:/Program Files/Blender Foundation/Blender/2.72/scripts/addons/Easy-City/matrice.txt", matrice, fmt='%1.0f,')

    for i in range (0, len(matrice)):
        for j in range (0, len(matrice[0])):
            if matrice[i][j] == 30:
                newRoad = roadStraight.copy()
                scene.objects.link(newRoad)
                newRoad.location = (2*i, 2*j, 0)
                bpy.ops.object.select_all(action='DESELECT')
                newRoad.select=True
                bpy.ops.transform.rotate(value=-1.5708, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                newRoad.select=False
                newRoad.parent = road
            elif matrice[i][j] == 31:
                newRoad = roadStraight.copy()
                scene.objects.link(newRoad)
                newRoad.location = (2*i, 2*j, 0)
                newRoad.parent = road
            elif matrice[i][j] == 40:
                newRoad = roadT.copy()
                scene.objects.link(newRoad)
                newRoad.location = (2*i, 2*j, 0)
                bpy.ops.object.select_all(action='DESELECT')
                newRoad.select=True
                bpy.ops.transform.rotate(value=1.5708, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                newRoad.select=False
                newRoad.parent = road
            elif matrice[i][j] == 41:
                newRoad = roadT.copy()
                scene.objects.link(newRoad)
                newRoad.location = (2*i, 2*j, 0)
                bpy.ops.object.select_all(action='DESELECT')
                newRoad.select=True
                bpy.ops.transform.rotate(value=-1.5708, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                newRoad.select=False
                newRoad.parent = road
            elif matrice[i][j] == 42:
                newRoad = roadT.copy()
                scene.objects.link(newRoad)
                newRoad.location = (2*i, 2*j, 0)
                bpy.ops.object.select_all(action='DESELECT')
                newRoad.select=True
                bpy.ops.transform.rotate(value=3.14159, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                newRoad.select=False
                newRoad.parent = road
            elif matrice[i][j] == 43:
                newRoad = roadT.copy()
                scene.objects.link(newRoad)
                newRoad.location = (2*i, 2*j, 0)
                bpy.ops.object.select_all(action='DESELECT')
                newRoad.select=True
                bpy.ops.transform.rotate(value=0, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                newRoad.select=False
                newRoad.parent = road

            elif matrice[i][j] == 50:
                newRoad = roadL.copy()
                scene.objects.link(newRoad)
                newRoad.location = (2*i, 2*j, 0)
                bpy.ops.object.select_all(action='DESELECT')
                newRoad.select=True
                bpy.ops.transform.rotate(value=3.14159, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                newRoad.select=False
                newRoad.parent = road
            elif matrice[i][j] == 51:
                newRoad = roadL.copy()
                scene.objects.link(newRoad)
                newRoad.location = (2*i, 2*j, 0)
                bpy.ops.object.select_all(action='DESELECT')
                newRoad.select=True
                bpy.ops.transform.rotate(value=1.5708, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                newRoad.select=False
                newRoad.parent = road
            elif matrice[i][j] == 52:
                newRoad = roadL.copy()
                scene.objects.link(newRoad)
                newRoad.location = (2*i, 2*j, 0)
                bpy.ops.object.select_all(action='DESELECT')
                newRoad.select=True
                bpy.ops.transform.rotate(value=0, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                newRoad.select=False
                newRoad.parent = road
            elif matrice[i][j] == 53:
                newRoad = roadL.copy()
                scene.objects.link(newRoad)
                newRoad.location = (2*i, 2*j, 0)
                bpy.ops.object.select_all(action='DESELECT')
                newRoad.select=True
                bpy.ops.transform.rotate(value=-1.5708, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                newRoad.select=False
                newRoad.parent = road
            
            elif matrice[i][j] == 60:
                newRoad = roadX.copy()
                scene.objects.link(newRoad)
                newRoad.location = (2*i, 2*j, 0)
                newRoad.parent = road

            elif matrice[i][j] >= 100:
                newbuild = buildings[buildings_index[matrice[i][j]]].copy()
                scene.objects.link(newbuild)
                newbuild.location = (2*i, 2*j, 0)
                bpy.ops.object.select_all(action='DESELECT')
                newbuild.select=True

                if "house" in newbuild.name:
                    if i>0 and i+1<size and j>0 and j+1<size:
                        if matrice[i-1][j]>1 and matrice[i-1][j]<100:
                            bpy.ops.transform.rotate(value=-3.14159, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                        elif matrice[i][j-1]>1 and matrice[i][j-1]<100:
                            bpy.ops.transform.rotate(value=-1.5708, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                        elif matrice[i][j+1]>1 and matrice[i][j+1]<100:
                            bpy.ops.transform.rotate(value=1.5708, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    elif i==0:
                        bpy.ops.transform.rotate(value=-3.14159, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    elif j==0:
                        bpy.ops.transform.rotate(value=-1.5708, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    elif j+1==size:
                        bpy.ops.transform.rotate(value=1.5708, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                elif np.sum(np.array(newbuild["shape"])) == 1:
                    bpy.ops.transform.rotate(value=random.sample([0, -3.14159, 1.5708, -1.5708],  1)[0], axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                newbuild.select=False
                newbuild.parent = b_rep

            elif matrice[i][j] == -1:
                newPark=parks[random.randint(0, 1)].copy()
                newPark.location = (2*i, 2*j, 0)
                scene.objects.link(newPark)
                newPark.parent = p_rep
            elif matrice[i][j] == -10:
                newPark=parks[2].copy()
                newPark.location = (2*i, 2*j, 0)
                scene.objects.link(newPark)
                newPark.parent = p_rep
            elif matrice[i][j] == -15:
                newPark=parks[2].copy()
                scene.objects.link(newPark)
                newPark.location = (2*i, 2*j, 0)
                bpy.ops.object.select_all(action='DESELECT')
                newPark.select=True
                bpy.ops.transform.rotate(value=-1.5708, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                newPark.parent = p_rep
            elif matrice[i][j] == -20:
                newPark=parks[3].copy()
                newPark.location = (2*i, 2*j, 0)
                scene.objects.link(newPark)
                newPark.parent = p_rep
    cameraPath(matrice)
    return matrice


def cameraPath(matrice):
    bpy.ops.object.select_all(action='DESELECT')
    camera = bpy.data.objects.get('Camera') 
    bpy.context.scene.frame_current = 0
    speed=12
    vidLimit=25

    size=len(matrice)
    i=math.floor(size/2)
    j=i
    z=60
    iAngle=0
    jAngle=0
    zAngle=0
    camera.select=True
    camera.data.lens = 10.5

    if matrice[i][j]>1:
        i=j
    elif matrice[i+1][j]>1:
        i+=1
    elif matrice[i-1][j]>1:
        i-=1
    elif matrice[i][j+1]>1:
        j+=1
    elif matrice[i][j-1]>1:
        j-=1
        
    if matrice[i][j]==30:
        if random.randint(0,1):
            zAngle=math.radians(90)
        else:
            zAngle=-math.radians(90)


    while z>10:
        camera.location=[2*i,2*j,z]
        camera.rotation_euler=[iAngle,jAngle,zAngle]
        camera.select=True
        bpy.ops.anim.keyframe_insert_menu(type='Location')
        bpy.ops.anim.keyframe_insert_menu(type='Rotation')
        bpy.context.scene.frame_current +=speed
        z-=10

    iAngle=math.radians(100)
    camera.rotation_euler=[iAngle,jAngle,zAngle]

    while i>=0 and j>=0 and i<size and j<size and vidLimit>0:
        vidLimit-=1
        camera.location=[2*i,2*j,0.5]
        if matrice[i][j]==30:
            camera.select=True
            bpy.ops.anim.keyframe_insert_menu(type='Location')
            bpy.ops.anim.keyframe_insert_menu(type='Rotation')
            bpy.context.scene.frame_current +=speed
            if (math.degrees(zAngle)%360-90)**2<2:
                i-=1                    
            else:
                i+=1
        elif matrice[i][j]==31:
            camera.select=True
            bpy.ops.anim.keyframe_insert_menu(type='Location')
            bpy.ops.anim.keyframe_insert_menu(type='Rotation')
            bpy.context.scene.frame_current +=speed
            if ((math.degrees(zAngle)+1)%360)**2<3:
                j+=1
            else:
                j-=1
        
        else:       
            left=False
            right=False
            up=False
            down=False
            coeff=0
            if (math.degrees(zAngle)%360-270)**2<1 or (math.degrees(zAngle)%360-90)**2<1:
                if matrice[i][j]==42 or matrice[i][j]==43 or matrice[i][j]==60:
                    if random.randint(0,1):
                        right=True
                    else:
                        left=True
                elif matrice[i][j]==40 or matrice[i][j]==50 or matrice[i][j]==51:
                    right=True
                elif matrice[i][j]==41 or matrice[i][j]==52 or matrice[i][j]==53:
                    left=True
                else:
                    print("vertical error crossing")
                if ((math.degrees(zAngle)%360-270)**2<1 and left) or ((math.degrees(zAngle)%360-90)**2<1 and right):
                    coeff=1
                else:
                    coeff=-1
            elif ((math.degrees(zAngle)+1)%360)**2<3 or (math.degrees(zAngle)%360-180)**2<1:
                if matrice[i][j]==40 or matrice[i][j]==41 or matrice[i][j]==60:
                    if random.randint(0,1):
                        up=True
                    else:
                        down=True
                elif matrice[i][j]==42 or matrice[i][j]==50 or matrice[i][j]==53:
                    up=True
                elif matrice[i][j]==43 or matrice[i][j]==51 or matrice[i][j]==52:
                    down=True
                else:
                    print("horizontal error crossing : ", matrice[i][j])
                if (((math.degrees(zAngle)+1)%360)**2<3 and down) or ((math.degrees(zAngle)%360-180)**2<1 and up):
                    coeff=1
                else:
                    coeff=-1
            else:
                print("error zAngle", math.degrees(zAngle)%360**2)
            jAngle=(math.radians(45)*coeff)/2
            zAngle-=(math.radians(45)*coeff)
            camera.rotation_euler=[iAngle,jAngle,zAngle]
            camera.select=True
            bpy.ops.anim.keyframe_insert_menu(type='Location')
            bpy.ops.anim.keyframe_insert_menu(type='Rotation')
            bpy.context.scene.frame_current +=speed
            jAngle=0
            zAngle-=(math.radians(45)*coeff)
            camera.rotation_euler=[iAngle,jAngle,zAngle]
            if ((math.degrees(zAngle)+1)%360)**2<3:
                j+=1
            elif (math.degrees(zAngle)%360-90)**2<1:
                i-=1
            elif (math.degrees(zAngle)%360-180)**2<1:
                j-=1
            else:
                i+=1
                

    nextJ=True
    iAngle=math.radians(45)
    zAngle=math.radians(-45)
    i=0;j=0;z=size/2
    for k in range(0,4):        
        camera.rotation_euler=[iAngle,jAngle,zAngle]
        camera.location=[i,j,size]
        camera.select=True
        bpy.ops.anim.keyframe_insert_menu(type='Location')
        bpy.ops.anim.keyframe_insert_menu(type='Rotation')
        bpy.context.scene.frame_current +=speed*2
        zAngle-=math.radians(90)
        if nextJ:
            j=((j+1)%(2*size+1))*2*size
            nextJ=False
        else:
            i=((i+1)%(2*size+1))*2*size
            nextJ=True





            
        #delete camera path
    """for i in range(0,1500):
        bpy.context.scene.frame_current=i
        bpy.ops.anim.keyframe_delete_v3d()"""



# Direction aux routes : Vertical=30; Horizontal=31; T=40 41 42 43; L=50 51 52 53 54 Croisement=60
def carsAnim(matrice, cars):
    city = bpy.data.objects['City']
    bpy.ops.object.add(type='EMPTY')
    car_rep = bpy.context.object
    car_rep.name = 'Cars'
    car_rep.parent = city  
    listCar=[]
    size=len(matrice)
    for i in range(0, size):
        for j in range(0,size):
            tempJ=(random.randint(0,12)-6)/10
            if matrice[i][j]==30:
                a=1
            elif matrice[i][j]==31:
                newCar=cars[random.randint(0, len(cars)-1)].copy()
                bpy.context.scene.objects.link(newCar)
                newCar.parent = car_rep
                if random.randint(0,1):     #to left
                    if random.randint(0,1):
                        newCar.location = (2*i-0.6, 2*j+tempJ, 0)
                    else:
                        newCar.location = (2*i-0.2, 2*j+tempJ, 0)
                    listCar.append([newCar,i,j,0])

                else:       #to right
                    newCar.rotation_euler=[0,math.radians(90),math.radians(180)]
                    if random.randint(0,1):
                        newCar.location = (2*i+0.6, 2*j+tempJ, 0)
                    else:
                        newCar.location = (2*i+0.2, 2*j+tempJ, 0)
                    listCar.append([newCar,i,j,1])

    bpy.context.scene.frame_current = 0
    for k in range(0,100):
        i=0
        while i<len(listCar):
            bpy.ops.object.select_all(action='DESELECT')
            listCar[i][0].select=True
            bpy.ops.anim.keyframe_insert_menu(type='Location')
            bpy.ops.anim.keyframe_insert_menu(type='Rotation')
            if listCar[i][3]==0:
                if listCar[i][0].location[1]+1<size:
                    listCar[i][2]-=1
                    listCar[i][0].location[1]-=2
                else:
                    bpy.ops.object.delete(use_global=False)
                    del listCar[i]

            elif listCar[i][3]==1:
                if listCar[i][0].location[1]-1>0:
                    listCar[i][2]+=1
                    listCar[i][0].location[1]+=2
                else:
                    print("allo ?")
                    bpy.ops.object.delete(use_global=False)
                    del listCar[i]
            elif listCar[i][3]==2:
                print("ok")
            elif listCar[i][3]==3:
                print("ok")
            i+=1
        bpy.context.scene.frame_current +=34
