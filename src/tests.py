import unittest

from src.board import *


class BoardTests(unittest.TestCase):
    """docstring for ModelTests"""

    def setUp(self):
        self.board = Board(8)

    def test_init(self):
        self.assertEqual(str(self.board).replace('\n', ''), '........'
                                                            '........'
                                                            '........'
                                                            '...OX...'
                                                            '...XO...'
                                                            '........'
                                                            '........'
                                                            '........')


class TileTests(unittest.TestCase):
    """docstring"""

    def setUp(self):
        self.tile = Tile()

    def test_init(self):
        self.assertEqual(self.tile.color, None)

    def test_flip(self):
        self.tile = Tile(BLACK)
        self.tile.flip()
        self.assertEqual(self.tile.color, WHITE)


if __name__ == '__main__':
    unittest.main()
