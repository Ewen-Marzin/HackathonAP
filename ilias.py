import numpy as np
import pandas as pd

clients = pd.read_csv('C:/Users/Ilias/OneDrive/Desktop/MINES 1A/info/hackathon 2/Hackathon/clients.csv')
usines = pd.read_csv('C:/Users/Ilias/OneDrive/Desktop/MINES 1A/info/hackathon 2/Hackathon/plants.csv')

clients["statut"] = 1

# utilisation d'une file de priorité pour lister les différents évènements 

v=0.05

def évènements(camions):
    pq = []
    t=0
    while t < 30*24*3600 : 
        for i in range(100): #initialisation pour tous les camtards
            (x1,y1) = camions[i][0],camions[i][1]
            x = arrivee_camion(camions[i])
            if x[4] = None : 
                (x2,y2) = (clients[x[5]][0], clients[x[5]][1])
            else : 
                (y2,x2) = (usines[x[4]][0], usines[x[4]][1])
            y = distance(x1,y1,x2,y2)/v
            heapq.heappush(y,i)
        (t,i) = heapq.heappop(pq)
        x = arrivee_camion(camions[i])
        (x1,y1) = camions[i][0],camions[i][1]
        if x[4] = None : 
            (x2,y2) = (clients[x[5]][0], clients[x[5]][1])
        else : 
            (y2,x2) = (usines[x[4]][0], usines[x[4]][1])
        y = distance(x1,y1,x2,y2)/v
        t+= y
        heapq.heappush(t,i)
    return "finitooooo"