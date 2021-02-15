#!/usr/bin/python
"""
Github repo can be found here:
https://github.com/sparshg/pycollab
"""
from os import environ
import math

# Hide pygame Hello prompt
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
from pygame.math import Vector2

# Declare some constants and variables
WIDTH, HEIGHT = (600, 400)
FPS = 60
WHITE = "#F1F1F1"
BLACK = "#101010"
ORANGE = "#FF6600"
RED = "#FF1F00"


class Frame:
    def __init__(self, gap=110):
        self.length = 3 * gap
        self.gap = gap
        self.turn = 1
        self.remove = False
        # fmt: off
        self.points = self.cartesian_to_standard([
            [self.gap/2, self.length/2], [self.gap/2, -self.length/2],
            [-self.gap/2, -self.length/2], [-self.gap/2, self.length/2],
            [-self.length/2, self.gap/2], [self.length/2, self.gap/2],
            [self.length/2, -self.gap/2], [-self.length/2, -self.gap/2],
        ])
        # fmt: on
        self.rects = []
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.moves = [[None, None, None], [None, None, None], [None, None, None]]

        for i in range(3):
            for j in range(3):
                self.rects.append(
                    pygame.Rect((-1.5 + 1 * j) * gap, (1.5 - 1 * i) * gap, gap, gap)
                )
        self.rects = self.cartesian_to_standard(self.rects)

        self.animations = [
            Animate(700 + i * 100).line(self.points[i], self.points[i + 1])
            for i in range(0, len(self.points), 2)
        ]

    # Convert given list cartesian coordinates to pygame coordinates
    @staticmethod
    def cartesian_to_standard(coords, origin=(WIDTH / 2, HEIGHT / 2)):
        for coord in coords:
            coord[0] = coord[0] + origin[0]
            coord[1] = -coord[1] + origin[1]
        return coords

    @staticmethod
    def standard_to_cartesian(coords, origin=(-WIDTH / 2, HEIGHT / 2)):
        return Frame.cartesian_to_standard(coords, origin)

    def detect_click(self, pos):
        for rect in self.rects:
            if rect.collidepoint(pos):
                # Spawn O or X
                # Update the board
                center = self.standard_to_cartesian([list(rect.center)])[0]
                index = (1 - int(center[1] / self.gap), int(center[0] / self.gap) + 1)
                self.board[index[0]][index[1]] = self.turn
                self.moves[index[0]][index[1]] = OX(self.turn, rect.center)
                self.rects.remove(rect)
                self.turn *= -1
                # Check if win
                self.check_win(index)
                break

    def check_win(self, index):
        def reset():
            for m in self.moves:
                for n in m:
                    if n is not None:
                        n.wait_and_remove = True
                        n.remove_time = (
                            2 * n.blink_count * n.blink_dur + pygame.time.get_ticks()
                        )

        def check(sum, i, j):
            if abs(sum) == 3:
                self.rects = []
                prev = i, j
                for t in range(3):
                    if i is None:
                        i = t
                    if i == -2:
                        i = 2 - t
                    if j is None:
                        j = t
                    self.moves[i][j].blink = True
                    self.moves[i][j].blink_start = pygame.time.get_ticks()
                    i, j = prev
                reset()

        # fmt: off
        sum = self.board[index[0]][0] + self.board[index[0]][1] + self.board[index[0]][2]
        check(sum, index[0], None)
        sum = self.board[0][index[1]] + self.board[1][index[1]] + self.board[2][index[1]]
        check(sum, None, index[1])
        sum = self.board[0][0] + self.board[1][1] + self.board[2][2]
        check(sum, None, None)
        sum = self.board[2][0] + self.board[1][1] + self.board[0][2]
        check(sum, -2, None)
        # fmt:on
        tie = 0
        for i in self.board:
            if 0 not in i:
                tie += 1
        if tie == 3:
            reset()

    def setup_remove(self, dur=500, animate=False):
        if not self.remove:
            self.remove = True
            self.remove_time = pygame.time.get_ticks() + dur
            if animate:
                for i in self.animations:
                    i.setup_remove(dur)

    def draw(self):
        for animation in self.animations:
            animation.update()
        for i in self.moves:
            for move in i:
                if move is not None:
                    move.draw()
        if self.remove:
            if pygame.time.get_ticks() > self.remove_time:
                main.reset()


class OX:
    def __init__(self, _type, center):
        self.type = _type
        self.center = center
        self.blink = False
        self.blink_count = 3
        self.blink_dur = 250
        self.blink_start = None
        self.wait_and_remove = False
        self.remove_time = None

        if _type == 1:
            self.animation = Animate(color=ORANGE).cross(center)
        elif _type == -1:
            self.animation = Animate(color=RED).circle(center)

    def draw(self):
        if self.blink:
            if pygame.time.get_ticks() < self.blink_start + self.blink_dur:
                self.animation.update()
            elif pygame.time.get_ticks() > self.blink_start + 2 * self.blink_dur:
                self.blink_start = pygame.time.get_ticks()
                self.blink_count -= 1
                if self.blink_count == 0:
                    self.blink = False
        else:
            self.animation.update()

        if self.wait_and_remove:
            if pygame.time.get_ticks() > self.remove_time:
                self.animation.setup_remove()
                main.frame.setup_remove()
                self.wait_and_remove = False


class Animate:

    LINEAR = lambda x: x
    EASE_OUT_SINE = lambda x: math.sin(math.pi / 2 * x)
    EASE_IO_SINE = lambda x: 0.5 - math.cos(math.pi * x) / 2
    EASE_OUT_QUART = lambda x: 1 - pow(1 - x, 4)
    EASE_IN_QUART = lambda x: pow(x, 4)

    def EASE_IO_QUART(x):
        return 8 * pow(x, 4) if x < 0.5 else 1 - pow(-2 * x + 2, 4) / 2

    def __init__(self, dur=500, color=WHITE, fn=EASE_OUT_QUART):
        self.color = color
        self.function = fn
        self.remove = False
        self.dur = dur
        self.start_time = pygame.time.get_ticks()
        self.final_time = self.start_time + dur
        self.type = None
        self.sub_animations = None

    def line(self, p1, p2, width=8):
        self.type = "line"
        self.finished = False
        self.width = width
        self.p1 = Vector2(p1)
        self.p2 = Vector2(p2)
        self.p = self.p2 - self.p1
        self.length = self.p.magnitude()
        return self

    def circle(self, center=[WIDTH / 2, HEIGHT / 2], radius=38, width=8):
        self.type = "circle"
        self.finished = False
        self.width = width
        self.radius = radius
        self.r = radius
        self.center = Vector2(center)
        self.rect = pygame.Rect(
            (center - Vector2(radius, radius)), (2 * radius, 2 * radius)
        )
        return self

    def cross(self, center=[WIDTH / 2, HEIGHT / 2], length=40, width=10):
        self.type = "cross"
        # fmt: off
        points = [
            Vector2(-length, 0), Vector2(length, 0),
            Vector2(0, length), Vector2(0, -length)
        ]
        # fmt: on
        for point in points:
            point.update(point.rotate(45) + Vector2(center))

        self.sub_animations = [
            Animate(self.dur + i * 150, self.color, self.function).line(
                points[i], points[i + 1], width
            )
            for i in range(0, len(points), 2)
        ]
        return self

    def setup_remove(self, dur=500):
        self.finished = True
        self.remove = True
        self.dur = dur
        self.start_time = pygame.time.get_ticks()
        self.final_time = self.start_time + self.dur
        if self.sub_animations is not None:
            for i in self.sub_animations:
                i.setup_remove(dur)

    def update(self, skip=False):

        # Call method recursively
        if self.type == "cross":
            for animation in self.sub_animations:
                animation.update()
            return

        # Calculate the animation
        if not self.finished or self.remove:
            if pygame.time.get_ticks() < self.final_time and not skip:
                fraction = (pygame.time.get_ticks() - self.start_time) / self.dur
                if fraction < 0.01:
                    fraction += 0.008

                if self.remove:
                    fraction = 1 - fraction

                if self.type == "line":
                    self.p.scale_to_length(self.length * self.function(fraction))
                elif self.type == "circle":
                    self.r = self.radius - self.width * self.function(fraction)
            else:
                if self.type == "line":
                    self.p = self.p2 - self.p1
                    if self.remove:
                        self.p = [0, 0]
                if self.type == "circle":
                    self.r = self.radius - self.width
                    if self.remove:
                        self.r = self.radius
                self.remove = False
                self.finished = True

        # Draw stuff
        if self.type == "line":
            pygame.draw.line(
                main.win, self.color, self.p1, self.p + self.p1, self.width
            )
        elif self.type == "circle":
            pygame.draw.circle(main.win, self.color, self.center, self.radius)
            pygame.draw.circle(main.win, BLACK, self.center, self.r)


# The main controller
class Main:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Tic-Tac-Toe")

        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True

        self.frame = Frame()
        self.clock = pygame.time.Clock()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main.running = False
            if event.type == pygame.MOUSEBUTTONUP:
                self.frame.detect_click(pygame.mouse.get_pos())

    def draw(self):
        self.win.fill(BLACK)
        self.frame.draw()
        pygame.display.update()

    def reset(self):
        self.frame = Frame()

    # The main loop
    def loop(self):
        while self.running:
            self.check_events()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()


# Test if the script is directly ran
if __name__ == "__main__":
    main = Main()
    main.loop()
