from src.utility import *


class Tile(object):
    """docstring"""
    def __init__(self, coordinates=(None, None), color=None):
        self.color = color
        self.coordinates = coordinates

    def flip(self):
        self.color = int(not self.color)

    def __repr__(self):
        if self.color is not None:
            return 'O' if self.color == WHITE else "X"
        return '.'
