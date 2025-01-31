import numpy as np
import pandas as pd

clients = pd.read_csv('C:/Users/Ilias/OneDrive/Desktop/MINES 1A/info/hackathon 2/Hackathon/clients.csv')
usines = pd.read_csv('C:/Users/Ilias/OneDrive/Desktop/MINES 1A/info/hackathon 2/Hackathon/plants.csv')

clients["statut"] = 1