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
import sys, random

import physics
from constants import *
from player import Player
from platforms import Platforms

# The main controller
class Main:
    def __init__(self):
        pg.init()
        pg.display.set_caption("Platformer")

        self.running = True
        self.win = pg.display.set_mode((WIDTH, HEIGHT))
        self.platforms = Platforms()
        self.player = Player()
        self.bgEnts = BgEnts()
        self.clock = pg.time.Clock()
        self.clock.tick()

    # For key press and close button functionality
    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

    # Update things
    def update(self):
        self.bgEnts.update()
        self.player.update(self.platforms.rects)

    # Draw things
    def render(self):
        self.win.fill(BLACK)
        self.bgEnts.render()
        self.platforms.render(self.win, self.player)
        self.player.render(self.win)
        pg.display.update()

    # The main loop
    def loop(self):
        while self.running:
            self.check_events()
            self.update()
            self.render()
            physics.dt = self.clock.tick(FPS) / 1000
        pg.quit()
        sys.exit()


# Background objects
class BgEnts:
    def __init__(self):
        self.waves = self.Waves()

    # Update scene
    def update(self):
        self.waves.gen_waves()
        self.waves.update()

    # Draw scene
    def render(self):
        self.waves.render()

    class Waves:
        def __init__(self):
            # Bigger num = less waves
            # Smaller num = more waves
            self.waveGenRate = 75
            # Bigger num = less thickness
            # Smaller num = more thickness
            self.waveThickness = 4

            # Min/max wave size
            self.minWaveSize = 10
            self.maxWaveSize = 35

            # Min/max wave max life
            self.minWaveLife = 25
            self.maxWaveLife = 125

            # Min/max wave speed
            self.minWaveSpeed = 10
            self.maxWaveSpeed = 35

            self.waves = []

        # Wave class
        class Wave:
            def __init__(self, x, y, life, speed):
                self.x = x
                self.y = y
                self.life = life
                self.speed = speed
                self.frame = 0

        # Generate waves randomly
        def gen_waves(self):
            if random.randint(0, self.waveGenRate) == self.waveGenRate:
                self.waves.append(
                    self.Wave(
                        random.randint(0, WIDTH),
                        random.randint(0, HEIGHT),
                        random.randint(self.minWaveLife, self.maxWaveLife),
                        random.randint(self.minWaveSpeed, self.maxWaveSpeed),
                    )
                )

        # Update waves
        def update(self):
            for i in range(len(self.waves)):
                if self.waves[i].frame >= self.waves[i].life:
                    self.waves[i] = None
                else:
                    self.waves[i].frame += 1
            # Remove empty list items
            self.waves = list(filter(lambda item: item != None, self.waves))

        # Render waves
        def render(self):
            for i in range(len(self.waves)):
                # Use surface since pg.draw.circle doesn't support transparency
                surf = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA, 32)
                pg.draw.circle(
                    surf,
                    (
                        # Convert hex code to RGB tuple then add allpha channel
                        tuple(int(PURPLE.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))
                        # Alpha channel, set according to frame of wave
                        + (255 - 255 / self.waves[i].life * self.waves[i].frame,)
                    ),
                    (self.waves[i].x, self.waves[i].y),
                    self.waves[i].frame,
                    int(self.waves[i].frame / self.waveThickness),
                )
                main.win.blit(surf, (0, 0))


# Test if the script is directly ran
if __name__ == "__main__":
    main = Main()
    main.loop()
