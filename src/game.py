EMPTY = '.'
WHITE = 'O'
BLACK = 'X'


class Field(object):
    """Class which represents game field."""
    _DIRECTIONS = ((0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1))

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

    def white_count(self):
        """Get count of white pieces."""
        return self._white_count

    def black_count(self):
        """Get count of black pieces"""
        return self._black_count

    def __getitem__(self, coords):
        """Get piece from field."""
        return self._field[coords[0]][coords[1]]

    def __setitem__(self, coords, color):
        """Set piece on the field and inc score."""
        self._field[coords[0]][coords[1]] = color
        self._white_count += 1 if color == WHITE else 0
        self._black_count += 1 if color == BLACK else 0

    def __str__(self):
        """String representation of field."""
        repr_ = []
        for row in self:
            for col in row:
                repr_.append(col)
            repr_.append('\n')
        return ''.join(repr_)

    def size(self):
        """Get size of field."""
        return self._size

    def directions(self):
        """Get directions."""
        return self._DIRECTIONS

    def __iter__(self):
        """Iter trough the field."""
        return self._field.__iter__()
