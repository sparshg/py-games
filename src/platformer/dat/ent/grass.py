import pygame as pg
from colors import *

def update(entity, display):
    pg.draw.rect(display, GREEN, (entity.pos.x, entity.pos.y, entity.dim.x, entity.dim.y))
