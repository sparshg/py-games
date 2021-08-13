# Physics settings

import pygame as pg
from constants import *

# Physics class
class Physics:

    clock = pg.time.Clock()
    dt = 1 / FPS
    gravity = 1800
    jumpHeight = -750
    friction = 1800
    xAcc = 3600
    maxXVel = 480
