"""Ball module for the Pong game."""
import random
import pygame as pg
import math


# Set global variables for the various values used, some are dependent on the desktop size
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

BALL_SPEED = 500

ANGLE_LIMIT = 65
SPEED_LIMIT = 200


class Ball:
    """Class to modell the Ball and handle the collisions."""

    def __init__(self, x, y, size) -> None:
        self.x = x
        self.y = y
        self.size = size
        self.rect = pg.Rect(x, y, size, size)
        self.velocity = BALL_SPEED
        self.direction = pg.math.Vector2(self.velocity, 0)

        self.place_ball()

    def place_ball(self):
        """Place the ball in the mioddle of the screeen,
        and launch it in a random direction with a given speed."""
        start_directions = [
            random.randint(0, 45),
            random.randint(135, 225),
            random.randint(315, 360),
            random.randint(135, 225),
        ]
        self.velocity = BALL_SPEED
        self.rect = pg.Rect(self.x, self.y, self.size, self.size)
        self.direction = pg.math.Vector2(self.velocity, 0)
        self.direction.rotate_ip(start_directions[random.randint(0, 3)])

    def draw(self, win):
        """Draw the ball to the screen."""
        pg.draw.rect(win, WHITE, self.rect)

    def move(self, dt):
        """Move the ball in the set direction. (FPS compensated)"""
        self.rect.move_ip(self.direction * dt)

    def collision_wall(self):
        """Chaeck for a collision with the walls.

        If there is one, set the new direction accordingly."""
        if self.rect.top <= 0 and (self.direction.as_polar()[1] <= 0):
            new_angle = 360 - self.direction.as_polar()[1]
            self.direction = pg.math.Vector2(self.velocity, 0)
            self.direction.rotate_ip(new_angle)
        if self.rect.bottom >= pg.display.get_window_size()[1] and (
            self.direction.as_polar()[1] >= 0
        ):
            new_angle = 360 - self.direction.as_polar()[1]
            self.direction = pg.math.Vector2(self.velocity, 0)
            self.direction.rotate_ip(new_angle)

    # Not used kept as an alternative
    def collision_paddle(self, paddle_l, paddle_r):
        """Check if the ball has collided with one of the padles.

        If so, set the new direction for the ball according to normal collision."""
        angle = self.direction.as_polar()[1]
        if (angle < 90 and angle >= 0) or (angle > -90 and angle <= 0):  # heading right
            if self.rect.colliderect(paddle_r.rect):
                new_angle = 180 - self.direction.as_polar()[1]
                self.direction = pg.math.Vector2(self.velocity, 0)
                self.direction.rotate_ip(new_angle)
        elif (angle > 90 and angle <= 180) or (
            angle < -90 and angle >= -180
        ):  # heading left
            if self.rect.colliderect(paddle_l.rect):
                new_angle = 180 - self.direction.as_polar()[1]
                self.direction = pg.math.Vector2(self.velocity, 0)
                self.direction.rotate_ip(new_angle)

    def collision_paddle_directed(self, paddle_l, paddle_r):
        """Check if the ball has collided with one of the padles.

        If so, set the new direction depending where the ball hit the paddle:
        The speed and bouncing angle will be adjusted depending
        how close to the edge the collision happened. The closer to the edge
        the higher the bounce-back speed and sharper the angle (within the set limits)
        """
        angle = self.direction.as_polar()[1]

        if (angle < 90 and angle >= 0) or (angle > -90 and angle <= 0):  # heading right
            if self.rect.colliderect(paddle_r.rect):
                limit_angle = ANGLE_LIMIT / (paddle_r.rect.height / 2)
                limit_speed = SPEED_LIMIT / (paddle_r.rect.height / 2)
                distance_from_mid = paddle_r.rect.centery - self.rect.centery

                new_angle = 180 + distance_from_mid * limit_angle
                self.velocity += math.copysign(distance_from_mid, 0) * limit_speed
                self.direction = pg.math.Vector2(self.velocity, 0)
                self.direction.rotate_ip(new_angle)
        elif (angle > 90 and angle <= 180) or (
            angle < -90 and angle >= -180
        ):  # heading left
            if self.rect.colliderect(paddle_l.rect):
                limit_angle = ANGLE_LIMIT / (paddle_l.rect.height / 2)
                limit_speed = SPEED_LIMIT / (paddle_l.rect.height / 2)
                distance_from_mid = self.rect.centery - paddle_l.rect.centery

                new_angle = 0 + distance_from_mid * limit_angle
                self.velocity += math.copysign(distance_from_mid, 0) * limit_speed
                self.direction = pg.math.Vector2(self.velocity, 0)
                self.direction.rotate_ip(new_angle)

    def score(self, score):
        """Check if the ball has left the screeen on the sides.

        If so, a pint is added to the player using the score parameter."""
        if self.rect.centerx <= 0:
            self.place_ball()
            return score.add_point("r")
        elif self.rect.centerx >= pg.display.get_window_size()[0]:
            self.place_ball()
            return score.add_point("l")
