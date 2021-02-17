#!/usr/bin/python
"""
Github repo can be found here:
https://github.com/sparshg/pycollab
"""
from os import environ

# Hide pygame Hello prompt
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame

# Declare some constants and variables
WIDTH, HEIGHT = (600, 400)
FPS = 60
WHITE = "#F1F1F1"
BLACK = "#101010"

# The main controller
class Main:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Platformer")

        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        self.clock = pygame.time.Clock()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main.running = False

    # Update things
    def update(self):
        pass

    # Draw things
    def draw(self):
        self.win.fill(BLACK)
        pygame.display.update()

    # The main loop
    def loop(self):
        while self.running:
            self.check_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()


# Test if the script is directly ran
if __name__ == "__main__":
    main = Main()
    main.loop()