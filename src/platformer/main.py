#!/usr/bin/python
"""
Github repo can be found here:
https://github.com/sparshg/py-games
"""

from gutils import *
from entities import *
from colors import *

gutils = GUtils()
entities = Entities()

mainWindow = gutils.Window(1000, 600, "Platformer")
def update():
    mainWindow.window.fill(BLACK)
    entities.update(mainWindow.window, entities.entities)
mainWindow.loop(update)

