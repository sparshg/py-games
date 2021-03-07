#!/usr/bin/python
"""
Github repo can be found here:
https://github.com/sparshg/pycollab
"""

import pygame as pg
import sys, math, random

# Declare some constants and variables
WIDTH, HEIGHT = (1248, 702)
FPS = 60
BLACK = (0, 0, 0)
GREY = (255/2, 255/2, 255/2)
WHITE = (255, 255, 255)
YELLOW = (255, 200, 0)

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
        self.goal = Goal(400, 475, 25)

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
        self.goal.render()
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
        self.planets = [Planet(50, 150, 5), Planet(225, 300, 20), Planet(400, 75, 50)]

    def render(self):
        for i in range(len(self.planets)):
            pg.draw.circle(main.win, WHITE, (self.planets[i].x, self.planets[i].y), self.planets[i].size)


class Player:
    def __init__(self):
        self.x = 50
        self.y = 50
        self.xVel = 0
        self.yVel = 0

    def update(self):
        # Controls
        keyDown = pg.key.get_pressed()
        if keyDown[pg.K_RIGHT]:
            main.player.xVel += Physics.controlPower
        if keyDown[pg.K_LEFT]:
            main.player.xVel -= Physics.controlPower
        if keyDown[pg.K_UP]:
            main.player.yVel -= Physics.controlPower
        if keyDown[pg.K_DOWN]:
            main.player.yVel += Physics.controlPower

        # Gravity
        for i in range(len(main.planets.planets)):
            # Direction = atan2(destination y - y, destination x - x)
            # That finds the direction if you're trying to point somewhere (which is (in this case) "main.planets.planets[i]")
            dir = math.atan2(main.planets.planets[i].y - self.y, main.planets.planets[i].x - self.x)
            # Distance = hypot(x1 - x2, y1 - y2)
            # Finds the dist between 2 points (multiplied by Physics.gravity to adjust the vel)
            dist = math.hypot(self.x - main.planets.planets[i].x, self.y - main.planets.planets[i].y)

            self.xVel += math.cos(dir) * main.planets.planets[i].size / (dist * Physics.gravity)
            self.yVel += math.sin(dir) * main.planets.planets[i].size / (dist * Physics.gravity)

            # Bounce if touching planet
            if dist < main.planets.planets[i].size + 25:
                self.xVel *= -1
                self.yVel *= -1

            self.x += self.xVel * main.dt
            self.y += self.yVel * main.dt

        # Bounce if on edge
        if self.x - 25 < 0 or self.x + 25 > WIDTH:
            self.xVel *= -1
        if self.y - 25 < 0 or self.y + 25 > HEIGHT:
            self.yVel *= -1

    def render(self):
        pg.draw.circle(main.win, GREY, (self.x, self.y), 25)


class Physics:
    gravity = 0.5
    # How much planets attract the player (the bigger, the more they do)
    controlPower = 0.1
    # How powerful the controls of the player are


class Goal:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.particles = []

    def render(self):
        pg.draw.circle(main.win, YELLOW, (self.x, self.y), self.size)
        for i in range(len(self.particles)):
            self.particles[i].render()


    def confetti(self):
        for i in range(math.random() * 20):
            self.particles.append(Particle(main.goal.x, main.goal.y, random.randint(5, 10), math.random(0, 6.28318531)))


class Particle:
    def __init__(self, x, y, xVel, yVel, dir):
        self.x = x
        self.y = y
        self.xVel = xVel
        self.yVel = yVel
        self.dir = dir

    def update(self):
        pass

    def render(self):
        pg.draw.circle(main.win, YELLOW, (self.x, self.y), main.goal.size / 4)


# Test if the script is directly ran
if __name__ == "__main__":
    main = Main()
    main.loop()
