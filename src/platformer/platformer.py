#!/usr/bin/python
"""
Github repo can be found here:
https://github.com/sparshg/pycollab
"""

# Import statements
from os import environ

# Hide pygame Hello prompt
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame as pg

# Declare some constants and variables
WIDTH, HEIGHT = (600, 400)
FPS = 60
BLACK = (0, 0, 0)
GREY = (225 / 2, 225 / 2, 225 / 2)
WHITE = (255, 255, 255)

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

    # For key press detection and closing the window properly
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


class Physics:

    clock = pg.time.Clock()
    dt = 1 / FPS
    gravity = 1800
    jumpHeight = -720
    friction = 1800
    xAcc = 3600
    maxXVel = 480

    def squareCollision(x1, y1, w1, h1, x2, y2, w2, h2):
        return x1 + w1 > x2 and x1 < x2 + w2 and y1 + h1 > y2 and y1 < y2 + h2


class Player:
    def __init__(self):
        self.pos = pg.Vector2(250, 300)
        self.vel = pg.Vector2(0, 0)
        self.onGround = True

    def colliding(self):
        for platform in main.platforms.rects:
            if pg.Rect(self.pos.x, self.pos.y, 50, 50).colliderect(platform):
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

    def render(self):
        pg.draw.rect(main.win, GREY, (self.pos.x, self.pos.y, 50, 50))


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
