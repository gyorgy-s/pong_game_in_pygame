"""Paddle module for the Pong game, to model the paddle element."""
import pygame as pg


# Set global variables for the various values used, some are dependent on the desktop size
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

MOVE_SPEED = 700


class Paddle:
    """Class to model the paddles."""

    def __init__(self, x, y, width, height) -> None:
        self.width = width
        self.height = height
        self.rect = pg.Rect(x, y, self.width, self.height)

    def draw(self, win):
        """Draw the paddle to the screen."""
        pg.draw.rect(win, WHITE, self.rect)

    def move(self, direction, dt):
        """Move the paddle in the given direction (0: up, 1: down) (FPS compensated).

        Does not move the paddle if it reached the edge of the screen."""
        if direction and (
            self.rect.y + int(MOVE_SPEED * dt)
            <= int(pg.display.get_window_size()[1] - self.height)
        ):
            self.rect.y += int(MOVE_SPEED * dt)
        elif not direction and self.rect.y > 0:
            self.rect.y -= int(MOVE_SPEED * dt)
