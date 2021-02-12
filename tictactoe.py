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

# The main controller
class Main:
    def __init__(self, win):
        self.running = True
        self.win = win
        self.clock = pygame.time.Clock()
        # dt is the time since last frame, which is ideally 1/FPS
        self.dt = self.clock.tick(FPS)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def draw(self):
        self.win.fill("#101010")
        pygame.display.update()

    # The main loop
    def loop(self):
        while self.running:
            self.check_events()
            self.draw()
            # Calculate dt for next frame
            self.dt = self.clock.tick(FPS)


def main():
    pygame.init()
    pygame.display.set_caption("Tic-Tac-Toe")
    win = pygame.display.set_mode(SIZE)
    Main(win).loop()
    pygame.quit()


# Test if the script is directly ran
if __name__ == "__main__":
    main()