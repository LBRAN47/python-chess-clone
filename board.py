from constants import *
from pieces import *
class Board():

    def __init__(self, board: list[list[Piece]] | None):
        if board is not None:
            if len(board) != 8:
                raise Exception("board must have 8 rows")
            white_king = False
            black_king = False
            for row in board:
                if len(row) != 8:
                    raise Exception("board must have 8 columns")
                for square in row:
                    if square is not None and isinstance(square, King):
                        if square.get_color() == WHITE:
                            if white_king:
                                raise Exception("only one King per side")
                            white_king = True
                            self._wking_position = square.get_position()
                        else:
                            if black_king:
                                raise Exception("only one King per side")
                            black_king = True
                            self._bking_position = square.get_position()
            if not white_king or not black_king:
                raise Exception("Each side must have one King")
            self._board = board
        else: #make regular board
            self._board = self.construct_board()
            self._wking_position = (5, 0)
            self._bking_posiiton = (5, 7)

        self._turn = WHITE

    
    def get_board(self) -> list[list[Piece]]:
        return self._board

    def get_turn(self) -> bool:
        return self._turn

    def change_turn(self) -> None:
        self._turn = WHITE if self._turn == BLACK else BLACK


    def construct_board(self) -> list[list[Piece]]:
        board = []
        for i in range(0, 8):
            row = []
            if i == 1 or i == 6:
                color = WHITE if i == 1 else BLACK
                for j in range(0, 8):
                    row.append(Pawn((j, i), color))
                board.append(row)
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
            else:
                for j in range(8):
                    row.append(None)
                board.append(row)
        return board


    def __str__(self) -> str:
        ans = ""
        for i in range(7, -1, -1):
            row = self._board[i]
            for square in row:
                ans += "|"
                if square is None:
                    ans += " "
                else:
                    ans += str(square)
            ans += "|\n"
        return ans

    def in_check(self, player: bool) -> bool:

        pass

    

