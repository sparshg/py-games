import pygame as pg
import physics
from constants import *


class Player:
    def __init__(self):
        self.pos = pg.Vector2(250, 300)
        self.vel = pg.Vector2(0, 0)
        self.onGround = True
        self.prevPositions = []
        self.width = 40
        self.height = 40
        self.trailPower = 2

    # Check col with ground
    def colliding(self, rects):
        for platform in rects:
            if pg.Rect(self.pos.x, self.pos.y, self.width, self.height).colliderect(
                pg.Rect(platform.x, platform.y, platform.w, platform.h)
            ):
                return True
        return False

    # Update player
    def update(self, plats):

        # Get keys
        keyDown = pg.key.get_pressed()

        if self.onGround:
            if keyDown[pg.K_UP]:
                self.vel.y = physics.jumpHeight
                self.onGround = False
            if not self.colliding(plats):
                self.onGround = False
        else:
            self.vel.y += physics.gravity * physics.dt
            self.pos.y += self.vel.y * physics.dt

            if self.colliding(plats):
                if self.vel.y > 0:
                    while self.colliding(plats):
                        self.pos.y -= 0.5
                    self.vel.y = 0
                    self.onGround = True
                else:
                    while self.colliding(plats):
                        self.pos.y += 0.5
                    self.vel.y = physics.gravity * physics.dt

        # Right
        if keyDown[pg.K_RIGHT]:
            self.vel.x += physics.xAcc * physics.dt
            if self.vel.x > physics.maxXVel:
                self.vel.x = physics.maxXVel

        # Left
        if keyDown[pg.K_LEFT]:
            self.vel.x -= physics.xAcc * physics.dt
            if -self.vel.x > physics.maxXVel:
                self.vel.x = -physics.maxXVel

        # Apply friction
        if self.vel.x < 0:
            self.vel.x += physics.friction * physics.dt
            if self.vel.x > 0:
                self.vel.x = 0
        elif self.vel.x > 0:
            self.vel.x -= physics.friction * physics.dt
            if self.vel.x < 0:
                self.vel.x = 0

        # Wall collision
        self.pos.x += self.vel.x * physics.dt
        if self.colliding(plats):
            while self.colliding(plats):
                if self.vel.x > 0:
                    self.pos.x -= 0.5
                else:
                    self.pos.x += 0.5
            self.vel.x = 0

        # Trail
        self.prevPositions.insert(0, pg.Vector2(self.pos.x, self.pos.y))
        if len(self.prevPositions) > self.width / 2:
            self.prevPositions.pop(len(self.prevPositions) - 1)

    # Render player
    def render(self, win):

        # Render trail
        for i in range(len(self.prevPositions)):
            pg.draw.rect(
                win,
                ORANGE,
                (
                    WIDTH / 2
                    - self.width / 4
                    - self.pos.x
                    + self.prevPositions[i].x
                    + i * self.trailPower / 2,
                    HEIGHT / 2
                    - self.height / 4
                    - self.pos.y
                    + self.prevPositions[i].y
                    + i * self.trailPower / 2,
                    self.width / 2 - i * self.trailPower,
                    self.height / 2 - i * self.trailPower,
                ),
            )

        # Render player
        pg.draw.rect(
            win,
            RED,
            (
                WIDTH / 2 - self.width / 2,
                HEIGHT / 2 - self.height / 2,
                self.width,
                self.height,
            ),
        )
