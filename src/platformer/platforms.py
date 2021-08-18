import pygame as pg
from read_level import *
from constants import *


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
    def render(self, win, player):
        for rect in self.rects:
            pg.draw.rect(
                win,
                DARKPURPLE,
                (
                    rect.x - player.pos.x - int(player.width / 2) + WIDTH / 2,
                    rect.y - player.pos.y - int(player.height / 2) + HEIGHT / 2,
                    rect.w,
                    rect.h,
                ),
            )
