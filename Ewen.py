import numpy as np
import pandas as pd
import heapq
import matplotlib.pyplot as plt
from code.py import trouver_evenement_pro

clients = pd.read_csv("C:/Users/utilisateur/Info/hackaton/clients.csv")
plants = pd.read_csv("C:/Users/utilisateur/Info/hackaton/plants.csv")

v = 50
temps = 0


def map():
    X = plants.coord_x
    Y = plants.coord_y
    W = clients.coord_x
    Z = clients.coord_y
    plt.scatter(W, Z, label="Clients")
    plt.scatter(X, Y, label="Usines")
    plt.show()


# Programme qui affiche la carte avec les localisations des clients et des usines


def distance(x1, y1, x2, y2):
    return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# Programme qui calcule la distance entre 2 points


def mouvement_camion(camion, t):
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


### Programme qui donne le mouvement d'un camion vers sa destination
# (usine : qui correspond à camion[4] ou client : qui correspond à camion[5], sachant qu'on ne peut pas se diriger vers 2 lieux, au moins un des deux est None)
# après un temps t qui va être relié au temps entre deux évènements


def arrivee_camion(camion):
    if camion[4] != None and camion[5] == None:
        camion[0] = plants[camion[4]].coord_x
        camion[1] = plants[camion[4]].coord_y
        camion[2] = 0
        camion[3] = max(80, plants[camion[4]].init)
        plants[camion[4]].init -= camion[3]
        camion[4] = None
        distance_client = 10 ^ 9
        for k in range(clients.shape[0]):
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

    elif camion[4] == None and camion[5] != None:
        camion[0] = clients[camion[5]].coord_x
        camion[1] = clients[camion[5]].coord_y
        camion[3] = max(0, camion[3] - min(7 * clients[camion[5]].consumption, clients[camion[5]].capacity))
        camion[2] = min(80, camion[2] + min(7 * clients[camion[5]].consumption, clients[camion[5]].capacity))
        if camion[3] == 0:
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
        if camion[3] != 0:
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


### Programme qui donne ce que fait un camion en arrivant à un lieu
# soit à une usine dans ce cas il décharge ses bouteilles vides (camion[2]) et récupère des bouteilles pleines (soit 80 si l'usine peut en fournir autant, soit le nombre max de ce que peut fournir l'usine)
# puis il va chez le client qui a besoin de bouteilles et pour lequel il n'y a pas de camion en chemin (statut = 1) le plus proche
# soit chez un client et donc si le camion n'a plus de bouteilles pleines il retourne à l'usine la plus proche, sinon il va chez le client le plus proche qui a besoin de bouteilles et pour lequel il n'y a pas de camion en chemin


def evolution(camions):
    k = trouver_evenement_pro()[0]
    t = trouver_evenement_pro()[1]
    camions[k] = arrivee_camion(camions[k])
    for i in range(len(camions)):
        if i != k:
            camions[i] = mouvement_camion(camions[i], t)
    for k in range(plants.shape[0]):
        if plants[k].init + plants[k].refill * t / 24 < plants[k].capacity:
            plants[k].init = plants[k].init + plants[k].refill * t / 24
    for k in range(clients.shape[0]):
        if clients[k].