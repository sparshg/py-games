#!/usr/bin/python
"""
Github repo can be found here:
https://github.com/sparshg/pycollab
"""

import pygame as pg
import sys, math

# Declare some constants and variables
WIDTH, HEIGHT = (1248, 702)
FPS = 60
BLACK = (0, 0, 0)
GREY = (255/2, 255/2, 255/2)
WHITE = (255, 255, 255)

# The main controller
class Main:
    def __init__(self):
        pg.init()
        pg.display.set_caption("Gravity")
        self.win = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.running = True

        self.planets = Planets()
        self.player = Player()

    # For key press detection and closing the window properly
    def checkEvents(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

    # Update things
    def update(self):
        self.player.update()

    # Draw things
    def render(self):
        self.win.fill(BLACK)
        self.planets.render()
        self.player.render()
        pg.display.update()

    # The main loop
    def loop(self):
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000
            self.checkEvents()
            self.update()
            self.render()
        pg.quit()
        sys.exit()


class Planet:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size


class Planets:
    def __init__(self):
        self.planets = [Planet(50, 50, 40)]

    def render(self):
        for i in range(len(self.planets)):
            pg.draw.circle(main.win, WHITE, (self.planets[i].x+self.planets[i].size, self.planets[i].y+self.planets[i].size), self.planets[i].size)


class Player:
    def __init__(self):
        self.x = 1
        self.y = 1
        self.xVel = 0
        self.yVel = 0

    def update(self):
        for i in range(len(main.planets.planets)):
            self.xVel += math.hypot(self.x - main.planets.planets[i].x, self.y - main.planets.planets[i].y) / 10 * main.planets.planets[i].size
            self.yVel += math.hypot(self.x - main.planets.planets[i].x, self.y - main.planets.planets[i].y) / 10 * main.planets.planets[i].size
        self.x += self.xVel * main.dt
        self.y += self.yVel * main.dt

    def render(self):
        pg.draw.circle(main.win, GREY, (self.x+25, self.y+25), 25)


# Test if the script is directly ran
if __name__ == "__main__":
    main = Main()
    main.loop()
