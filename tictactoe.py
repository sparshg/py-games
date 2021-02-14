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
WHITE = "#f1f1f1"
BLACK = "#101010"


class Frame:
    def __init__(self, len=320, gap=110):
        self.len = len
        self.gap = gap
        # fmt: off
        self.points = self.cartesian([
            [self.gap/2, self.len/2], [self.gap/2, -self.len/2],
            [-self.gap/2, self.len/2], [-self.gap/2, -self.len/2],
            [-self.len/2, self.gap/2], [self.len/2, self.gap/2],
            [-self.len/2, -self.gap/2], [self.len/2, -self.gap/2],
        ])
        # fmt: on

    # Convert given list cartesian coordinates to pygame coordinates
    @staticmethod
    def cartesian(coords, new_origin=(WIDTH / 2, HEIGHT / 2)):
        for coord in coords:
            coord[0] = coord[0] + new_origin[0]
            coord[1] = -coord[1] + new_origin[1]
        return coords

    def draw(self):
        for i in range(0, len(self.points), 2):
            pygame.draw.line(Main.win, WHITE, self.points[i], self.points[i + 1], 10)


# The main controller
class Main:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Tic-Tac-Toe")

        Main.win = pygame.display.set_mode((WIDTH, HEIGHT))
        Main.running = True

        self.frame = Frame()
        self.clock = pygame.time.Clock()
        # dt is the time since last frame, which is ideally 1/FPS
        self.dt = self.clock.tick(FPS)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Main.running = False

    def draw(self):
        Main.win.fill(BLACK)
        self.frame.draw()
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
