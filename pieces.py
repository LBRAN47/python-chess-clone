from constants import *
from abc import ABC, abstractmethod

class Piece():

    def __init__(self, position: tuple[int], color: bool):
        for coord in position:
            if coord < 1 or coord > 8:
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
    def can_move(self, square: tuple[int]) -> bool:
        if self.get_position() == square:
            return False
        for coord in square:
            if coord < 1 or coord > 8:
                return False
        return True

class Pawn(Piece):

    def __init__(self, position: tuple[int], color: bool):

        super().__init__(position, color)
        self._has_moved = False
        
        if self._color == WHITE:
            if self._position[1] != 2:
               raise Exception("White Pawns must begin in row 2")
        else:
            if self._position[1] != 7:
               raise Exception("Black Pawns must begin in row 7")

    def has_moved(self) -> bool:
        return self._has_moved

    def can_move(self, square: tuple[int]) -> bool:
        if not super().can_move(square):
            return False
        diff = (square[0] - self.get_position()[0],  square[1] - self.get_position()[1])
        
        #ensure pawn moves forward only one square
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

        if diff[0] != -1 and diff[0] != 0 and diff[0] != 1:
            return False
        return True

class Bishop(Piece):

    def __init__(self, position: tuple[int], color: bool):
        super().__init__(position, color)


    def can_move(self, square: tuple[int]) -> bool:
        if not super().can_move(square):
            return False
        return abs(square[0] - self.get_position()[0]) == abs(square[1] - self.get_position()[1])

class Rook(Piece):

    def __init__(self, position: tuple[int], color: bool):
        super().__init__(position, color)
        self._has_moved = False

    def has_moved(self) -> bool:
        return self._has_moved

    def can_move(self, square: tuple[int]) -> bool:
        if not super().can_move(square):
            return False
        return (self.get_position()[0] == square[0] or self.get_position()[1] == square[1])

class Queen(Piece):

    def __init__(self, position: tuple[int], color: bool):
        super().__init__(position, color)
        self.rook = Rook(position, color)
        self.bishop = Bishop(position, color)

    def can_move(self, square: tuple[int]) -> bool:
        if not super().can_move(square):
            return False
        if self.rook.can_move(square) or self.bishop.can_move(square):
            return True
        return False
 
class King(Piece):

    def __init__(self, position: tuple[int], color: bool):
        if color == WHITE and position != (5, 1):
            raise Exception("King must start on the right starting square")
        if color == BLACK and position != (5, 8):
            raise Exception("King must start on the right starting square")

        super().__init__(position, color)
        self._has_moved = False

    def has_moved(self) -> bool:
        return self._has_moved

    def can_move(self, square: tuple[int]) -> bool:
        if not super().can_move(square):
            return False
        diff = (square[0] - self.get_position()[0], square[1] - self.get_position()[1])
        #exception for castling
        if not self.has_moved() and diff == (2, 0) or diff == (-2, 0):
            return True
        return not(abs(diff[0]) > 1 or abs(diff[1]) > 1)
    
