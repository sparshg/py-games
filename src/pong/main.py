import pygame
import sys
import random
from random import randint


# class Vec:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y


def ball_animation():
    global ball_speed_x, ball_speed_y
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.colliderect(player):
        ball_speed_x = -1 * (random.uniform(5, 9))
    elif ball.colliderect(opponent):
        ball_speed_x = 1 * (random.uniform(5, 9))
    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1
    if ball.left <= 0 and ball_speed_x < 0:
        ball_speed_x *= -1
    if ball.right >= screen_width and ball_speed_x > 0:
        ball_speed_x *= -1


def player_animation():
    global player
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height


def opponent_animation():
    global opponent
    opponent.y += opponent_speed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height


def score(x, y):
    global smallfont
    text_1 = smallfont.render("" + str(x), True, (211, 211, 211))
    text_2 = smallfont.render("" + str(y), True, (211, 211, 211))
    screen.blit(text_1, (((screen_width / 4) - (25 / 2)), 70))
    screen.blit(text_2, (((3 * screen_width / 4) - (25 / 2)), 70))


pygame.init()
clock = pygame.time.Clock()

screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong")

ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
player = pygame.Rect(screen_width - 10, screen_height / 2 - 70, 10, 140)
opponent = pygame.Rect(0, screen_height / 2 - 70, 10, 140)

bg_color = (40, 40, 40)
light_grey = (211, 211, 211)
ball_color = (211, 211, 211)

ball_speed_x = 7
ball_speed_y = 7
player_speed = 0
opponent_speed = 0
score_1 = 0
score_2 = 0
smallfont = pygame.font.SysFont("freesansbold.ttf", 90)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        player_speed = 0
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            player_speed += 7
        if pygame.key.get_pressed()[pygame.K_UP]:
            player_speed -= 7

        opponent_speed = 0
        if pygame.key.get_pressed()[pygame.K_s]:
            opponent_speed += 7
        if pygame.key.get_pressed()[pygame.K_w]:
            opponent_speed -= 7

    if ball.right >= screen_width:
        score_1 += 1
    if ball.left <= 0:
        score_2 += 1

    ball_animation()
    player_animation()
    opponent_animation()

    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, ball_color, ball)
    pygame.draw.aaline(
        screen, light_grey, (screen_width / 2, 0), (screen_width / 2, screen_height)
    )
    score(score_1, score_2)

    pygame.display.flip()
    clock.tick(60)
