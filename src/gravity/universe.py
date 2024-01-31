import pygame as pg
from planet import Planet
from constants import *
from random import randrange


class Universe:
    def __init__(self):
        self.planets = []
        for i in range(randrange(2, 8)):
            radius = randrange(2, 28)
            self.planets.append(
                Planet(
                    radius * 10000000,
                    radius,
                    pg.Vector2(randrange(radius, WIDTH - radius), randrange(radius, HEIGHT - radius)),
                    #pg.Vector2(randrange(-2000, 2000), randrange(-2000, 2000))
                    pg.math.Vector2(0),
                    pg.Color(randrange(0 , 255), randrange(0 , 255), randrange(0 , 255))
                )
            )

    def update(self, dt):
        for planet in self.planets:
            planet.calcUpdate(self.planets)
        for planet in self.planets:
            planet.applyUpdate(dt)

    def render(self, surf):
        for planet in self.planets:
            planet.render(surf)
