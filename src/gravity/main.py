#!/usr/bin/python
"""
Github repo can be found here:
https://github.com/sparshg/py-games
"""

import pygame as pg
import sys
from universe import Universe
from constants import *


# The main controller
class Main:
    def __init__(self):
        pg.init()
        pg.display.set_caption("gravity")
        self.win = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.running = True
        self.universe = Universe()

    # Key press and close button functionality
    def checkEvents(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

    # Update things
    def update(self, dt):
        self.universe.update(dt)

    # Draw things
    def render(self):
        self.win.fill(BLACK)
        self.universe.render(self.win)
        pg.display.update()

    # The main loop
    def loop(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000
            self.checkEvents()
            self.update(dt)
            self.render()

            for event in pg.event.get():
                  if (event.type ==pg.KEYDOWN):
                    if event.key == pg.K_SPACE:
                        self.universe.add()

        pg.quit()
        sys.exit()


# Test if the script is directly ran
if __name__ == "__main__":
    main = Main()
    main.loop()
