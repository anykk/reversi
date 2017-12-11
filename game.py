from exceptions import IllegalArgumentError


BLACK = 'X'
WHITE = 'O'
EMPTY = '.'


class Field:
    """Class which represents game field."""
    _DIRECTIONS = ((0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1))

    def __init__(self, size):
        """Initialize game field."""
        if size % 2 or size < 4:
            raise IllegalArgumentError("Field can't be not even or less than 4.")
        self._size = size
        self._skeleton = [[EMPTY for _ in range(self._size)] for _ in range(self._size)]
        self._black_count = 0
        self._white_count = 0
        self.set_up()

    def set_up(self):
        """Set disks on start positions."""
        self[self._size // 2 - 1, self._size // 2 - 1] = WHITE
        self[self._size // 2 - 1, self._size // 2] = BLACK
        self[self._size // 2, self._size // 2 - 1] = BLACK
        self[self._size // 2, self._size // 2] = WHITE

    @property
    def size(self):
        """Get size of field."""
        return self._size

    @property
    def skeleton(self):
        """Get skeleton of field."""
        return self._skeleton

    @property
    def directions(self):
        """Get directions."""
        return self._DIRECTIONS

    @property
    def is_full(self):
        """Check that field is full."""
        return self._white_count + self._black_count == self._size ** 2

    def flip(self, coords):
        """Flip disk. It mean that disk changes its color."""
        if self[coords] == WHITE:
            self._white_count -= 1
            self[coords] = BLACK
        elif self[coords] == BLACK:
            self._black_count -= 1
            self[coords] = WHITE
        else:
            raise TypeError("Can't flip EMPTY or another type of disk.")

    def in_range(self, coords):
        """Check, that coordinates are correct."""
        return 0 <= coords[0] < self._size and 0 <= coords[1] < self._size

    @property
    def white_count(self):
        """Get count of white disks."""
        return self._white_count

    @property
    def black_count(self):
        """Get count of black disks"""
        return self._black_count

    def __getitem__(self, coords):
        """Get disk from field."""
        return self._skeleton[coords[0]][coords[1]]

    def __setitem__(self, coords, color):
        """Set disk on the field and inc score."""
        self._skeleton[coords[0]][coords[1]] = color
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

    def __iter__(self):
        """Iter trough the field."""
        return self._skeleton.__iter__()
