#!/usr/bin/python
"""
Github repo can be found here:
https://github.com/sparshg/pycollab
"""

import pygame as pg
import sys
from universe import Universe
from planet import Planet
from constants import *


# The main controller
class Main:
    def __init__(self):
        pg.init()
        pg.display.set_caption("gravity")
        self.win = pg.display.set_mode((WIDTH, HEIGHT))
        self.background = pg.Surface((WIDTH, HEIGHT)).convert_alpha()
        self.background.fill((0, 0, 0, 2))
        self.clock = pg.time.Clock()
        self.running = True

        self.universe = Universe()

    # For key press detection and closing the window properly
    def checkEvents(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.universe.planets.append(
                        Planet(10, 3, (WIDTH, HEIGHT), (-100, -100))
                    )

    # Update things
    def update(self, dt):
        self.universe.update(dt)

    # Draw things
    def render(self):
        self.win.blit(self.background, (0, 0))

        self.universe.render(self.win)
        pg.display.update()

    # The main loop
    def loop(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000
            self.checkEvents()
            self.update(dt)
            self.render()
        pg.quit()
        sys.exit()


# Test if the script is directly ran
if __name__ == "__main__":
    main = Main()
    main.loop()
