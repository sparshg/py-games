import sys, os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame as pg

class GUtils:
    def __init__(self):
        pg.init()
    class Window:
        def __init__(self, w, h, title = None, icon_path = None):
            self.w = w
            self.h = h
            self.running = True
            if title: pg.display.set_caption(title)
            if icon_path: pg.display.set_icon(icon_path)
            self.window = pg.display.set_mode((w, h))
        def loop(self, func):
            while self.running:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        self.running = False
                        pg.display.update()
                        break
                func()
                pg.display.update()
            pg.quit()
            sys.exit()

