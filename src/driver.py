from time import sleep
from random import choice
from src.game import *


class Reversi(object):
    """Main class which contains logic of the game."""
    def __init__(self, size=8, player=BLACK, ai=True):
        self._field = Field(size)
        self._current_player = player
        self._ai = ai

    def current_player(self):
        return self._current_player

    def is_correct_move(self, coords):
        """Checks that move is correct and returns pieces to flip if move is correct."""
        if self._field[coords] is not EMPTY and not self._field.in_range(coords):
            return False

        to_flip = []
        other = self.get_opponent()
        for dx, dy in self._field.directions():
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
        self._current_player = self.get_opponent()

    def ai(self):
        """Returns AI flag."""
        return self._ai

    def ai_move(self):
        """AI makes move."""
        sleep(3)
        possible_moves = self.get_correct_moves()
        self.make_move(choice(possible_moves))

    def get_opponent(self):
        """Gets opponent to current player."""
        if self._current_player == WHITE:
            return BLACK
        if self._current_player == BLACK:
            return WHITE
        else:
            raise ValueError("Can't get opponent to this.")

    def field(self):
        """Returns current field state of the game."""
        return self._field
