import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


clients = pd.read_csv('C:/Users/utilisateur/Info/hackaton/clients.csv')     #2000 clients
plants = pd.read_csv('C:/Users/utilisateur/Info/hackaton/plants.csv')   #20 usines

clients["status"]=[1 for i in range (2000)]
clients["bouteilles_pleines"]=[0 for i in range (2000)]



def distance (a,b,c,d) :
    return np.sqrt((a-c)**2+(b-d)**2)


def init_cametards():       #initialisation des camions
    camions = [[0,0,0,0,0,0] for i in range (100)]      #(x,y,bouteilles vides, bouteilles pleines, objectif usine, objectif client)
    for i in range (20):

        stock = plants.init[i]      # remplissage des camions
        tkt=np.floor(stock/5)
        reste=stock-tkt
        for j in range (i*5, i*5 +reste):
            camions[j][0],camions[j][1] = plants.coord_x[i], plants.coord_y[i]
            camions[j][3]=tkt+1
        for j in range (i*5+reste, 5+i*5):
            camions[j][0],camions[j][1] = plants.coord_x[i], plants.coord_y[i]
            camions[j][3]=tkt

        def trietpastriselectiftascapteahah(i):         # on choisit les 5 clients demandeurs les plus proches
            res=[]
            for c in range (2000):
                res.append(distance(clients[c].coord_x,clients[c].coord_y,plants.coord_x[i], plants.coord_y[i]))
            res.sort()
            return res[:5]

        tkt= trietpastriselectiftascapteahah(i)
        for j in range (i*5, 5+i*5):
            camions[j][5]=res[j-5*i]


camions = init_cametards()


def show_map ():
    X=plants.coord_x
    Y=plants.coord_y
    W=clients.coord_x
    Z=clients.coord_y
    plt.scatter(W,Z, label ="Clients", s=10)
    plt.scatter(X,Y, label ="Usines",s=50)
    X=[camions[i][0] for i in range (100)]
    Y=[camions[i][1] for i in range (100)]
    plt.scatter(X,Y,s=30)
    plt.show()



def trouver_evenement_pro ():
    cpt=10**9
    cametarddesesmorts=camion[0]

    for camion in camions :

        if camion[4] != None and camion[5] == None:
            a=distance (camion[0], camion[1], plants[camion[4]].coord_x, plants[camion[4]].coord_y)
            if a<cpt:
                cametarddesesmorts=camion
                cpt=a

        elif camion[4] == None and camion[5] != None:
            a=distance (camion[0], camion[1], clients[camion[5]].coord_x, clients[camion[5]].coord_y)
            if a<cpt:
                cametarddesesmorts=camion
                cpt=a

        return (cametarddesesmorts, cpt/v)








def mouvement_camions(camion, t):
    if camion[4] != None and camion[5] == None:
        for camion in camions:
            d = distance(
                camion[0],
                camion[1],
                plants[camion[4]].coord_x,
                plants[camion[4]].coord_y,
            )
            direction = (
                (plants[camion[4]].coord_x - camion[0]) / d,
                plants[camion[4]].coord_y - camion[1] / d,
            )
            camion[0] += v * t * direction[0]
            camion[1] += v * t * direction[1]
    elif camion[4] == None and camion[5] != None:
        d = distance(
            camion[0], camion[1], clients[camion[5]].coord_x, clients[camion[5]].coord_y
        )
        direction = (
            (plants[camion[4]].coord_x - camion[0]) / d,
            plants[camion[4]].coord_y - camion[1] / d,
        )
        camion[0] += v * t * direction[0]
        camion[1] += v * t * direction[1]
    return camion


def arrivee_camion(camion):
    if camion[4] != None and camion[5] == None:
        camion[2] = 0
        camion[3] = max(80, plants[camion[4]].init)
        m = 10 ^ 9
        for k in range(clients.shape[0]):
            if (
                clients[k].status == 2
                and distance(
                    camion[0], camion[1], clients[k].coord_x, clients[k].coord_y
                )
                < m
            ):
                camion[5] = k
                m = distance(
                    camion[0], camion[1], clients[k].coord_x, clients[k].coord_y
                )

    elif camion[4] == None and camion[5] != None:
            camion[5] = None
    return camion



def quoicoubeh ():
    horloge =0
    camions = init_cametards()
    heapq= fonctionIlias

    while horloge <=30*24:
        a=heapq.push_back
        camion, horloge = a[0],a[1]
        arrivee_camion(camion)
        for camtarddesesmorts in camions :
            if camtarddesesmorts!=camion:
                mouvement_camions(camtarddesesmorts)







