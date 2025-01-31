import numpy as np
import pygame as pg

clients = pd.read_csv('C:/Users/utilisateur/Info/hackaton/clients.csv')
plants = pd.read_csv('C:/Users/utilisateur/Info/hackaton/plants.csv')

def map ():
    X=plants.coord_x
    Y=plants.coord_y
    W=clients.coord_x
    Z=clients.coord_y
    plt.scatter(W,Z, label ="Clients")
    plt.scatter(X,Y, label ="Usines")
    plt.show()


pg.init()
clock = pg.time.Clock()
running = True
while running:
    clock.tick(10)

def distance(x1, y1, x2, y2):
    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def deposer_bouteilles_usine(nb_bouteillev, stockage):
    depot = min(nb_bouteillev, refill)
    stockage = stockage + depot

def consommer(clients):
    for i in range(len(clients)):
        x, y, capacity, stock, consumption = clients[i]
        stock = max(0, stock - consumption)
        clients[i] = (x, y, capacity, stock, consumption)