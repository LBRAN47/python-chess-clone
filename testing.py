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

board = Board(None)

board.move_piece((3, 1), (3, 3))
board.move_piece((2, 0), (5, 3))
board.move_piece((4, 1), (4, 2))
board.move_piece((4, 6), (4, 4))
board.move_piece((5, 3), (4, 4))
board.move_piece((4, 4), (3, 3))
board.move_piece((5, 0), (3, 2))
board.move_piece((5, 7), (3, 5))
board.move_piece((3, 5), (2, 6))


print(board)

