# Scrolling mechanism

import pygame as pg
from main import scrollX, scrollY, scrollVel


def get_scroll_pos():
    global scrollX, scrollY, scrollVel
    keys = pg.key.get_pressed()
    if keys[pg.K_UP]:
        scrollY -= scrollVel
    if keys[pg.K_DOWN]:
        scrollY += scrollVel
    if keys[pg.K_RIGHT]:
        scrollX += scrollVel
    if keys[pg.K_LEFT]:
        scrollX -= scrollVel
    return (scrollX, scrollY)
