import numpy as np
import pandas as pd
import heapq
import matplotlib.pyplot as plt

clients = pd.read_csv("C:/Users/utilisateur/Info/hackaton/clients.csv")
plants = pd.read_csv("C:/Users/utilisateur/Info/hackaton/plants.csv")

v = 50


def map():
    X = plants.coord_x
    Y = plants.coord_y
    W = clients.coord_x
    Z = clients.coord_y
    plt.scatter(W, Z, label="Clients")
    plt.scatter(X, Y, label="Usines")
    plt.show()


def distance(x1, y1, x2, y2):
    return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


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


def arrivée_camion(camion):
    if camion[4] != None and camion[5] == None:
        d = distance(
            camion[0], camion[1], plants[camion[4]].coord_x, plants[camion[4]].coord_y
        )
        if d == 0:
            camion[2] = 0
            camion[3] = max(80, plants[camion[4]].init)
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
        d = distance(
            camion[0], camion[1], clients[camion[5]].coord_x, clients[camion[5]].coord_y
        )
        if d == 0:
            camion[3] = min(0, camion[3] - 7 * clients[camion[5]].consumption)
            camion[2] = max(80, camion[2] + 7 * clients[camion[5]].consumption)
            if camion[3] == 0:
                camion[5] = None
                distance_usine = 10 ^ 9
                for k in range(plants.shape[0]):
                    if (
                        distance(
                            camion[0], camion[1], plants[k].coord_x, plants[k].coord_y
                        )
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
                    if (
                        distance(
                            camion[0], camion[1], clients[k].coord_x, clients[k].coord_y
                        )
                        < distance_usine
                    ):
                        distance_usine = distance(
                            camion[0], camion[1], clients[k].coord_x, clients[k].coord_y
                        )
                        camion[5] = k
                return camion

    return camion
