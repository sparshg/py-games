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
from constants import *
from read_level import *
from physics import *

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
        Physics.clock.tick()

    # For key press and close button functionality
    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

    # Update things
    def update(self):
        self.bgEnts.update()
        self.player.update()

    # Draw things
    def render(self):
        self.win.fill(BLACK)
        self.bgEnts.render()
        self.platforms.render()
        self.player.render()
        pg.display.update()

    # The main loop
    def loop(self):
        while self.running:
            self.check_events()
            self.update()
            self.render()
            Physics.dt = Physics.clock.tick(FPS) / 1000
        pg.quit()
        sys.exit()


# The player
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
    def colliding(self):
        for platform in main.platforms.rects:
            if pg.Rect(self.pos.x, self.pos.y, self.width, self.height).colliderect(
                pg.Rect(platform.x, platform.y, platform.w, platform.h)
            ):
                return True
        return False

    # Update player
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
        self.prevPositions.insert(0, pg.Vector2(self.pos.x, self.pos.y))
        if len(self.prevPositions) > self.width / 2:
            self.prevPositions.pop(len(self.prevPositions) - 1)

    # Render player
    def render(self):

        # Render trail
        for i in range(len(self.prevPositions)):
            pg.draw.rect(
                main.win,
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
            main.win,
            RED,
            (
                WIDTH / 2 - self.width / 2,
                HEIGHT / 2 - self.height / 2,
                self.width,
                self.height,
            ),
        )


# Platform class
class Platform:
    def __init__(self, x, y, w, h, type="ground"):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.type = type


# Platforms
class Platforms:
    def __init__(self):
        p = "ground"
        _ = "_"
        self.rects = []
        self.layout = read_level()

        # Convert JSON data to Python list
        for i in range(len(self.layout)):
            for j in range(len(self.layout[i])):
                if self.layout[i][j] == p:
                    self.rects.append(Platform(j * 50, i * 50, 50, 50))

    # Render platforms
    def render(self):
        for rect in self.rects:
            pg.draw.rect(
                main.win,
                DARKPURPLE,
                (
                    rect.x - main.player.pos.x - int(main.player.width / 2) + WIDTH / 2,
                    rect.y
                    - main.player.pos.y
                    - int(main.player.height / 2)
                    + HEIGHT / 2,
                    rect.w,
                    rect.h,
                ),
            )


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
