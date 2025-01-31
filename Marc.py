import numpy as np
import pygame as pg

pg.init()
clock = pg.time.Clock()
running = True
while running:
    clock.tick(10)

def distance(x1, y1, x2, y2):
    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
