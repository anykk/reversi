from src.utils import *


class Field(object):
    """Class which represents game field."""
    def __init__(self, size):
        """Initialize game field."""
        if size % 2 or size < 4:
            raise ValueError("Field can't be not even or less than 4.")
        self._size = size
        self._field = [[EMPTY for _ in range(self._size)] for _ in range(self._size)]
        self._black_count = 0
        self._white_count = 0
        self[self._size // 2 - 1, self._size // 2 - 1] = WHITE
        self[self._size // 2 - 1, self._size // 2] = BLACK
        self[self._size // 2, self._size // 2 - 1] = BLACK
        self[self._size // 2, self._size // 2] = WHITE

    def field(self):
        return self._field

    def is_full(self):
        """Check that field is full."""
        return self._white_count + self._black_count == self._size ** 2

    def flip(self, coords):
        """Flip piece. It mean that piece changes its color."""
        if self[coords] == WHITE:
            self._white_count -= 1
            self[coords] = BLACK
        elif self[coords] == BLACK:
            self._black_count -= 1
            self[coords] = WHITE
        else:
            raise TypeError("Can't flip EMPTY or another type of cell.")

    def in_range(self, coords):
        """Check, that coordinates are correct."""
        return 0 <= coords[0] < self._size and 0 <= coords[1] < self._size

    def piece_count(self):
        return self._white_count, self._black_count

    def __getitem__(self, coords):
        """Get piece from field."""
        return self._field[coords[0]][coords[1]]

    def __setitem__(self, coords, color):
        """Set piece to field and inc score."""
        self._field[coords[0]][coords[1]] = color
        self._white_count += 1 if color == WHITE else 0
        self._black_count += 1 if color == BLACK else 0

    def __str__(self):
        """String representation of field."""
        repr_ = []
        for row in self:
            for col in row:
                if col is EMPTY:
                    repr_.append('.')
                else:
                    repr_.append('X') if col is BLACK else repr_.append('O')
            repr_.append('\n')
        return ''.join(repr_)

    def size(self):
        return self._size

    def __iter__(self):
        return self._field.__iter__()
