from constants import *
from pieces import *
class Board():

    def __init__(board: list[list[Piece]] | None):
        if board is not None:
            self._board = board
        else: #make regular board
            self._board = []
            for i in range(0, 8):
                row = []
                if i == 1 or i == 6:
                    color = WHITE if i == 1 else BLACK
                    for j in range(0, 8):
                        row.append(Pawn((j, i), color))
                    self._board.append(row)
                elif i == 0 or i == 7:
                    color = WHITE if i == 0 else BLACK
                    row.append(Rook((0, i), color))
                    row.append(Knight((1, i), color))
                    row.append(Bishop((2, i), color))
                    row.append(Queen((3, i), color))
                    row.append(King((4, i), color))
                    row.append(Bishop((5, i), color))
                    row.append(Knight((6, i), color))
                    row.append(Rook((7, i), color))
                    board.append(row)
