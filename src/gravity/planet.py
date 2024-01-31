import pygame as pg
from constants import *
import math

class Planet:
    def __init__(self, mass, radius, pos, vel=(0, 0), color=WHITE):
        self.mass = mass
        self.radius = radius
        self.pos = pg.Vector2(pos)
        self.vel = pg.Vector2(vel)
        self.color = color

    def handleCollisionElastic(self, target):
        elasticity = 1
        distance = self.pos.distance_to(target.pos)

        if distance <= (self.radius + target.radius):
            normal = (target.pos - self.pos).normalize()
            relative_velocity = target.vel - self.vel
            relative_velocity_along_normal = relative_velocity.dot(normal)

            if relative_velocity_along_normal < 0:
                impulse_scalar = -(1 + elasticity) * relative_velocity_along_normal / (1 / self.mass + 1 / target.mass)

                self.vel -= impulse_scalar / self.mass * normal
                target.vel += impulse_scalar / target.mass * normal

                overlap = (self.radius + target.radius) - distance
                self.pos -= overlap / 2 * normal
                target.pos += overlap / 2 * normal

    def calcUpdate(self, planets):
        net_acc = pg.math.Vector2(0, 0)

        for planet in planets:
            if planet != self:
                self.handleCollisionElastic(planet)
                diff = planet.pos - self.pos
                net_acc += diff.normalize() * (G * self.mass * planet.mass / diff.length_squared())

        self.vel += net_acc

    def applyUpdate(self, dt):
        self.pos += self.vel * TIME_MULTIPLIER * dt

    def render(self, surf):
        pg.draw.circle(surf, self.color, self.pos, self.radius)

