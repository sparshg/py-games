import pygame as pg
from body import Body


class Universe:
    def __init__(self):
        self.bodies = [Body(10, 10), Body(2, 10, (300, 0))]

    def update(self, dt):
        for body in self.bodies:
            body.calcUpdate(self.bodies)
        for body in self.bodies:
            body.applyUpdate(dt)

    def render(self, surf):
        for body in self.bodies:
            body.render(surf)
