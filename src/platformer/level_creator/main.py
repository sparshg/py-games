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

import sys
from constants import *
from file_editor import *
from scrolling import *

mouseDown = False
scrollX = 0
scrollY = 0
scrollVel = 1
blockSize = 50

# The main controller
class Main:
    def __init__(self):
        pg.init()
        pg.display.set_caption("Platformer Level Creator")
        self.running = True
        self.win = pg.display.set_mode((WIDTH, HEIGHT))
        self.menuBar = MenuBar()
        self.selectedBlock = SelectedBlock()
        self.platforms = Platforms()

    # For key press and close button functionality
    def check_events(self):
        global mouseDown
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.MOUSEBUTTONUP:
                mouseDown = True

    # Update things
    def update(self):
        global scrollX, scrollY
        self.menuBar.update()
        self.selectedBlock.update()
        scrollX = get_scroll_pos()[0]
        scrollY = get_scroll_pos()[1]
        keys = pg.key.get_pressed()
        # Save on CTRL + S
        if keys[pg.K_s] and (keys[pg.K_LCTRL] or keys[pg.K_RCTRL]):
            write_level(main.platforms.platforms)

    # Draw things
    def render(self):
        self.win.fill(BLACK)
        self.platforms.render()
        self.menuBar.render()
        self.selectedBlock.render()
        pg.display.update()

    # The main loop
    def loop(self):
        global mouseDown
        while self.running:
            self.check_events()
            self.update()
            self.render()
            mouseDown = False
        pg.quit()
        sys.exit()


# Menu bar buttons
class MenuButton:
    def __init__(self, renFun, side, id):
        self.renFun = renFun
        self.side = side
        self.id = id


# Button 1 (ground)
def ren_btn1(x, y):
    pg.draw.rect(
        main.win,
        DARKPURPLE,
        (
            x + main.menuBar.height / 4,
            y + main.menuBar.height / 4,
            main.menuBar.height / 2,
            main.menuBar.height / 2,
        ),
    )


btn1 = MenuButton(ren_btn1, "lt", "ground")


# Button 2 (air/clear)
def ren_btn2(x, y):
    # Draw red X
    pg.draw.line(
        main.win,
        RED,
        (x + main.menuBar.height / 4, y + main.menuBar.height / 4),
        (
            x + main.menuBar.height - main.menuBar.height / 4,
            y + main.menuBar.height - main.menuBar.height / 4,
        ),
        10,
    )
    pg.draw.line(
        main.win,
        RED,
        (
            x + main.menuBar.height - main.menuBar.height / 4,
            y + main.menuBar.height / 4,
        ),
        (
            x + main.menuBar.height / 4,
            y + main.menuBar.height - main.menuBar.height / 4,
        ),
        10,
    )


btn2 = MenuButton(ren_btn2, "lt", None)


# Button 3 (the save button)
def ren_btn3(x, y):
    font = pg.font.SysFont("Segoe UI", 25)
    surf = font.render("Save", 1, BLACK)
    main.win.blit(
        surf,
        (
            x + main.menuBar.height / 2 - font.size("Save")[0] / 2,
            y + main.menuBar.height / 2 - font.size("Save")[1] / 2,
        ),
    )


btn3 = MenuButton(ren_btn3, "rt", "SAVE")


# Menu bar
class MenuBar:
    def __init__(self):
        global scrollY
        self.width = WIDTH
        self.height = 75

        self.buttonClicked = None
        self.buttons = [btn1, btn2, btn3]

    # Update bar
    def update(self):
        if self.buttonClicked != None:
            main.selectedBlock.quit_selection()
            main.selectedBlock.select_block(self.buttons[self.buttonClicked].id)
            self.buttonClicked = None

    # Draw bar
    def render(self):
        # Current X
        ltX = 0
        rtX = self.width - self.height
        # Background
        pg.draw.rect(main.win, LIGHTGRAY, (0, 0, self.width, self.height))
        # Buttons
        for i in range(len(self.buttons)):
            # If on right side
            if self.buttons[i].side == "lt":
                if pg.Rect(ltX, 0, self.height, self.height).collidepoint(
                    pg.mouse.get_pos()
                ):
                    if pg.mouse.get_pressed()[0]:
                        pg.draw.rect(
                            main.win, DARKGRAY, (ltX, 0, self.height, self.height)
                        )
                    else:
                        pg.draw.rect(main.win, GRAY, (ltX, 0, self.height, self.height))
                    if mouseDown:
                        self.buttonClicked = i
                self.buttons[i].renFun(ltX, 0)
                ltX += self.height
            # if on left side
            elif self.buttons[i].side == "rt":
                if pg.Rect(rtX, 0, self.height, self.height).collidepoint(
                    pg.mouse.get_pos()
                ):
                    if pg.mouse.get_pressed()[0]:
                        pg.draw.rect(
                            main.win, DARKGRAY, (rtX, 0, self.height, self.height)
                        )
                    else:
                        pg.draw.rect(main.win, GRAY, (rtX, 0, self.height, self.height))
                    if mouseDown:
                        self.buttonClicked = i
                self.buttons[i].renFun(rtX, 0)
                rtX -= self.height


# Block in hand
class SelectedBlock:
    def __init__(self):
        self.shown = False
        self.blockId = False

    # Begin selection
    def select_block(self, id):
        self.quit_selection()
        if id != "SAVE":
            self.blockId = id
            self.shown = True
        else:
            # Save level
            write_level(main.platforms.platforms)

    # Drop item in hand
    def quit_selection(self):
        self.blockId = False
        self.shown = False

    # Place block in desired location
    def place_block(self):
        global scrollX, scrollY
        # Collumn
        y = (pg.mouse.get_pos()[1] + scrollY) // blockSize
        # Cell
        x = (pg.mouse.get_pos()[0] + scrollX) // blockSize
        # Check if tile exists
        def place():
            if y < len(main.platforms.platforms):
                if x < len(main.platforms.platforms[y]):
                    main.platforms.platforms[y][x] = self.blockId
                else:
                    for i in range(x - len(main.platforms.platforms[y])):
                        main.platforms.platforms[y].append(None)
                    main.platforms.platforms[y].insert(x, self.blockId)
            else:
                for i in range(y - len(main.platforms.platforms)):
                    main.platforms.platforms.append(
                        [None] * len(main.platforms.platforms)
                    )
                row = [None] * len(main.platforms.platforms[y - 1])
                row[x] = self.blockId
                main.platforms.platforms.append(row)

        place()
        # If pressing SHIFT key, don't unselect
        if (
            not pg.key.get_pressed()[pg.K_LSHIFT]
            and not pg.key.get_pressed()[pg.K_RSHIFT]
        ):
            self.quit_selection()

    # Update self
    def update(self):
        if self.shown and mouseDown:
            self.place_block()

    # Draw self
    def render(self):
        if self.shown:
            for i in range(len(main.menuBar.buttons)):
                if main.menuBar.buttons[i].id == self.blockId:
                    main.menuBar.buttons[i].renFun(
                        pg.mouse.get_pos()[0] - main.menuBar.height / 2,
                        pg.mouse.get_pos()[1] - main.menuBar.height / 2,
                    )
                    break


# Level to be rendered
class Platforms:
    def __init__(self):
        self.platforms = read_level()

    # Render
    def render(self):
        global scrollX, scrollY
        for i in range(len(self.platforms)):
            for j in range(len(self.platforms[i])):
                if self.platforms[i][j] == "ground":
                    pg.draw.rect(
                        main.win,
                        DARKPURPLE,
                        (
                            j * blockSize - scrollX,
                            i * blockSize - scrollY,
                            blockSize,
                            blockSize,
                        ),
                    )


# Test if the script is directly ran
if __name__ == "__main__":
    main = Main()
    main.loop()
