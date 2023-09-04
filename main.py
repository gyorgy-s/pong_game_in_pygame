"""Main module for the Pong game."""
import time
import pygame as pg
from paddle import Paddle
from ball import Ball
from score import Score

pg.init()


# Get desktop size, and dinamically determine the size for thte game window
desktop_size = pg.display.get_desktop_sizes()
desktop_size = list(desktop_size[0])
desktop_size.sort()

WIDTH, HEIGHT = desktop_size[0], int(desktop_size[0] * 0.7)

window = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Pong")

# Set global variables for the various values used, some are dependent on the desktop size
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

FPS = 60

DIVIDER_WIDTH = WIDTH // 200
DIVIDER_NUMBER = (HEIGHT // 100) * 2 + 1
DIVIDER_SEGMENT_HEIGHT = HEIGHT / DIVIDER_NUMBER

PADDLE_WIDTH, PADDLE_HEIGHT = WIDTH // 50, HEIGHT // 6
PADDLE_SPACE = 20
UP, DOWN = 0, 1

BALL_SIZE = WIDTH // 50

divider_segments = [
    pg.Rect(
        WIDTH // 2 - DIVIDER_WIDTH // 2,
        0 + i * DIVIDER_SEGMENT_HEIGHT,
        DIVIDER_WIDTH,
        DIVIDER_SEGMENT_HEIGHT,
    )
    for i in range(DIVIDER_NUMBER)
]


def draw_divider(win, segments):
    """Draw the divider in the midle. Alternating between White and black rects."""
    for i, _ in enumerate(segments):
        if i % 2 == 1:
            pg.draw.rect(win, BLACK, segments[i])
        elif i % 2 == 0:
            pg.draw.rect(win, WHITE, segments[i])


def draw(win, paddle_l, paddle_r, ball, score):
    """Draw the elements to the window."""
    win.fill(BLACK)
    draw_divider(win, divider_segments)
    paddle_l.draw(win)
    paddle_r.draw(win)
    ball.draw(win)
    score.draw_score(win)

    pg.display.flip()


def init_elements():
    """Initialize the elements of the game.

    Used for resetting the game as well."""
    return (
        Paddle(
            PADDLE_SPACE, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT
        ),
        Paddle(
            WIDTH - PADDLE_WIDTH - PADDLE_SPACE,
            HEIGHT // 2 - PADDLE_HEIGHT // 2,
            PADDLE_WIDTH,
            PADDLE_HEIGHT,
        ),
        Ball(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE),
        Score(window, HEIGHT // 30, HEIGHT // 15),
    )


def main():
    """Main game loop."""
    run = True
    clock = pg.time.Clock()
    playing = True
    prev_time = time.time()

    paddle_left, paddle_right, ball, score = init_elements()

    while run:
        # Delta time for the game, to stabilize the running speed, independent on the FPS
        dt = time.time() - prev_time
        prev_time = time.time()

        keys_pressed = pg.key.get_pressed()

        if playing:
            ball.move(dt)
            ball.collision_wall()
            ball.collision_paddle_directed(paddle_left, paddle_right)
            winner = ball.score(score)
            draw(window, paddle_left, paddle_right, ball, score)
            if winner:
                if winner == "l":
                    score.final_score(window, "Left")
                elif winner == "r":
                    score.final_score(window, "Right")
                playing = False

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    playing = True
                    paddle_left, paddle_right, ball, score = init_elements()

        if keys_pressed[pg.K_ESCAPE]:
            pg.quit()
            exit()
        if keys_pressed[pg.K_UP]:
            paddle_right.move(UP, dt)
        if keys_pressed[pg.K_DOWN]:
            paddle_right.move(DOWN, dt)
        if keys_pressed[pg.K_w]:
            paddle_left.move(UP, dt)
        if keys_pressed[pg.K_s]:
            paddle_left.move(DOWN, dt)

        clock.tick(FPS)


if __name__ == "__main__":
    main()
