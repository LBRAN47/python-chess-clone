from abc import abstractmethod
from typing import override
from constants import (WHITE, BLACK, BoardCoordinate)

"""
A bass class to represent a chess piece, from which all chess pieces (Pawn,
Bishop, Knight, Rook, Queen, King) all inherit. Contains the logic that is 
common to all pieces, including all getters and setters, plus a method 
which performs some legality checks for piece movement, which can be
overloaded in the child to check for rules of that specific piece. There
is one abstract method, get_valid_moves, which must be implemented by child
classes.
"""
class Piece():

    """
    Sets the position and color of this piece, checking the position is within
    the 8x8 chess board.
    args:
        position : a BoardCoordinate that the piece is initially placed
        color : WHITE or BLACK, the color of the peice
    """
    def __init__(self, position: BoardCoordinate, color: bool):
        for coord in position:
            if coord < 0  or coord > 7:
                raise Exception(f"{self.__class__.__name__} must be in the board") 
        self._position = position
        self._color = color
        


    """
    Returns the current board position of the piece
    """
    def get_position(self) -> BoardCoordinate:
        return self._position

    """
    Returns the color of the piece
    """
    def get_color(self) -> bool:
        return self._color
    
    """
    sets the position of the piece
    args:
        position : the BoardCoordinate for the piece to be placed.
    """
    def set_position(self, position: BoardCoordinate):
        self._position = position

    """
    Returns True if the following are True:
        1. The square is different from the piece's position
        2. The square is inside the board
        3. the square is either empty or contains a piece of the opposite color
    And returns False otherwise.
    In essence, this method checks the legalities common to all pieces when
    checking if a move is legal.
    args :
        square : the BoardCoordinate to move the piece to.
        board : a 2D list representing the board state. 
    """
    def can_move(self, square: BoardCoordinate, board) -> bool:
        if self.get_position() == square:
            return False
        for coord in square:
            if coord < 0  or coord > 7:
                return False
        col, row = square
        if board[row][col] is not None and board[row][col].get_color() == self.get_color():
            return False
        return True


    """
    returns a BoardCoordinate 'delta' based on the diff, where diff is a
    BoardCoordinate that represents a move relative to a starting position.
    e.g. (1, 2) represents moving 1 square to the right and 2 squares up.
    a delta is essentially a unit vector represents the direction of the move.
    e.g. (4, -4) has a delta of (1, -1), which represents bottom-right diagonal
    move.
    args:
        diff : a 2D vector representing a move from one square to another
    """
    def get_delta(self, diff: BoardCoordinate) -> BoardCoordinate:
        dx = 0 if diff[0] == 0 else (1 if diff[0] > 0 else -1)
        dy = 0 if diff[1] == 0 else (1 if diff[1] > 0 else -1)
        return (dx, dy)

    """
    Returns the string representation of this object instance, which is
    simply the first letter of its name.
    """
    def __str__(self) -> str:
        return self.__class__.__name__[0]

    """
    Returns the filename of the piece's image in this project.
    """
    def get_filename(self) -> str:
        col = "B" if self.get_color() == BLACK else "W"
        return str(self) + col + ".png"

    """
    Same as set_position, but is intended to be overloaded by certain child
    classes to also keep track of whether that piece has moved before.
    so set_position simply sets the position of the piece, wheras move_piece
    performs a move in the context of the chess game.
    """
    def move_piece(self, new: BoardCoordinate):
        self.set_position(new)

    """
    abstract method which retunrs a list of BoardCoordinates that the piece
    can legally move to.
    """
    @abstractmethod
    def get_valid_moves(self, board) -> list[BoardCoordinate]:
        pass
    
class Pawn(Piece):

    def __init__(self, position: BoardCoordinate, color: bool):

        super().__init__(position, color)
        self._has_moved = False
        self._just_moved = False
        
        if self._color == WHITE:
            if self._position[1] != 1:
               raise Exception("White Pawns must begin in row 2")
        else:
            if self._position[1] != 6:
               raise Exception("Black Pawns must begin in row 7")

    def has_moved(self) -> bool:
        return self._has_moved

    def has_just_moved(self) -> bool:
        return self._just_moved

    @override
    def can_move(self, square: BoardCoordinate, board: list[list[Piece]]) -> bool:
        if not super().can_move(square, board):
            return False
        diff = (square[0] - self.get_position()[0],  square[1] - self.get_position()[1])
        col, row = square
        position = self.get_position()
        direction = self.get_delta(diff)
        
        if self.get_color() == WHITE:
            if diff[1] != 1 and diff[1] != 2:

                return False
            if diff[1] != 1 and self.has_moved():
                return False
        else:
            if diff[1] != -1 and diff[1] != -2:
                return False
            if diff[1] != -1 and self.has_moved():
                return False
        if diff[0] == 0:
            while position != square:
                position = (position[0] + direction[0], position[1] + direction[1])
                if board[position[1]][position[0]] is not None:
                    return False

        elif diff[0] == -1 or diff[0] == 1:
            side_piece = board[position[1]][col]
            if self.enpessant(side_piece):
                return True
            elif board[row][col] is None or board[row][col].get_color() == self.get_color():
                return False
        else:
            return False

        return True

    def enpessant(self, side_piece: Piece | None) -> bool:
        return side_piece is not None and isinstance(side_piece, Pawn) and\
                side_piece.get_color() != self.get_color() and side_piece.has_just_moved()

    @override
    def move_piece(self, new: BoardCoordinate):
        diff = (new[0] - self.get_position()[0], new[1] - self.get_position()[1])
        self._position = new
        if not self._has_moved and abs(diff[1]) == 2:
            self._just_moved = True
        self._has_moved = True
    
    @override
    def get_valid_moves(self, board: list[list[Piece]]) -> list[BoardCoordinate]:
        ans = []
        pos = self.get_position()
        if self.get_color() == WHITE:
            directions = [(0, 1), (0, 2), (1, 1), (-1, 1)]
        else:
            directions =  [(0, -1), (0, -2), (1, -1), (-1, -1)]
        moves = []
        for direction in directions:
            moves.append(tuple(a + b for a, b in zip(direction, pos)))

        for move in moves:
            if self.can_move(move, board):
                ans.append(move)
        return ans


        

class Bishop(Piece):

    def __init__(self, position: BoardCoordinate, color: bool):
        super().__init__(position, color)


    @override
    def can_move(self, square: BoardCoordinate, board: list[list[Piece]]) -> bool:
        if not super().can_move(square, board):
            return False
        diff = (square[0] - self.get_position()[0],  square[1] - self.get_position()[1])
        col, row = square
        position = self.get_position()
        direction = self.get_delta(diff)
        if  abs(diff[0]) != abs(diff[1]):
            return False
        while position != square:
            position = (position[0] + direction[0], position[1] + direction[1])
            if position == square:
                continue
            if board[position[1]][position[0]] is not None:
                return False
        if board[row][col] is not None and board[row][col].get_color() == self.get_color():
            return False
        return True

    @override
    def get_valid_moves(self, board: list[list[Piece]]) -> list[BoardCoordinate]:
        ans = []
        moves = []
        pos = self.get_position()
        mov = pos
        for direction in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            mov = tuple(a + b for a, b in zip(direction, mov))
            while mov[0] <= 7 and mov[0] >= 0 and mov[1] <= 7 and mov[1] >= 0:
                moves.append(mov)
                mov = tuple(a + b for a, b in zip(direction, mov))
            mov = pos
        for move in moves:
            if self.can_move(move, board):
                ans.append(move)
        return ans



class Rook(Piece):

    def __init__(self, position: BoardCoordinate, color: bool):
        super().__init__(position, color)
        self._has_moved = False

    def has_moved(self) -> bool:
        return self._has_moved

    @override
    def can_move(self, square: BoardCoordinate, board: list[list[Piece]]) -> bool:
        if not super().can_move(square, board):
            return False
        diff = (square[0] - self.get_position()[0],  square[1] - self.get_position()[1])
        col, row = square
        position = self.get_position()
        direction = self.get_delta(diff)
        if not (self.get_position()[0] == square[0] or self.get_position()[1] == square[1]):
            return False
        while position != square:
            position = (position[0] + direction[0], position[1] + direction[1])
            if position == square:
                continue
            if board[position[1]][position[0]] is not None:
                return False
        if board[row][col] is not None and board[row][col].get_color() == self.get_color():
            return False
        return True

    @override
    def get_valid_moves(self, board: list[list[Piece]]) -> list[BoardCoordinate]:
        ans = []
        moves = []
        pos = self.get_position()
        mov = pos
        for direction in [(0, 1), (0, -1), (-1, 0), (1, 0)]:
            mov = tuple(a + b for a, b in zip(direction, mov))
            while mov[0] <= 7 and mov[0] >= 0 and mov[1] <= 7 and mov[1] >= 0:
                moves.append(mov)
                mov = tuple(a + b for a, b in zip(direction, mov))
            mov = pos
        for move in moves:
            if self.can_move(move, board):
                ans.append(move)
        return ans

class Queen(Piece):

    def __init__(self, position: BoardCoordinate, color: bool):
        super().__init__(position, color)
        self.rook = Rook(position, color)
        self.bishop = Bishop(position, color)
        self._position = position

    @override
    def can_move(self, square: BoardCoordinate, board: list[list[Piece]]) -> bool:
        if not super().can_move(square, board):
            return False
        if self.rook.can_move(square, board) or self.bishop.can_move(square, board):
            return True
        return False

    @override
    def move_piece(self, new: BoardCoordinate):
        self.rook._position = new
        self.bishop._position = new
        self._position = new

    @override
    def get_valid_moves(self, board: list[list[Piece]]) -> list[BoardCoordinate]:
        return self.rook.get_valid_moves(board) + self.bishop.get_valid_moves(board)
    
 
class King(Piece):

    def __init__(self, position: BoardCoordinate, color: bool):
        if color == WHITE and position != (4, 0):
            self._has_moved = True
        elif color == BLACK and position != (4, 7):
            self._has_moved = True
        else:
            self._has_moved = False
        super().__init__(position, color)

    def has_moved(self) -> bool:
        return self._has_moved

    @override
    def can_move(self, square: BoardCoordinate, board: list[list[Piece]]) -> bool:
        if not super().can_move(square, board):
            return False
        diff = (square[0] - self.get_position()[0], square[1] - self.get_position()[1])
        #exception for castling
        if not self.has_moved() and diff == (2, 0) or diff == (-2, 0):
            return True
        return not(abs(diff[0]) > 1 or abs(diff[1]) > 1)

    def castle(self, rook: Rook, board: list[list[Piece | None]]):
        #move rook
        rook_x, rook_y = rook.get_position()
        new_x = 3 if rook_x == 0 else 5
        board[rook_y][rook_x] = None
        board[rook_y][new_x] = rook
        rook.set_position((new_x, rook_y))
        
        #move king
        king_x, king_y = self.get_position()
        new_x = 2 if king_x == 0 else 6
        board[king_y][king_x] = None
        board[king_y][new_x] = self
        self.move_piece((new_x, king_y))


    @override
    def move_piece(self, new: BoardCoordinate) -> None:
        self._position = new
        self._has_moved = True

    @override
    def get_valid_moves(self, board: list[list[Piece]]) -> list[BoardCoordinate]:
        ans = []
        for direction in [(0, 1), (1, 1), (-1, 1), (1, 0), (-1, 0), (0, -1), (1, -1), (-1, -1)]:
            pos = tuple(a + b for a, b in zip(self.get_position(), direction))
            if self.can_move(pos, board):
                ans.append(pos)
        return ans



    
class Knight(Piece):

    
    def __init__(self, position: BoardCoordinate, color: bool):
        super().__init__(position, color)
    
    @override
    def can_move(self, square: BoardCoordinate, board: list[list[Piece]]) -> bool:
        if not super().can_move(square, board):
            return False
        diff = (abs(square[0] - self.get_position()[0]), abs(square[1] - self.get_position()[1]))
        return (diff[0] == 2 and diff[1] == 1) or (diff[0] == 1 and diff[1] == 2)
    
    @override
    def get_valid_moves(self, board: list[list[Piece]]) -> list[BoardCoordinate]:
        ans = []
        for direction in [(-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1)]:
            pos = tuple(a + b for a, b in zip(self.get_position(), direction))
            if self.can_move(pos, board):
                ans.append(pos)
        return ans

    @override
    def __str__(self) -> str:
        return "N"


        
        
        















