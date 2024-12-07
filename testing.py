from pieces import Pawn, Bishop, Rook, Queen, King, Knight
from constants import *
from board import *

import time

"""
takes in the input of the user, which must be in the form "charintcharint" e.g. "d4e5".
returns a list of two tuples, the coordinates of the piece to move, and the target square.
"""
def interpreter(text: str) -> list[tuple[int]]:
    
    if len(text) != 4:
        print("text must be of length 4\n")
        return
    pos = text[0:2]
    target = text[2:]
    squares = []
    for coord in [pos, target]:
        if coord[0] not in COLUMNS.keys() or not coord[1].isdigit() or int(coord[1]) not in range(1, 9):
            print(f"{coord} is not a letter followed by a number\n")
            return
        col = COLUMNS[coord[0]]
        row = int(coord[1]) - 1
        squares.append((col, row))
    return squares

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
    move = input("enter 4 characters representing the move e.g. e2e4\n")
    move = interpreter(move)
    if move is None:
        continue
    pos, target = move
    board.move_piece(pos, target)
    print(board)
    if board.in_checkmate():
        color = "white" if board.get_turn() != WHITE else "black"
        print(f"Game Over! {color} wins by checkmate!")
        break
    time.sleep(0.1)
    
