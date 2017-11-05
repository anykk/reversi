from src.tile import *


class Board(object):
    """docstring"""
    def __init__(self):
        self.board = [[Tile((x, y)) for x in range(8)] for y in range(8)]
        self[3, 3] = Tile((3, 3), WHITE)
        self[3, 4] = Tile((3, 4), BLACK)
        self[4, 3] = Tile((4, 3), BLACK)
        self[4, 4] = Tile((4, 4), WHITE)

    def is_correct_move(self, player, coordinates):
        if self[coordinates].color != None and not self.is_on_board(coordinates):
            return False

        self[coordinates] = Tile(coordinates, player)
        opponent = get_opponent(player)

        tiles_to_flip = []
        for dx, dy in DIRECTIONS:
            x, y = coordinates
            x += dx
            y += dy
            if self.is_on_board((x, y)) and self[x, y].color == opponent:
                x += dx
                y += dy
                if not self.is_on_board((x, y)):
                    continue
                while self[x, y].color == opponent:
                    x += dx
                    y += dy
                    if not self.is_on_board((x, y)):
                        break
                if not self.is_on_board((x, y)):
                    continue
                if self[x, y].color == player:
                    while 1:
                        x -= dx
                        y -= dy
                        if x == coordinates[0] and y == coordinates[1]:
                            break
                        tiles_to_flip.append(self[x, y])

            self[coordinates] = Tile(coordinates)
            if len(tiles_to_flip) == 0:
                return False
            return

    def get_correct_moves(self, player):
        valid_moves = []

        for x in range(8):
            for y in range(8):
                if self.is_correct_move(player, (x, y)) != False:
                    valid_moves.append(self[x, y])
        return valid_moves

    @staticmethod
    def is_on_board(coordinates):
        return 0 <= coordinates[0] <= 7 and 0 <= coordinates[1] <= 7

    def __getitem__(self, coordinates):
        return self.board[coordinates[1]][coordinates[0]]

    def __setitem__(self, coordinates, value):
        self.board[coordinates[1]][coordinates[0]] = value

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
    board = Board()
    print(board)
