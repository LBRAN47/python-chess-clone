from constants import *
from pieces import *

def coord_to_square(coord: tuple[int]) -> str | None:
    if len(coord) != 2:
        print("coord must be a coordinate\n")
        return None
    ans = ''
    num = coord[0]
    for let in COLUMN_LETTERS:
        if COLUMNS[let] == num:
            ans += let
    ans += str(coord[1] + 1)
    return ans


class Board():

    def __init__(self, board: list[list[Piece]] | None = None):
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
                            self.wking_position = square.get_position()
                        else:
                            if black_king:
                                raise Exception("only one King per side")
                            black_king = True
                            self.bking_position = square.get_position()
            if not white_king or not black_king:
                raise Exception("Each side must have one King")
            self._board = board
        else: #make regular board
            self._board = self.construct_board()
            self.wking_position = (4, 0)
            self.bking_position = (4, 7)

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
        position = self.wking_position if player == WHITE else self.bking_position
        for row in self.get_board():
            for square in row:
                if square is None:
                    continue
                if square.get_color() != player and position in square.get_valid_moves(self.get_board()):
                    return True
        return False

    def can_castle(self, piece: King, target: tuple[int]) -> bool:
        position = piece.get_position()
        origin = position
        diff = (target[0] - position[0], target[1] - position[1])
        direction = piece.get_delta(diff)
        iteration = 1
        while True:
            position = (position[0] + direction[0], position[1] + direction[1])
            square = self._board[position[1]][position[0]]
            if square is not None and isinstance(square, Rook) and not square.has_moved() and\
            square.get_color() == piece.get_color():
                x_pos, y_pos  = square.get_position()
                new_x = 3 if x_pos == 0 else 5
                self._board[y_pos][x_pos] = None
                self._board[y_pos][new_x] = square
                square.set_position((new_x, y_pos))
                break
            if self._board[position[1]][position[0]] is not None:
                print(f"cannot castle due to piece blocking at {position}\n")
                return False
            if iteration <= 2:
                cur_pos = piece.get_position()
                self._board[cur_pos[1]][cur_pos[0]] = None
                self._board[position[1]][position[0]] = piece
                piece.set_position(position)
                if piece.get_color() == WHITE:
                    self.wking_position = position
                else:
                    self.bking_position = position
                if self.in_check(piece.get_color()):
                    self._board[origin[1]][origin[0]] = piece
                    self._board[position[1]][position[0]] = None
                    piece.set_position(origin)
                    print("got in check trying to move piece\n")
                    return False

            if  position[0] < 0 or position[0] > 7:
                print("reached the end\n")
                return False
            iteration += 1
        return True


    
    def move_piece(self, position: tuple[int], new: tuple[int]) -> None:
        piece = self.get_board()[position[1]][position[0]]
        if piece is None:
            print("no piece at position")
            return
        elif piece.get_color() != self.get_turn():
            color = "White" if self._turn == WHITE else "Black"
            print(f"tried to move {piece.__class__.__name__} at {coord_to_square(position)} but it is {color}'s turn")
            return
        else:
            if piece.can_move(new, self.get_board()):
                if isinstance(piece, King) and abs(position[0] - new[0]) == 2 and not self.can_castle(piece, new):
                    print(f"cannot castle bozo")
                    return
                target = self._board[new[1]][new[0]]
                piece.set_position(new)
                self._board[position[1]][position[0]] = None
                self._board[new[1]][new[0]] = piece
                if isinstance(piece, King):
                    if piece.get_color() == WHITE:
                        self.wking_position = new
                    else:
                        self.bking_position = new
                if self.in_check(self._turn):
                    piece.set_position(position)
                    piece._has_moved = False
                    self._board[position[1]][position[0]] = piece
                    self._board[new[1]][new[0]] = target
                    if isinstance(piece, King):
                        if piece.get_color() == WHITE:
                            self.wking_position = position
                        else:
                            self.bking_position = position
                    color = "White" if self._turn == WHITE else "Black"
                    print(f"illegal move: {color} King in check")
                    return
                if isinstance(piece, King):
                    if piece.get_color() == WHITE:
                        self.wking_position = new
                    else:
                        self.bking_position = new
                piece.move_piece(new)
                self.change_turn()
                return
            else:
                print(f"illegal move: {piece.__class__.__name__} at {coord_to_square(position)} to {coord_to_square(new)}")
                return

    def in_checkmate(self) -> bool:
        color =  self.get_turn()
        if not self.in_check(color):
            return False
        board = self.get_board()
        ans = True
        for row in board:
            for square in row:
                if square is None or square.get_color() != color:
                    continue
                for move in square.get_valid_moves(self._board):
                    target = self._board[move[1]][move[0]]
                    pos = square.get_position()
                    self._board[pos[1]][pos[0]] = None
                    self._board[move[1]][move[0]] = square
                    square.set_position(move)
                    if isinstance(square, King):
                        if color == WHITE:
                            self.wking_position = move
                        else:
                            self.bking_position = move
                    if not self.in_check(color):
                        ans = False
                    square.set_position(pos)
                    self._board[move[1]][move[0]] = target
                    self._board[pos[1]][pos[0]] = square
                    if isinstance(square, King):
                        if color == WHITE:
                            self.wking_position = pos
                        else:
                            self.bking_position = pos

        return ans







