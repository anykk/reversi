import json
import logging
from time import sleep
from random import choice
from game import *
from exceptions import GameOverException, NextPlayerException, MoveError, SaveError, LoadError


LOGGER = logging.getLogger("driver")


class Reversi:
    """Main class which contains logic of the game."""
    def __init__(self, size=8, player=BLACK, mode="AI", lvl="Easy"):
        LOGGER.info(f"Game was initialized with following parameters: [{size, player, mode, lvl}].")
        self._field = Field(size)
        self._current_player = player
        self._mode = mode
        self._lvl = lvl

    @property
    def current_player(self):
        """Returns current player flag(color)."""
        return self._current_player

    @property
    def field(self):
        """Returns current field state of the game."""
        return self._field

    def save(self, filename):
        try:
            with open(filename, "w", encoding="utf-8",) as file:
                json.dump({"current_player": self._current_player,
                           "Field": {"skeleton": self.field.skeleton, "size": self.field.size,
                                     "black_count": self.field.black_count, "white_count": self.field.white_count},
                           "mode": self._mode, "lvl": self._lvl}, file, indent=4, ensure_ascii=False)
                LOGGER.info(f"Game was saved in '{filename}' file.")
        except Exception as e:
            LOGGER.error(f"Error when was trying save game: {e}")
            raise SaveError(e)

    def load(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                game = json.load(file)
            self.field._skeleton, self.field._size, self.field._black_count, self.field._white_count = game[
                "Field"].values()
            self._current_player = game["current_player"]
            self._mode = game["mode"]
            self._lvl = game["lvl"]
            LOGGER.info(f"Game was loaded from '{filename}' file.")
        except Exception as e:
            LOGGER.error(f"Error when was trying load game: {e}")
            raise LoadError(e)

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
            LOGGER.info(f"{'Black' if self.current_player == BLACK else 'White'} made move to {coords}.")
            self.next_player()
        else:
            LOGGER.warning(f"{'Black' if self.current_player == BLACK else 'White'} tried to make illegal move. Skip.")
            raise MoveError(f"{self._current_player} tried to make move with wrong coords: {coords}.")

    @property
    def mode(self):
        """Returns AI flag."""
        return self._mode

    def ai_move(self):
        """AI makes move."""
        sleep(1)
        if self._lvl == "Easy":
            possible_moves = self.get_correct_moves()
            self.make_move(choice(possible_moves))
        elif self._lvl == "Medium":
            pass
        else:
            pass

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
                LOGGER.info("Game over.")
                raise GameOverException()
            raise NextPlayerException()
