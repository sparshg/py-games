import pygame as pg
from planet import Planet
from constants import *


class Universe:
    def __init__(self):
        self.planets = [
            Planet(10, 10, (WIDTH / 2 - 100, HEIGHT / 2), (0, 50)),
            Planet(10, 10, (WIDTH / 2 + 100, HEIGHT / 2), (0, -50)),
        ]

    def update(self, dt):
        for planet in self.planets:
            planet.calcUpdate(self.planets)
        for planet in self.planets:
            planet.applyUpdate(dt)

    def render(self, surf):
        for planet in self.planets:
            planet.render(surf)
