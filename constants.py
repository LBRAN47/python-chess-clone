from board import *
WHITE = True
BLACK = False
COLUMN_LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
COLUMNS = {"a" : 0, "b" : 1, "c" : 2, "d" : 3, "e" : 4, "f" : 5, "g" : 6, "h" : 7}


GREEN = (119, 149, 86)
CREAM = (235, 236, 208)
COLORS = [GREEN, CREAM]
GREY = (164, 164, 164)
DARK_GREY = (100, 100, 100)
SQUARE_LENGTH = 64
BOARD_POSITION = (0, 0) #top left corner of the board

VALID_MOVE_RADIUS = SQUARE_LENGTH // 8

SELECT_BOX_LENGTH = 50
INNER_BOX_LENGTH = 38

WHITE_PROMOTION_PIECES = [Queen((0, 0), WHITE),
                          Rook((0, 0), WHITE), Bishop((0, 0), WHITE), Knight((0, 0), WHITE)]
BLACK_PROMOTION_PIECES = [Queen((0, 0), BLACK),
                          Rook((0, 0), BLACK), Bishop((0, 0), BLACK), Knight((0, 0), BLACK)]
