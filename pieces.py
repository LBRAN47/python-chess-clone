import constants
from abc import ABC, abstractmethod

class Piece():

    def __init__(self, position: tuple[int], color: bool):
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
        pass

class Pawn(Piece):

    def __init__(self, position: tuple[int], color: bool):

        super().__init__(self, position, color)
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
        for coord in square:
            if coord < 1 or coord > 8:
                return False

        diff = (square[0] - self.get_position[0],  square[1] - self.get_position[1])

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

            

                


