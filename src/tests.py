import unittest

from game import *


class BoardTests(unittest.TestCase):
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

    def test_flip(self):
        self.field.flip((3, 3))
        self.assertEqual(self.field._white_count, 1)
        self.assertEqual(self.field._black_count, 3)
        self.assertEqual(self.field[3, 3], BLACK)
        with self.assertRaises(TypeError):
            self.field.flip((0, 0))


if __name__ == '__main__':
    unittest.main()
