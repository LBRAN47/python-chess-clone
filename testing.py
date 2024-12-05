from pieces import Pawn, Bishop, Rook, Queen, King, Knight
from constants import *
from board import *

import time

board = Board()
print(board)
board.move_piece((1, 1), (1, 3))
board.move_piece((2, 6), (2, 4))
board.move_piece((2, 4), (1, 3))
board.move_piece((1, 3), (1, 2))
board.move_piece((1, 2), (1, 1))
board.move_piece((1, 1), (0, 0))
print(board)

board = Board()

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

board = Board()

my_board = board.get_board()
for row in my_board:
    for square in row:
        if square is None:
            continue
        print(f"Piece: {square}, position: {square.get_position()}\nPossible Moves: {square.get_valid_moves(my_board)}")

print("=====================")
print("new game")
print("=====================")

while True:
    move = input("enter 4 numbers representing the move e.g. 1214\n")
    board.move_piece((int(move[0]),int(move[1])), (int(move[2]), int(move[3])))
    print(board)
    time.sleep(0.1)
