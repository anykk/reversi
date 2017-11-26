EMPTY = None
WHITE = 0
BLACK = 1

DIRECTIONS = ((0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1))


def get_opponent(player):
    if player == WHITE:
        return BLACK
    elif player == BLACK:
        return WHITE
    else:
        raise ValueError
