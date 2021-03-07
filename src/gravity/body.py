import pygame as pg
from constants import *


class Body:
    def __init__(self, mass, radius, pos=(WIDTH / 2, HEIGHT / 2), vel=(0, 0)):
        self.mass = mass
        self.radius = radius
        self.pos = pg.Vector2(pos)
        self.vel = pg.Vector2(vel)

    def calcUpdate(self, bodies):
        self.field = pg.Vector2(0, 0)
        for body in bodies:
            r = body.pos - self.pos
            mag = r.magnitude()
            if mag != 0:
                self.field += G * body.mass * r * mag ** -3

    def applyUpdate(self, dt):
        self.vel += self.field * dt
        self.pos += self.vel * dt

    def render(self, surf):
        pg.draw.circle(surf, WHITE, self.pos, self.radius)