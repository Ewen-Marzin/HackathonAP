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

def charge(n):
    capacite_actuelle = capacite - (bouteilles_vides_v + bouteilles_pleines_v)
    if n <= capacite_actuelle:
        if bouteilles_pleines:
            bouteilles_pleines_v += n
        else:
            bouteilles_vides_v += n

def decharge(n):
    if bouteilles_pleines:
        if n <= bouteilles_pleines_v:
            bouteilles_pleines_v = bouteilles_pleines_v - n
    else:
        if n <= bouteilles_vides_v:
            bouteilles_vides_v = bouteilles_vides_v - n

def decharge(self, n, bouteilles_pleines:'bool'):
        if bouteilles_pleines:
            if n <= self._bouteilles_pleines:
                self._bouteilles_pleines = self._bouteilles_pleines - n
            else:
                return False
        else:
            if n <= self._bouteilles_vides:
                self._bouteilles_vides = self._bouteilles_vides - n
            else:
                return False
