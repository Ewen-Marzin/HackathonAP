import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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
