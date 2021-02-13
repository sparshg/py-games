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
SIZE = (600, 400)
FPS = 60
WHITE = "#f1f1f1"
BLACK = "#101010"

# The main controller
class Main:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Tic-Tac-Toe")

        Main.win = pygame.display.set_mode(SIZE)
        Main.running = True
        self.clock = pygame.time.Clock()
        # dt is the time since last frame, which is ideally 1/FPS
        self.dt = self.clock.tick(FPS)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Main.running = False

    def draw(self):
        Main.win.fill(BLACK)
        pygame.display.update()

    # The main loop
    def loop(self):
        while self.running:
            self.check_events()
            self.draw()
            # Calculate dt for next frame
            self.dt = self.clock.tick(FPS)
        pygame.quit()


# Test if the script is directly ran
if __name__ == "__main__":
    Main().loop()
