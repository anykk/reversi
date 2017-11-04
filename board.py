from enum import Enum


class Color(Enum):
	WHITE = 0
	BLACK = 1

class Tile(object):
	"""docstring"""
	def __init__(self, color):
		self.color = color

	def __repr__(self):
		if self.color is not None:
			return 'O' if self.color == Color.WHITE else "X" 
		return '.'

class Board(object):
	"""docstring"""
	def __init__(self):
		self.board = [[Tile(None) for _ in range(8)] for _ in range(8)]
		self[3, 3] = Tile(Color(0))
		self[3, 4] = Tile(Color(1))
		self[4, 3] = Tile(Color(1))
		self[4, 4] = Tile(Color(0))

	def __getitem__(self, coordinates):
		return self.board[coordinates[0]][coordinates[1]]

	def __setitem__(self, coordinates, value):
		self.board[coordinates[0]][coordinates[1]] = value
	
	def __repr__(self):
		repr_ = []
		for row in self.board:
			for col in row:
				repr_.append(str(col))
			repr_.append('\n')
		return ''.join(repr_)
