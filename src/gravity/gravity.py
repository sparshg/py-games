#!/usr/bin/python
"""
Github repo can be found here:
https://github.com/sparshg/pycollab
"""

import pygame as pg
import sys

# Declare some constants and variables
WIDTH, HEIGHT = (1248, 702)
FPS = 60
BLACK = "#000000"

# The main controller
class Main:
    def __init__(self):
        pg.init()
        pg.display.set_caption("gravity")
        self.win = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.running = True

    # For key press detection and closing the window properly
    def checkEvents(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

    # Update things
    def update(self):
        pass

    # Draw things
    def render(self):
        self.win.fill(BLACK)
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


# Test if the script is directly ran
if __name__ == "__main__":
    main = Main()
    main.loop()
