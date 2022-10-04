import pygame
import constants as const


class Text:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.y_space = 20
        self.text_data = []

        # font
        self.chary = pygame.font.SysFont("Arial", 20)

    def append_text_data(self, text, color):
        self.text_data.append([text, color])

    def render(self, screen):
        for i, (text, color) in enumerate(self.text_data):
            text_obj = self.chary.render(text, True, color)
            screen.blit(text_obj, (self.x, i * self.y_space + self.y))

        self.text_data = []


class ClueText(Text):
    def draw(self, screen):
        if const.game_state == 'won' or const.game_state == 'lost' or const.game_state == 'main_game':
            self.append_text_data(f"Guess the 4 digit number combination! You have {const.remaining_attempts} "
                                  f"attempts left", const.CREAM)

            for i in range(const.attempts):
                self.append_text_data(f"> Attempt #{i + 1}: {const.correct_num[i]} correct numbers, "
                                      f"{const.correct_pos[i]} are in the correct position. [{const.combinations[i]}]",
                                      const.BLUE)

        if const.game_state == 'won':
            self.append_text_data(f"You win! The correct number was {const.secret_num}", const.LIME)
            self.append_text_data("Press the restart button to play again", const.RED)

        if const.game_state == 'lost':
            self.append_text_data(f"You have run out of attempt! You lost. The correct number was {const.secret_num}",
                                  const.RED)
            self.append_text_data("Press the restart button to play again", const.RED)

        self.render(screen)
