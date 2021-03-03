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

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                main.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RIGHT: Keys.rtArrow = True
                else: Keys.rtArrow = False
                if event.key == pg.K_LEFT: Keys.ltArrow = True
                else: Keys.ltArrow = False
                if event.key == pg.K_UP: Keys.upArrow = True
                else: Keys.upArrow = False
                if event.key == pg.K_DOWN: Keys.dnArrow = True
                else: Keys.dnArrow = False

    # Update things
    def update(self):
        Player.update()

    # Draw things
    def render(self):
        self.win.fill(BLACK)
        Platforms.render()
        Player.render()
        pg.display.update()

    # The main loop
    def loop(self):
        while self.running:
            self.check_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
        pg.quit()

class Keys:
    rtArrow = False
    ltArrow = False
    upArrow = False
    dnArrow = False

class Physics:
    gravity = 1
    jumpHeight = 18
    friction = 2
    acceleration = 4

    def squareCollision(x1, y1, w1, h1, x2, y2, w2, h2):
        return ((x1 + w1 > x2) and (x1 < x2 + w2)) and (
            (y1 + h1 > y2) and (y1 < y2 + h2)
        )


class Player:
    x = 0
    y = 0
    xVel = 0
    yVel = 0

    def colliding():
        for i in range(len(Platforms.platforms)):
            if Physics.squareCollision(Player.x, Player.y, 50, 50, Platforms.platforms[i].x, Platforms.platforms[i].y, 50, 50):
                return True
        return False

    def update():
        Player.yVel += Physics.gravity
        Player.y += Player.yVel
        if Player.colliding():
            while Player.colliding():
                if Player.yVel < 0:
                    Player.y += 1
                elif Player.yVel > 0:
                    Player.y -= 1
            Player.yVel = 0
        Player.x += Player.xVel
        if Keys.rtArrow: Player.xVel += Physics.acceleration
        if Keys.ltArrow: Player.xVel -= Physics.acceleration

    def render():
        pg.draw.rect(main.win, WHITE, (Player.x, Player.y, 50, 50))

class Platform:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Platforms:
    platforms = [Platform(0, 100), Platform(100, 100), Platform(125, 200)]

    def render():
        for i in range(len(Platforms.platforms)):
            pg.draw.rect(main.win, WHITE, (Platforms.platforms[i].x, Platforms.platforms[i].y, 50, 50))

# Test if the script is directly ran
if __name__ == "__main__":
    main = Main()
    main.loop()
