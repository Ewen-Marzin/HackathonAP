import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import heapq

## Dataframes 

plants = pd.read_csv('C:/Users/utilisateur/Info/hackaton/plants.csv')   #20 usines
clients = pd.read_csv('C:/Users/utilisateur/Info/hackaton/clients.csv')     #2000 clients
clients["status"]=[1 for i in range (2000)]
clients["bouteilles_pleines"]=[0 for i in range (2000)]

## Fonctions utiles 

def distance (a,b,c,d) :
    return np.sqrt((a-c)**2+(b-d)**2)


def show_map ():        # Si l'envie nous prenait d'afficher ce qu'il se passe 
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

# Fonction au final inutilisée pour trouver l'évenement suivant 
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


## Fonctions dans le programme final

# Initialisation des camions 
def init_cametards():       
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
        for j in range (i*5, 5+i*5):        # Les camions ont maintenant tous une destination !
            camions[j][5]=res[j-5*i]


# On fait avancer tous les camions après un temps dt qui va correspondre au temps séparant deux événements
# (usine correspond à camion[4] et client correspond à camion[5], au moins un des deux est None)
def mouvement_camion(camion, dt):
    if camion[4] != None and camion[5] == None:     #objectif = usine
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
        camion[0] += v * dt * direction[0]
        camion[1] += v * dt * direction[1]

    elif camion[4] == None and camion[5] != None:   #objectif = client
        d = distance(
            camion[0], camion[1], clients[camion[5]].coord_x, clients[camion[5]].coord_y
        )
        direction = (
            (plants[camion[4]].coord_x - camion[0]) / d,
            plants[camion[4]].coord_y - camion[1] / d,
        )
        camion[0] += v * dt * direction[0]
        camion[1] += v * dt * direction[1]
    return camion



# On effectue toutes les actions nécessaires lorque qu'un événement se produit (c'est à dire qu'un camion arrive à un endroit !)
# Soit à une usine dans ce cas il décharge ses bouteilles vides (camion[2]) et récupère des bouteilles pleines (soit 80 si l'usine peut en fournir autant, soit le nombre max de ce que peut fournir l'usine)
# Puis il va chez le client qui a besoin de bouteilles et pour lequel il n'y a pas de camion en chemin (statut = 1) le plus proche
# Soit chez un client et donc si le camion n'a plus de bouteilles pleines il retourne à l'usine la plus proche, sinon il va chez le client le plus proche qui a besoin de bouteilles et pour lequel il n'y a pas de camion en chemin

def arrivee_camion(camion):

    if camion[4] != None and camion[5] == None:     # On arrive à une usine --> on échange les bouteilles 

        camion[0] = plants[camion[4]].coord_x
        camion[1] = plants[camion[4]].coord_y
        camion[2] = 0
        camion[3] = max(80, plants[camion[4]].init)
        plants[camion[4]].init -= camion[3]
        camion[4] = None
        distance_client = 10 ^ 9
        for k in range(clients.shape[0]):       # On cherche le prochain client 
            if (
                clients[k].status == 1
                and distance(
                    camion[0], camion[1], clients[k].coord_x, clients[k].coord_y
                )
                < distance_client
            ):
                camion[5] = k
                distance_client = distance(
                    camion[0], camion[1], clients[k].coord_x, clients[k].coord_y
                )
            clients[camion[5]].status = 2
            return camion

    elif camion[4] == None and camion[5] != None:       # On arrive chez un client --> on échange les bouteilles 
        camion[0] = clients[camion[5]].coord_x
        camion[1] = clients[camion[5]].coord_y
        camion[3] = max(0, camion[3] - min(7 * clients[camion[5]].consumption, clients[camion[5]].capacity))
        camion[2] = min(80, camion[2] + min(7 * clients[camion[5]].consumption, clients[camion[5]].capacity))
        if camion[3] == 0:      # Si le camion n'a plus de bouteilles pleines 
            camion[5] = None
            distance_usine = 10 ^ 9
            for k in range(plants.shape[0]):
                if (
                    distance(camion[0], camion[1], plants[k].coord_x, plants[k].coord_y)
                    < distance_usine
                ):
                    distance_usine = distance(
                        camion[0], camion[1], plants[k].coord_x, plants[k].coord_y
                    )
                    camion[4] = k
            return camion
        if camion[3] != 0:      # Si le camion a encore des bouteilles pleines 
            camion[4] = None
            distance_client = 10 ^ 9
            for k in range(clients.shape[0]):
                if (clients[k].status == 1 and
                    distance(
                        camion[0], camion[1], clients[k].coord_x, clients[k].coord_y
                    )
                    < distance_usine
                ):
                    distance_usine = distance(
                        camion[0], camion[1], clients[k].coord_x, clients[k].coord_y
                    )
                    camion[5] = k
            clients[camion[5]].status = 2
            return camion
    return camion




## Le rendu final ! 

def quoicoubeh ():

    horloge =0
    camions = init_cametards()
    Y=[]

    pq = []
    déplacements_camions=[[(camions[i][0],camions[i][1])] for i in range(100)]
    
    for i in range(100): #initialisation pour tous les camtards
        (x1,y1) = camions[i][0],camions[i][1]
        x = camions[i]
        if x[4] == None : 
            (x2,y2) = (clients[x[5]][0], clients[x[5]][1])
        else : 
            (y2,x2) = (usines[x[4]][0], usines[x[4]][1])
        déplacements_camions[i].append((x2,y2))
        y = distance(x1,y1,x2,y2)/v
        heapq.heappush(y,i)


    while horloge <=30*24:

        (horloge, camion) = heapq.heappop(pq)
        x = camion
        (x1,y1) = camion[0],camion[1]
        if x[4] == None : 
            (x2,y2) = (clients[x[5]][0], clients[x[5]][1])
        else : 
            (y2,x2) = (usines[x[4]][0], usines[x[4]][1])
        déplacements_camions[i].append((x2,y2))
        y = distance(x1,y1,x2,y2)/v
        Y.append(y)
        heapq.heappush(horloge+y,camion)

        arrivee_camion(camion)
        for camtarddesesmorts in camions :
            if camtarddesesmorts!=camion:
                mouvement_camion(camtarddesesmorts, Y[-2])
        for k in range(plants.shape[0]):
            if plants[k].init + plants[k].refill * t / 24 < plants[k].capacity:
                plants[k].init = plants[k].init + plants[k].refill * t / 24
        for k in range(clients.shape[0]):
            if clients[k].bouteilles_pleines - clients[k].consumption * t / 24 != 0:
                clients[k].bouteilles_pleines -= clients[k].consumption * t / 24
    






