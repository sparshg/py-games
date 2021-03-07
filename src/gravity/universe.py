import pygame as pg
from body import Body
from constants import *


class Universe:
    def __init__(self):
        self.bodies = [
            Body(10, 10, (WIDTH / 2 - 100, HEIGHT / 2), (0, 50)),
            Body(10, 10, (WIDTH / 2 + 100, HEIGHT / 2), (0, -50)),
        ]

    def update(self, dt):
        for body in self.bodies:
            body.calcUpdate(self.bodies)
        for body in self.bodies:
            body.applyUpdate(dt)

    def render(self, surf):
        for body in self.bodies:
            body.render(surf)
