import json
import sys
import time
from copy import deepcopy

import pygame
from pygame.locals import *

from logic import *

# TODO: Add a RULES button on start page
# TODO: Add score keeping

# set up pygame for main gameplay
pygame.init()
const = json.load(open("constants.json", "r"))
screen = pygame.display.set_mode(
    (const["size"], const["size"]))
my_font = pygame.font.SysFont(const["font"], const["font_size"], bold=True)
WHITE = (255, 255, 255)


def winCheck(board, status, theme, text_col):
    """
    Check game status and display win/lose result.
    Parameters:
        board (list): game board
        status (str): game status
        theme (str): game interface theme
        text_col (tuple): text colour
    Returns:
        board (list): updated game board
        status (str): game status
    """
    if status != "PLAY":
        size = const["size"]
        # Fill the window with a transparent background
        s = pygame.Surface((size, size), pygame.SRCALPHA)
        s.fill(const["colour"][theme]["over"])
        screen.blit(s, (0, 0))

        # Display win/lose status
        if status == "WIN":
            msg = "YOU WIN!"
        else:
            msg = "GAME OVER!"

        screen.blit(my_font.render(msg, 1, text_col), (140, 180))
        # Ask user to play again
        screen.blit(my_font.render(
            "Play again? (y/ n)", 1, text_col), (80, 255))

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT or \
                        (event.type == pygame.KEYDOWN and event.key == K_n):
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN and event.key == K_y:
                    # 'y' is pressed to start a new game
                    board = newGame(theme, text_col)
                    return (board, "PLAY")
    return (board, status)


def newGame(theme, text_col):
    """
    Start a new game by resetting the board.
    Parameters:
        theme (str): game interface theme
        text_col (tuple): text colour
    Returns:
        board (list): new game board
    """
    # clear the board to start a new game
    board = [[0] * 4 for _ in range(4)]
    display(board, theme)

    screen.blit(my_font.render("NEW GAME!", 1, text_col), (130, 225))
    pygame.display.update()
    # wait for 1 second before starting over
    time.sleep(1)

    board = fillTwoOrFour(board, iter=2)
    display(board, theme)
    return board


def restart(board, theme, text_col):
    """
    Ask user to restart the game if 'n' key is pressed.
    Parameters:
        board (list): game board
        theme (str): game interface theme
        text_col (tuple): text colour
    Returns:
        board (list): new game board
    """
    # Fill the window with a transparent background
    s = pygame.Surface((const["size"], const["size"]), pygame.SRCALPHA)
    s.fill(const["colour"][theme]["over"])
    screen.blit(s, (0, 0))

    screen.blit(my_font.render("RESTART? (y / n)", 1, text_col), (85, 225))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or \
                    (event.type == pygame.KEYDOWN and event.key == K_n):
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == K_y:
                board = newGame(theme, text_col)
                return board


def display(board, theme):
    """
    Display the board 'matrix' on the game window.
    Parameters:
        board (list): game board
        theme (str): game interface theme
    """
    screen.fill(tuple(const["colour"][theme]["background"]))
    box = const["size"] // 4
    padding = const["padding"]
    for i in range(4):
        for j in range(4):
            colour = tuple(const["colour"][theme][str(board[i][j])])
            pygame.draw.rect(screen, colour, (j * box + padding,
                                              i * box + padding,
                                              box - 2 * padding,
                                              box - 2 * padding), 0)
            if board[i][j] != 0:
                if board[i][j] in (2, 4):
                    text_colour = tuple(const["colour"][theme]["dark"])
                else:
                    text_colour = tuple(const["colour"][theme]["light"])
                # display the number at the centre of the tile
                screen.blit(my_font.render("{:>4}".format(
                    board[i][j]), 1, text_colour),
                    # 2.5 and 7 were obtained by trial and error
                    (j * box + 2.5 * padding, i * box + 7 * padding))
    pygame.display.update()


def playGame(theme, difficulty):
    """
    Main game loop function.
    Parameters:
        theme (str): game interface theme
        difficulty (int): game difficulty, i.e., max. tile to get
    """
    # initialise game status
    status = "PLAY"
    # set text colour according to theme
    if theme == "light":
        text_col = tuple(const["colour"][theme]["dark"])
    else:
        text_col = WHITE
    board = newGame(theme, text_col)

    # main game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or \
                    (event.type == pygame.KEYDOWN and event.key == K_q):
                # exit if q is pressed
                pygame.quit()
                sys.exit()

            # a key has been pressed
            if event.type == pygame.KEYDOWN:
                # 'n' is pressed to restart the game
                if event.key == pygame.K_n:
                    board = restart(board, theme, text_col)

                if str(event.key) not in const["keys"]:
                    # no direction key was pressed
                    continue
                else:
                    # convert the pressed key to w/a/s/d
                    key = const["keys"][str(event.key)]

                # obtain new board by performing move on old board's copy
                new_board = move(key, deepcopy(board))

                # proceed if change occurs in the board after making move
                if new_board != board:
                    # fill 2/4 after every move
                    board = fillTwoOrFour(new_board)
                    display(board, theme)
                    # update game status
                    status = checkGameStatus(board, difficulty)
                    # check if the game is over
                    (board, status) = winCheck(board, status, theme, text_col)