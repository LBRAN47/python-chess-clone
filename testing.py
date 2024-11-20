from pieces import Pawn, Bishop, Rook, Queen, King, Knight
from constants import *
from board import *

board = Board(None)
print(board)
board.move_piece((1, 1), (1, 3))
board.move_piece((2, 6), (2, 4))
board.move_piece((2, 4), (1, 3))
board.move_piece((1, 3), (1, 2))
board.move_piece((1, 2), (1, 1))
board.move_piece((1, 1), (0, 0))
print(board)


