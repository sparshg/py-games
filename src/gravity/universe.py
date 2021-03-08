from planet import Planet
from constants import *


class Universe:
    def __init__(self):
        self.planets = [
            Planet(100, 10, (WIDTH / 2, HEIGHT / 2), fixed=True),
            Planet(50, 5, (WIDTH / 2 - 400, HEIGHT / 2), (0, -100)),
        ]

    def update(self, dt):
        for planet in self.planets:
            planet.calcUpdate(self.planets)
        for planet in self.planets:
            planet.applyUpdate(dt)

    def render(self, surf):
        for planet in self.planets:
            planet.render(surf)
