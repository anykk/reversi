from time import sleep
from random import choice
from src.game import *


class Reversi(object):
    """Main class which contains logic of the game."""
    def __init__(self, size=8, player=BLACK, ai=True):
        self._field = Field(size)
        self._current_player = player
        self._ai = ai

    @property
    def current_player(self):
        """Returns current player flag(color)."""
        return self._current_player

    @property
    def field(self):
        """Returns current field state of the game."""
        return self._field

    def is_correct_move(self, coords):
        """Checks that move is correct and returns disks to flip if move is correct."""
        if self._field[coords] is not EMPTY or not self._field.in_range(coords):
            return False

        to_flip = []
        other = self.get_opponent()
        for dy, dx in self._field.directions:
            y, x = coords
            y += dy
            x += dx

            if self._field.in_range((y, x)) and self._field[y, x] == other:
                y += dy
                x += dx

                while self._field.in_range((y, x)) and self._field[y, x] == other:
                    y += dy
                    x += dx

                if self._field.in_range((y, x)) and self._field[y, x] == self._current_player:
                    while (x, y) != coords:
                        y -= dy
                        x -= dx
                        if (y, x) == coords:
                            break
                        to_flip.append((y, x))
        return to_flip if to_flip else False

    def get_correct_moves(self):
        """Claim all possible correct moves."""
        correct_moves = []
        size = self._field.size

        for y in range(size):
            for x in range(size):
                if self.is_correct_move((y, x)):
                    correct_moves.append((y, x))
        return correct_moves

    def make_move(self, coords):
        """Make move and swap player flag."""
        to_flip = self.is_correct_move(coords)
        if to_flip:
            for coord in list(to_flip):
                self._field.flip(coord)
            self._field[coords] = self._current_player
            self.next_player()
        else:
            raise ValueError("You can't place disk here.")

    @property
    def ai(self):
        """Returns AI flag."""
        return self._ai

    def ai_move(self):
        """AI makes move."""
        sleep(1.5)
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

    def next_player(self):
        """Switch flag to next player."""
        self._current_player = self.get_opponent()
        moves = self.get_correct_moves()
        if not moves:
            self._current_player = self.get_opponent()
            moves = self.get_correct_moves()
            if not moves:
                raise RuntimeError("Game over.")
