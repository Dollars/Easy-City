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

def draw_roads_and_buildings(size, roads, buildings, max_block_size, parks, park_mean):
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

    np.savetxt("C:/Program Files/Blender Foundation/Blender/2.72/scripts/addons/Easy-City/matrice.txt", matrice, fmt='%1.0f,')

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

            elif matrice[i][j] == 1:
                newbuild = buildings[random.randint(0, len(buildings)-1)].copy()
                scene.objects.link(newbuild)
                newbuild.location = (2*i, 2*j, 0)
                bpy.ops.object.select_all(action='DESELECT')
                newbuild.select=True
                if "house" in newbuild.name:
                    if i>0 and i+1<size and j>0 and j+1<size:
                        if matrice[i-1][j]>1:
                            bpy.ops.transform.rotate(value=-3.14159, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                        elif matrice[i][j-1]>1:
                            bpy.ops.transform.rotate(value=-1.5708, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                        elif matrice[i][j+1]>1:
                            bpy.ops.transform.rotate(value=1.5708, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    elif i==0:
                        bpy.ops.transform.rotate(value=-3.14159, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    elif j==0:
                        bpy.ops.transform.rotate(value=-1.5708, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    elif j+1==size:
                        bpy.ops.transform.rotate(value=1.5708, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                else:
                    bpy.ops.transform.rotate(value=random.sample([0, -3.14159, 1.5708, -1.5708],  1)[0], axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                newbuild.select=False
                newbuild.parent = b_rep
            elif matrice[i][j] == -1:
                newPark=parks[random.randint(0, len(parks)-1)].copy()
                newPark.location = (2*i, 2*j, 0)
                scene.objects.link(newPark)
                newPark.parent = p_rep