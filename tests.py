import unittest
from board import *


class BoardTests(unittest.TestCase):
	"""docstring for ModelTests"""
	def setUp(self):
		self.board = Board()

	def test_init(self):
		self.assertEqual(str(self.board), '........\n........\n........\n...OX...\n...XO...\n........\n........\n........\n')

	def test_pass(self):
		pass

if __name__ == '__main__':
	unittest.main()