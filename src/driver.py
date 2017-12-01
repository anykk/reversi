from src.game import *
from time import sleep


class Reversi(object):
    """Main class which contains rules of game."""
    def __init__(self, size=8, player=BLACK):
        self._field = Field(size)
        self._current_player = player #flag

    def is_correct_move(self, coords):
        """Check that move is correct."""
        if self._field[coords] is not EMPTY and not self._field.in_range(coords):
            return False

        to_flip = []
        other = get_opponent(self._current_player)
        for dx, dy in DIRECTIONS:
            x, y = coords
            x += dx
            y += dy

            if self._field.in_range((x, y)) and self._field[x, y] == other:
                x += dx
                y += dy

                while self._field.in_range((x, y)) and self._field[x, y] == other:
                    x += dx
                    y += dy
                if self._field[x, y] == self._current_player:
                    while (x, y) != coords:
                        x -= dx
                        y -= dy
                        if (x, y) == coords:
                            break
                        to_flip.append((x, y))
        return to_flip if to_flip else False

    def get_correct_moves(self):
        """Claim all possible correct moves."""
        correct_moves = []
        size = self._field.size()

        for x in range(size):
            for y in range(size):
                if self.is_correct_move((x, y)):
                    correct_moves.append((x, y))
        return correct_moves

    def make_move(self, coords):
        """Make move and swap player flag."""
        to_flip = list(self.is_correct_move(coords))
        if not to_flip:
            return

        for coord in to_flip:
            self._field.flip(coord)
        self._field[coords] = self._current_player
        self._current_player = get_opponent(self._current_player)

    def ai_move(self):
        """AI makes move."""
        sleep(3)
        print("kek ya shodil")

    def field(self):
        return self._field
