import pygame as pg
from planet import Planet
from constants import *
from random import randrange


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

    def add(self):
        print('add new planet!')
        randomMass = randrange(100)
        randomRadius = randrange(50)
        randomPosX = randrange(WIDTH)
        randomPosY = randrange(HEIGHT)
        randomVelocity = randrange(100)
        newPlanet = Planet(randomMass, randomRadius, (randomPosX, randomPosY), (0, randomVelocity))
        self.planets.append(newPlanet)

    def render(self, surf):
        for planet in self.planets:
            planet.render(surf)
