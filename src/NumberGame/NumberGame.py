import os
import pygame
import sys

from numpad import NumPad
from button import RestartButton
from text import ClueText
import logic as logic
import constants as const


class Game:
    def __init__(self):
        # Enter instances here -----------------------------------------------------
        logic.gen_secret_num()
        self.restart_button = RestartButton("Restart", 110, 30, (680, 360), const.RED)
        self.numpad = NumPad()
        self.clue_text = ClueText(10, 5)

    def run(self):  # This bad boy runs every frame -------------------------------
        # Enter functions here
        self.draw_ui_rect()
        self.numpad.draw(screen)
        self.restart_button.draw(screen)
        self.clue_text.draw(screen)

    @staticmethod
    def draw_ui_rect():
        pygame.draw.rect(screen, const.CREAM, (670, 0, 280, 400))  # 'numpad' rect
        pygame.draw.rect(screen, const.GREEN, (670, 0, 130, 30))  # 'timer' rect
        pygame.draw.rect(screen, const.GREEN, (670, 260, 130, 140))  # 'buttons' rect


# Game Setups -------------------------------------------------------------
# Switch to parent directory
path = os.path.dirname(__file__)
os.chdir(os.path.abspath(os.path.join(path, os.pardir)))

# Initialize pygame
pygame.init()
clock = pygame.time.Clock()

# Initiate screen
screen_width = 800
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))

# Set caption, icon, color
pygame.display.set_caption("NumberGame!")


def run_game():
    # Initiate instances
    program = Game()

    # Main loop (runs every tick) -------------------------------------------------
    while True:
        # Event code
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Game code
        program.run()

        # Updates, mind the order
        pygame.display.flip()
        screen.fill(const.PURPLE)

        # Time & Clock
        clock.tick(60)


if __name__ == '__main__':
    run_game()
