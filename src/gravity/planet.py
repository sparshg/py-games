import pygame as pg
from constants import *


class Planet:
    def __init__(
        self, mass, radius, pos=(WIDTH / 2, HEIGHT / 2), vel=(0, 0), fixed=False
    ):
        self.mass = mass
        self.radius = radius
        self.fixed = fixed
        self.pos = pg.Vector2(pos)
        self.vel = pg.Vector2(vel)

    def calcUpdate(self, planets):
        if not self.fixed:
            self.field = pg.Vector2(0, 0)
            for planet in planets:
                r = planet.pos - self.pos
                mag = r.magnitude()
                if mag != 0:
                    if mag < self.radius + planet.radius:
                        mag = self.radius + planet.radius
                    self.field += G * planet.mass * r * mag ** -3

    def applyUpdate(self, dt):
        if not self.fixed:
            self.vel += self.field * dt
            self.pos += self.vel * dt

    def render(self, surf):
        pg.draw.circle(surf, WHITE, self.pos, self.radius)