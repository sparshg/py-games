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
GREY = (225/2, 225/2, 225/2)
WHITE = (255, 255, 255)

# The main controller
class Main:
    def __init__(self):
        self.platforms = Platforms()
        self.player = Player()
        self.keys = Keys()
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
        keyDown = pg.key.get_pressed()
        if keyDown[pg.K_RIGHT]: self.keys.rtArrow = True
        else: self.keys.rtArrow = False
        if keyDown[pg.K_LEFT]: self.keys.ltArrow = True
        else: self.keys.ltArrow = False
        if keyDown[pg.K_UP]: self.keys.upArrow = True
        else: self.keys.upArrow = False
        if keyDown[pg.K_DOWN]: self.keys.dnArrow = True
        else: self.keys.dnArrow = False

    # Update things
    def update(self):
        self.player.update()

    # Draw things
    def render(self):
        self.win.fill(BLACK)
        self.platforms.render()
        self.player.render()
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
    def __init__(self):
        self.rtArrow = False
        self.ltArrow = False
        self.upArrow = False
        self.dnArrow = False

class Physics:
    gravity = 0.5
    jumpHeight = -12
    friction = 0.5
    acceleration = 1
    maxXVel = 8

    def squareCollision(x1, y1, w1, h1, x2, y2, w2, h2):
        return x1+w1>x2 and x1<x2+w2 and y1+h1>y2 and y1<y2+h2

class Player:
    def __init__(self):
        self.x = 250
        self.y = 300
        self.xVel = 0
        self.yVel = 0

    def colliding(self):
        for i in range(len(Platforms.platforms)):
            if Physics.squareCollision(main.player.x, main.player.y, 50, 50, main.platforms.platforms[i].x, main.platforms.platforms[i].y, 50, 50):
                return True
        return False

    def update(self):
        # Gravity
        main.player.yVel += Physics.gravity
        main.player.y += main.player.yVel
        if main.player.colliding():
            while main.player.colliding():
                if main.player.yVel < 0:
                    main.player.y += 0.5
                elif main.player.yVel > 0:
                    main.player.y -= 0.5
            if main.keys.upArrow and main.player.yVel > 0:
                main.player.yVel = Physics.jumpHeight
            else:
                main.player.yVel = Physics.gravity

        # Movement
        # Right
        if main.keys.rtArrow:
            main.player.xVel += Physics.acceleration
            if main.player.xVel > Physics.maxXVel:
                main.player.xVel = Physics.maxXVel

        # Left
        if main.keys.ltArrow:
            main.player.xVel -= Physics.acceleration
            if -main.player.xVel > Physics.maxXVel:
                main.player.xVel = -Physics.maxXVel

        # Apply friction
        if main.player.xVel > 0:
            main.player.xVel -= Physics.friction
        if main.player.xVel < 0:
            main.player.xVel += Physics.friction

        # Go back to where you were before if you've hit a wall
        main.player.x += main.player.xVel
        if main.player.colliding():
            main.player.x -= main.player.xVel
            main.player.xVel = 0

    def render(self):
        pg.draw.rect(main.win, GREY, (int(main.player.x), int(main.player.y), 50, 50))

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
        [p, _, _, _, _, _, _, _, _, _, _, p],
        [p, p, p, _, _, p, _, _, _, _, p, p],
        [p, _, _, _, _, _, _, _, _, _, _, p],
        [p, _, p, _, _, _, p, p, p, p, _, p],
        [p, _, _, _, _, _, _, _, _, _, _, p],
        [p, p, p, p, p, p, p, p, p, p, p, p]
    ]
    platforms = []

    def __init__(self):
        for i in range(len(Platforms.tiles)):
            for j in range(len(Platforms.tiles[i])):
                if Platforms.tiles[i][j] == Platforms.p:
                    Platforms.platforms.append(Platform(j * 50, i * 50))

    def render(self):
        for i in range(len(Platforms.platforms)):
            pg.draw.rect(main.win, WHITE, (Platforms.platforms[i].x, Platforms.platforms[i].y, 50, 50))

# Test if the script is directly ran
if __name__ == "__main__":
    main = Main()
    main.loop()
