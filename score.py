"""Score module for the Pong game."""
import pygame as pg


# Set global variables for the various values used, some are dependent on the desktop size
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class Score:
    """Class to display and keep track of the score."""

    GOAL = 5

    def __init__(self, win, size_score, size_final) -> None:
        self.win_width = win.get_width()
        self.win_height = win.get_height()
        self.score_l = 0
        self.score_r = 0
        self.font_type = pg.font.get_default_font()
        self.font_score = pg.font.Font(self.font_type, size_score)
        self.font_final = pg.font.Font(self.font_type, size_final)

    def draw_score(self, win):
        """Draw the score for each player to the top of the screen."""
        ren_l = self.font_score.render(str(self.score_l), 1, WHITE)
        ren_r = self.font_score.render(str(self.score_r), 1, WHITE)

        win.blit(
            ren_l,
            (self.win_width // 2 - (self.win_width // 10 + ren_l.get_size()[0]), 10),
        )
        win.blit(ren_r, (self.win_width // 2 + self.win_width // 10, 10))

    def final_score(self, win, winner):
        """Draw the Winner to the middle of the screen."""
        ren = self.font_final.render(f"{winner} player wins!", 1, WHITE, BLACK)
        message_size = ren.get_size()
        win.blit(
            ren,
            (
                self.win_width // 2 - message_size[0] // 2,
                self.win_height // 2 - message_size[1] // 2,
            ),
        )
        pg.display.flip()

    def add_point(self, side):
        """Add point to the given player, and check for winner."""
        match side:
            case "l":
                self.score_l += 1
            case "r":
                self.score_r += 1
            case _:
                pass
        return self.check_winner()

    def check_winner(self):
        """Determine the winner according to the score kept."""
        winner = ""

        if self.score_l >= self.GOAL:
            winner = "l"
        elif self.score_r >= self.GOAL:
            winner = "r"
        else:
            winner = ""

        return winner
