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
        Platforms.init()
        pg.init()
        pg.display.set_caption("Platformer")
        self.running = True
        self.clock = pg.time.Clock()
        self.win = pg.display.set_mode((WIDTH, HEIGHT))

    # For key press detection and closing the window properly
    def checkEvents(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                main.running = False
        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT]: Keys.rtArrow = True
        else: Keys.rtArrow = False
        if keys[pg.K_LEFT]: Keys.ltArrow = True
        else: Keys.ltArrow = False
        if keys[pg.K_UP]: Keys.upArrow = True
        else: Keys.upArrow = False
        if keys[pg.K_DOWN]: Keys.dnArrow = True
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
            self.checkEvents()
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
    gravity = 0.5
    jumpHeight = -12
    friction = 0.5
    acceleration = 1
    maxXVel = 8

    def squareCollision(x1, y1, w1, h1, x2, y2, w2, h2):
        return x1+w1>x2 and x1<x2+w2 and y1+h1>y2 and y1<y2+h2

class Player:
    x = 250
    y = 300
    xVel = 0
    yVel = 0

    def colliding():
        for i in range(len(Platforms.platforms)):
            if Physics.squareCollision(Player.x, Player.y, 50, 50, Platforms.platforms[i].x, Platforms.platforms[i].y, 50, 50):
                return True
        return False

    def update():
        # Gravity
        Player.yVel += Physics.gravity
        Player.y += Player.yVel
        if Player.colliding():
            while Player.colliding():
                if Player.yVel < 0:
                    Player.y += 0.5
                elif Player.yVel > 0:
                    Player.y -= 0.5
            if Keys.upArrow and Player.yVel > 0:
                Player.yVel = Physics.jumpHeight
            else:
                Player.yVel = Physics.gravity

        # Movement

        # Right
        if Keys.rtArrow:
            Player.xVel += Physics.acceleration
            if Player.xVel > Physics.maxXVel:
                Player.xVel = Physics.maxXVel

        # Left
        if Keys.ltArrow:
            Player.xVel -= Physics.acceleration
            if -Player.xVel > Physics.maxXVel:
                Player.xVel = -Physics.maxXVel

        # Apply friction
        if Player.xVel > 0:
            Player.xVel -= Physics.friction
        if Player.xVel < 0:
            Player.xVel += Physics.friction

        # Go back to where you were before if you've hit a wall
        Player.x += Player.xVel
        if Player.colliding():
            Player.x -= Player.xVel
            Player.xVel = 0

    def render():
        pg.draw.rect(main.win, WHITE, (int(Player.x), int(Player.y), 50, 50))

class Platform:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Platforms:
    p = 'p'
    _ = '_'
    tiles = [
        [p, p, p, p, p, p, p, p, p, p, p, p],
        [p, _, _, _, _, _, _, _, _, _, _, p],
        [p, _, _, _, _, p, _, _, _, _, _, p],
        [p, p, p, _, _, p, _, _, _, _, p, p],
        [p, _, _, _, _, _, _, _, _, _, _, p],
        [p, _, p, _, _, _, p, p, p, p, _, p],
        [p, _, _, _, _, _, _, _, _, _, _, p],
        [p, p, p, p, p, p, p, p, p, p, p, p]
    ]
    platforms = []

    def init():
        for i in range(len(Platforms.tiles)):
            for j in range(len(Platforms.tiles[i])):
                if Platforms.tiles[i][j] == Platforms.p:
                    Platforms.platforms.append(Platform(j * 50, i * 50))

    def render():
        for i in range(len(Platforms.platforms)):
            pg.draw.rect(main.win, WHITE, (Platforms.platforms[i].x, Platforms.platforms[i].y, 50, 50))

# Test if the script is directly ran
if __name__ == "__main__":
    main = Main()
    main.loop()
