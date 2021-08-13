import pygame as pg
from constants import *


class Physics:

    clock = pg.time.Clock()
    dt = 1 / FPS
    gravity = 1800
    jumpHeight = -720
    friction = 1800
    xAcc = 3600
    maxXVel = 480

    def squareCollision(x1, y1, w1, h1, x2, y2, w2, h2):
        return x1 + w1 > x2 and x1 < x2 + w2 and y1 + h1 > y2 and y1 < y2 + h2
