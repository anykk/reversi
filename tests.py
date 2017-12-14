import unittest
from driver import *


class FieldTests(unittest.TestCase):
    """docstring for ModelTests"""

    def setUp(self):
        self.field = Field(8)

    def test_init(self):
        self.assertEqual(str(self.field).replace('\n', ''), '........'
                                                            '........'
                                                            '........'
                                                            '...OX...'
                                                            '...XO...'
                                                            '........'
                                                            '........'
                                                            '........')

    def test_error(self):
        with self.assertRaises(IllegalArgumentError):
            self.field = Field(3)

    def test_flip(self):
        self.field.flip((3, 3))
        self.assertEqual(self.field.white_count, 1)
        self.assertEqual(self.field.black_count, 3)
        self.assertEqual(self.field[3, 3], BLACK)
        with self.assertRaises(TypeError):
            self.field.flip((0, 0))

    def test_in_range(self):
        self.assertTrue(self.field.in_range((7, 7)))
        self.assertTrue(self.field.in_range((0, 5)))
        self.assertTrue(self.field.in_range((5, 3)))
        self.assertFalse(self.field.in_range((8, 7)))
        self.assertFalse(self.field.in_range((0, 8)))
        self.assertFalse(self.field.in_range((-1, 0)))

    def test_set_and_get(self):
        self.field[0, 0] = WHITE
        self.field[2, 3] = BLACK
        self.assertEqual(self.field.black_count, 3)
        self.assertEqual(self.field.white_count, 3)
        self.assertEqual(self.field[0, 0], WHITE)
        self.assertEqual(self.field[2, 3], BLACK)


class ReversiTests(unittest.TestCase):
    def setUp(self):
        self.reversi = Reversi()

    def test_correct_moves(self):
        self.assertEqual(self.reversi.get_correct_moves(), [(2, 3), (3, 2), (4, 5), (5, 4)])
        self.reversi.make_move((2, 3))
        self.assertEqual(self.reversi.get_correct_moves(), [(2, 2), (2, 4), (4, 2)])

    def test_game_over(self):
        self.reversi._field._skeleton = [['X' for _ in range(8)] for _ in range(8)]
        with self.assertRaises(GameOverException):
            self.reversi.next_player()

    def test_move_error(self):
        with self.assertRaises(MoveError):
            self.reversi.make_move((0, 0))


if __name__ == '__main__':
    unittest.main()
