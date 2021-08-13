#!/usr/bin/python
"""
Github repo can be found here:
https://github.com/sparshg/py-games
"""

# Import statements
from os import environ

# Hide pygame Hello prompt
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame as pg

import sys
from constants import *
from physics import Physics

# The main controller
class Main:
    def __init__(self):
        pg.init()
        pg.display.set_caption("Platformer")
        self.running = True
        self.win = pg.display.set_mode((WIDTH, HEIGHT))
        self.platforms = Platforms()
        self.player = Player()
        Physics.clock.tick()

    # For key press and close button functionality
    def checkEvents(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                main.running = False

    # Update things
    def update(self):
        self.player.update()

    # Draw things
    def render(self):
        self.win.fill(BLACK)
        self.platforms.render()
        self.player.render()
        pg.display.update()

    # The main loop
    def loop(self):
        while self.running:
            self.checkEvents()
            self.update()
            self.render()
            Physics.dt = Physics.clock.tick(FPS) / 1000
        pg.quit()
        sys.exit()


class Player:
    def __init__(self):
        self.pos = pg.Vector2(250, 300)
        self.vel = pg.Vector2(0, 0)
        self.onGround = True
        self.prevPositions = []
        self.width = 40
        self.height = 40

    def colliding(self):
        for platform in main.platforms.rects:
            if pg.Rect(self.pos.x, self.pos.y, self.width, self.height).colliderect(platform):
                return True
        return False

    def update(self):

        # Get keys
        keyDown = pg.key.get_pressed()

        if self.onGround:
            if keyDown[pg.K_UP]:
                self.vel.y = Physics.jumpHeight
                self.onGround = False
            if not self.colliding():
                self.onGround = False
        else:
            self.vel.y += Physics.gravity * Physics.dt
            self.pos.y += self.vel.y * Physics.dt

            if self.colliding():
                if self.vel.y > 0:
                    while self.colliding():
                        self.pos.y -= 0.5
                    self.vel.y = 0
                    self.onGround = True
                else:
                    while self.colliding():
                        self.pos.y += 0.5
                    self.vel.y = Physics.gravity * Physics.dt

        # Right
        if keyDown[pg.K_RIGHT]:
            self.vel.x += Physics.xAcc * Physics.dt
            if self.vel.x > Physics.maxXVel:
                self.vel.x = Physics.maxXVel

        # Left
        if keyDown[pg.K_LEFT]:
            self.vel.x -= Physics.xAcc * Physics.dt
            if -self.vel.x > Physics.maxXVel:
                self.vel.x = -Physics.maxXVel

        # Apply friction
        # If friction starts moving block in opposite direction instead of stopping, set vel to 0
        if self.vel.x < 0:
            self.vel.x += Physics.friction * Physics.dt
            if self.vel.x > 0:
                self.vel.x = 0
        elif self.vel.x > 0:
            self.vel.x -= Physics.friction * Physics.dt
            if self.vel.x < 0:
                self.vel.x = 0

        # Wall collision
        self.pos.x += self.vel.x * Physics.dt
        if self.colliding():
            while self.colliding():
                if self.vel.x > 0:
                    self.pos.x -= 0.5
                else:
                    self.pos.x += 0.5
            self.vel.x = 0

        # Trail
        self.prevPositions.append(pg.Vector2(self.pos.x, self.pos.y))
        if len(self.prevPositions) > self.width/2:
            self.prevPositions.pop(0)

    def render(self):

        # Ren trail
        for i in range(len(self.prevPositions)):
            pg.draw.rect(main.win, ORANGE, (
                self.prevPositions[len(self.prevPositions) - i - 1].x - (self.width-i*2)/2 + self.width/2,
                self.prevPositions[len(self.prevPositions) - i - 1].y - (self.height-i*2)/2 + self.height/2,
                self.width - i*2,
                self.height - i*2
            ))

        # Ren player
        pg.draw.rect(main.win, RED, (self.pos.x, self.pos.y, self.width, self.height))


class Platform:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Platforms:
    def __init__(self):
        p = "p"
        _ = "_"
        self.rects = []
        self.layout = [
            [p, p, p, p, p, p, p, p, p, p, p, p],
            [p, _, _, _, _, _, _, _, _, _, _, p],
            [p, _, _, _, _, _, _, _, _, _, _, p],
            [p, p, p, _, _, p, _, _, _, _, p, p],
            [p, _, _, _, _, _, _, _, _, _, _, p],
            [p, _, p, _, _, _, p, p, p, p, _, p],
            [p, _, _, _, _, _, _, _, _, _, _, p],
            [p, p, p, p, p, p, p, p, p, p, p, p],
        ]
        for i in range(len(self.layout)):
            for j in range(len(self.layout[i])):
                if self.layout[i][j] == p:
                    self.rects.append(pg.Rect(j * 50, i * 50, 50, 50))

    def render(self):
        for rect in self.rects:
            pg.draw.rect(main.win, WHITE, rect)


# Test if the script is directly ran
if __name__ == "__main__":
    main = Main()
    main.loop()
