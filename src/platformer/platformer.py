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
WHITE = (255, 255, 255)

# The main controller
class Main:
    def __init__(self):
        pg.init()
        pg.display.set_caption("Platformer")
        self.running = True
        self.clock = pg.time.Clock()
        self.win = pg.display.set_mode((WIDTH, HEIGHT))

        self.player = Player()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                main.running = False

    # Update things
    def update(self):
        self.player.update()

    # Draw things
    def render(self):
        self.win.fill(BLACK)
        platforms.render()
        self.player.render()
        pg.display.update()

    # The main loop
    def loop(self):
        while self.running:
            self.check_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
        pg.quit()


class Physics:

    gravity = 2
    jumpHeight = 18
    friction = 2
    acceleration = 4

    @staticmethod
    def squareCollision(x1, y1, w1, h1, x2, y2, w2, h2):
        return ((x1 + w1 > x2) and (x1 < x2 + w2)) and (
            (y1 + h1 > y2) and (y1 < y2 + h2)
        )


class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.xVel = 0
        self.yVel = 0

    def colliding(self):
        return False

    def update(self):
        self.yVel += Physics.gravity
        self.y += self.yVel
        if self.colliding():
            while self.colliding():
                if self.yVel < 0:
                    pass
                elif self.yVel > 0:
                    pass
            self.yVel = 0

    def render(self):
        pg.draw.rect(main.win, WHITE, (self.x, self.y, 50, 50))


class Platforms:
    def __init__(self):
        self.platforms = []

    def render(self):
        for i in range(len(self.platforms)):
            pg.draw.rect(
                main.win, WHITE, (self.platforms[i].x, self.platforms[i].y, 75, 75)
            )


platforms = Platforms()

# Test if the script is directly ran
if __name__ == "__main__":
    main = Main()
    main.loop()
