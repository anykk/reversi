from src.tile import *
import pprint


class Board(object):
    """docstring"""
    def __init__(self, board_size):
        self.board_size = board_size
        self.board = [[Tile((x, y), EMPTY) for x in range(self.board_size)] for y in range(self.board_size)]
        self[self.board_size // 2 - 1, self.board_size // 2 - 1] = WHITE
        self[self.board_size // 2 - 1, self.board_size // 2] = BLACK
        self[self.board_size // 2, self.board_size // 2 - 1] = BLACK
        self[self.board_size // 2, self.board_size // 2] = WHITE

    def is_correct_move(self, player, coordinates):
        if self[coordinates].color is not None and not self.in_range(coordinates):
            return False

        to_flip = []
        other = get_opponent(player)
        for dx, dy in DIRECTIONS:
            x, y = coordinates
            x += dx
            y += dy

            if self.in_range((x, y)) and self[x, y].color == other:
                x += dx
                y += dy

                while self.in_range((x, y)) and self[x, y].color == other:
                    x += dx
                    y += dy
                if self[x, y].color == player:
                    while (x, y) != coordinates:
                        x -= dx
                        y -= dy
                        if (x, y) == coordinates:
                            break
                        to_flip.append(self[x, y])
        return to_flip if to_flip else False

    def get_correct_moves(self, player):
        correct_moves = []

        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.is_correct_move(player, (x, y)):
                    correct_moves.append(self[x, y])
        return correct_moves

    def in_range(self, coordinates):
        return 0 <= coordinates[0] < self.board_size and 0 <= coordinates[1] < self.board_size

    def __getitem__(self, coordinates):
        return self.board[coordinates[0]][coordinates[1]]

    def __setitem__(self, coordinates, color):
        self.board[coordinates[0]][coordinates[1]] = Tile(tuple(reversed(coordinates)), color)

    def __repr__(self):
        repr_ = []
        for row in self:
            for col in row:
                repr_.append(str(col))
            repr_.append('\n')
        return ''.join(repr_)

    def __iter__(self):
        return self.board.__iter__()


if __name__ == '__main__':
    b = Board(8)
    print(list(map(lambda x: x.coordinates, b.get_correct_moves(WHITE))))