import pygame as pg

class Physics:
    def __init__(self):
        self.gravity = 0.008
    def checkcol_square_square(self, pos1, dim1, pos2, dim2):
        if pg.Rect(pos1.x, pos1.y, dim1.x, dim1.y).colliderect(pos2.x, pos2.y, dim2.x, dim2.y):
            return True

physics = Physics()
