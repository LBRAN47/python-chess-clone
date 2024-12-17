from constants import *
from abc import ABC, abstractmethod
from typing import override

class Piece():

    def __init__(self, position: tuple[int], color: bool):
        for coord in position:
            if coord < 0  or coord > 7:
                raise Exception(f"{self.__class__.__name__} must be in the board") 
        self._position = position
        self._color = color
        


    def get_position(self) -> tuple[int]:
        return self._position

    def get_color(self) -> bool:
        return self._color
    
    def set_position(self, position: tuple[int]):
        self._position = position

    @abstractmethod
    def can_move(self, square: tuple[int], board) -> bool:
        if self.get_position() == square:
            return False
        for coord in square:
            if coord < 0  or coord > 7:
                return False
        col, row = square
        if board[row][col] is not None and board[row][col].get_color() == self.get_color():
            return False
        return True

    def get_delta(self, diff: tuple[int]) -> tuple[int]:
        dx = 0 if diff[0] == 0 else (1 if diff[0] > 0 else -1)
        dy = 0 if diff[1] == 0 else (1 if diff[1] > 0 else -1)
        return (dx, dy)

    def __str__(self) -> str:
        return self.__class__.__name__[0]

    def get_filename(self) -> str:
        col = "B" if self.get_color() == BLACK else "W"
        return str(self) + col + ".png"

    def move_piece(self, new: tuple[int]):
        self._position = new

class Pawn(Piece):

    def __init__(self, position: tuple[int], color: bool):

        super().__init__(position, color)
        self._has_moved = False
        
        if self._color == WHITE:
            if self._position[1] != 1:
               raise Exception("White Pawns must begin in row 2")
        else:
            if self._position[1] != 6:
               raise Exception("Black Pawns must begin in row 7")

    def has_moved(self) -> bool:
        return self._has_moved

    def can_move(self, square: tuple[int], board: list[list[Piece]]) -> bool:
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
            if board[row][col] is None or board[row][col].get_color() == self.get_color():
                return False
        else:
            return False

        return True
    
    def get_valid_moves(self, board: list[list[Piece]]) -> list[tuple[int]]:
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

    def __init__(self, position: tuple[int], color: bool):
        super().__init__(position, color)


    def can_move(self, square: tuple[int], board: list[list[Piece]]) -> bool:
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

    def get_valid_moves(self, board: list[list[Piece]]) -> list[tuple[int]]:
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

    def __init__(self, position: tuple[int], color: bool):
        super().__init__(position, color)
        self._has_moved = False

    def has_moved(self) -> bool:
        return self._has_moved

    def can_move(self, square: tuple[int], board: list[list[Piece]]) -> bool:
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

    def get_valid_moves(self, board: list[list[Piece]]) -> list[tuple[int]]:
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

    def __init__(self, position: tuple[int], color: bool):
        super().__init__(position, color)
        self.rook = Rook(position, color)
        self.bishop = Bishop(position, color)

    def can_move(self, square: tuple[int], board: list[list[Piece]]) -> bool:
        if not super().can_move(square, board):
            return False
        if self.rook.can_move(square, board) or self.bishop.can_move(square, board):
            return True
        return False

    @override
    def move_piece(self, new: tuple[int]):
        self.rook._position = new
        self.bishop._position = new

    def get_valid_moves(self, board: list[list[Piece]]) -> list[tuple[int]]:
        return self.rook.get_valid_moves(board) + self.bishop.get_valid_moves(board)
    
 
class King(Piece):

    def __init__(self, position: tuple[int], color: bool):
        if color == WHITE and position != (4, 0):
            self._has_moved = True
        elif color == BLACK and position != (4, 7):
            self._has_moved = True
        else:
            self._has_moved = False
        super().__init__(position, color)

    def has_moved(self) -> bool:
        return self._has_moved

    def can_move(self, square: tuple[int], board: list[list[Piece]]) -> bool:
        if not super().can_move(square, board):
            return False
        diff = (square[0] - self.get_position()[0], square[1] - self.get_position()[1])
        #exception for castling
        if not self.has_moved() and diff == (2, 0) or diff == (-2, 0):
            return True
        return not(abs(diff[0]) > 1 or abs(diff[1]) > 1)
    @override
    def move_piece(self, new: tuple[int]) -> None:
        self._position = new
        self._has_moved = True

    def get_valid_moves(self, board: list[list[Piece]]) -> list[tuple[int]]:
        ans = []
        for direction in [(0, 1), (1, 1), (-1, 1), (1, 0), (-1, 0), (0, -1), (1, -1), (-1, -1)]:
            pos = tuple(a + b for a, b in zip(self.get_position(), direction))
            if self.can_move(pos, board):
                ans.append(pos)
        return ans



    
class Knight(Piece):

    
    def __init__(self, position: tuple[int], color: bool):
        super().__init__(position, color)

    def can_move(self, square: tuple[int], board: list[list[Piece]]) -> bool:
        if not super().can_move(square, board):
            return False
        diff = (abs(square[0] - self.get_position()[0]), abs(square[1] - self.get_position()[1]))
        return (diff[0] == 2 and diff[1] == 1) or (diff[0] == 1 and diff[1] == 2)
    
    def get_valid_moves(self, board: list[list[Piece]]) -> list[tuple[int]]:
        ans = []
        for direction in [(-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1)]:
            pos = tuple(a + b for a, b in zip(self.get_position(), direction))
            if self.can_move(pos, board):
                ans.append(pos)
        return ans

    def __str__(self) -> str:
        return "N"


        
        
        















