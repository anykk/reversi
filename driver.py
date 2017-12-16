from time import sleep
from random import choice
from game import *
from exceptions import GameOverException, NoMovesException, MoveError, SaveError, LoadError


class Reversi:
    """Main class which contains logic of the game."""
    def __init__(self, size=8, player=BLACK, mode="Classic", opponent="Human", lvl=None):
        self._field = Field(size)
        self._current_player = player
        self._mode = mode
        self._opponent = opponent
        self._lvl = lvl

    @property
    def winner(self):
        """Returns winner."""
        if self._field.black_count > self._field.white_count:
            return "Black won!"
        elif self._field.white_count > self._field.black_count:
            return "White won!"
        else:
            return "Draw!"

    @property
    def current_player(self):
        """Returns current player flag(color)."""
        return self._current_player

    @property
    def str_player(self):
        """Returns string player name."""
        return "Black" if self._current_player == BLACK else "White"

    @property
    def field(self):
        """Returns current field state of the game."""
        return self._field

    def is_correct_move(self, coords):
        """Checks that move is correct and returns disks to flip if move is correct."""
        try:
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
        except IndexError:
            return False

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
            raise MoveError(f"{self._current_player} tried to make move with wrong coords: {coords}.")

    @property
    def opponent(self):
        """Returns AI flag."""
        return self._opponent

    def ai_move(self):
        """AI makes move."""
        sleep(1)
        if self._lvl == "Easy":
            possible_moves = self.get_correct_moves()
            self.make_move(possible_moves[0])
        elif self._lvl == "Medium":
            possible_moves = self.get_correct_moves()
            self.make_move(choice(possible_moves))
        else:
            possible_moves = self.get_correct_moves()
            good_moves = [(0, 0), (0, self._field.size), (self._field.size, 0), (self._field.size, self._field.size)]
            moved = False
            for coords in good_moves:
                if coords in possible_moves:
                    self.make_move(coords)
                    moved = True
                    break
            if not moved:
                self.make_move(choice(possible_moves))

    def get_opponent(self):
        """Gets opponent to current player."""
        if self._current_player == WHITE:
            return BLACK
        if self._current_player == BLACK:
            return WHITE
        else:
            raise TypeError("Can't get opponent to this.")

    def next_player(self):
        """Switch flag to next player."""
        self._current_player = self.get_opponent()
        moves = self.get_correct_moves()
        if not moves:
            self._current_player = self.get_opponent()
            moves = self.get_correct_moves()
            if not moves:
                raise GameOverException()
            raise NoMovesException()
