import numpy as np
import random

#Principe : Parcours classique de la matrice. Quand m[i][j]=0, création d'un bloc de building (m[][]=2), de largeur 2 (ou 1 quand ce n'est pas possible autrement) et de taille random (entre 2 et tailleMaxBloc) positionner
#horizontalement ou verticalement. Le bloc est ensuite entouré de rue (m[][]=1). Répété jusqu'au remplissage de la matrice.

tailleMaxBloc=10
size=100
matrice=np.zeros((size,size),int)
i=0;j=0;count=0

for i in range (0,size):
    j=0
    while j<size:
        if matrice[i][j]==0:
            longueur=random.randint(2,tailleMaxBloc)
            
            #Si 3 cases horizontales, pas de bloc vertical, sinon route de largeur 2.
            cntLong=0
            for k in range(j,size):
                if matrice[i][k]==0:
                    cntLong+=1
                else:
                    break;
            if cntLong==3:
                longueur=3
                horizontal=1
            else:
                horizontal=random.randint(0,1)
               
            #creation building m[][]=2 entouré de route m[][]=1
            
            #longueur horizontal
            if horizontal: 
                if cntLong>=longueur:
                    if j+longueur+1<size:
                        if matrice[i][j+longueur+1]==1 and matrice[i][j+longueur]==0:
                            longueur+=1
                else:
                    longueur=cntLong
                       
                iPlus1=i+1<size 
                iPlus2=i+2<size
                iMoins1=i-1>0
                tempLongueur=longueur
                tempJ=j
                while j<size and longueur>0:
                    matrice[i][j]=2
                    if iPlus1:
                        matrice[i+1][j]=2
                    if iPlus2:
                        matrice[i+2][j]=1
                    if iMoins1:
                        matrice[i-1][j]=1
                    longueur-=1
                    j+=1
                if tempJ-1>0:
                    matrice[i][tempJ-1]=1
                    if iPlus1:
                        matrice[i+1][tempJ-1]=1
                    if iPlus2:
                        matrice[i+2][tempJ-1]=1
                    if iMoins1:
                        matrice[i-1][tempJ-1]=1
                if j<size:
                    matrice[i][j]=1
                    if iPlus1:
                        matrice[i+1][j]=1
                    if iPlus2:
                        matrice[i+2][j]=1
                    if iMoins1:
                        matrice[i-1][j]=1
                        
            else: #longueur vertical
                jPlus1=j+1<size
                jPlus2=j+2<size
                jMoins1=j-1>0
                tempLongueur=longueur
                tempI=i
                while i<size and longueur>0:
                    matrice[i][j]=2
                    if jPlus1:
                        if matrice[tempI][j+1]==1:
                            matrice[i][j+1]=1
                        else:
                            matrice[i][j+1]=2;
                            if jPlus2:
                                matrice[i][j+2]=1
                    if jMoins1:
                        matrice[i][j-1]=1
                    longueur-=1
                    i+=1
                i=tempI
                if i+tempLongueur<size:
                    matrice[i+tempLongueur][j]=1
                    if jPlus1:
                        if matrice[i+tempLongueur-1][j+1]==1:
                            matrice[i+tempLongueur][j+1]=1
                        else:
                            matrice[i+tempLongueur][j+1]=1;
                            if jPlus2:
                                matrice[i+tempLongueur][j+2]=1
                    if jMoins1:
                        matrice[i+tempLongueur][j-1]=1
                if i-1>0:
                    matrice[i-1][j]=1
                    if jPlus1:
                        if matrice[i][j+1]==1:
                            matrice[i-1][j+1]=1
                        else:
                            matrice[i-1][j+1]=1;
                            if jPlus2:
                                matrice[i-1][j+2]=1
                    if jMoins1:
                        matrice[i-1][j-1]=1 
                j+=2
        else:
             j+=1
 
 
#Verification qu'aucune route ne fait 2 carrés de large                
"""i=0;j=0
for i in range (0,size-1):
    for j in range (0,size-1):
        if matrice[i][j]==1 and matrice[i+1][j]==1 and matrice [i][j+1]==1 and matrice [i+1][j+1]==1:
             print("Chemin foireux",i,j)"""


print(matrice)                
print(" ")
print(" ")