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

def charger_donnees(fichier):
    instances = []
    with open(fichier, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Ignorer l'en-tête
        for ligne in reader:
            instances.append((float(ligne[0]), float(ligne[1]), int(ligne[2]), int(ligne[3]), int(ligne[4])))
    return instances

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