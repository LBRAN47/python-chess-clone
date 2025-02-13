# A coordinate in the window, representing an x and y position.
type Coordinate = tuple[int, int]
# A coordinate in the board, representing a 0-indexed collum and row position.
type BoardCoordinate = tuple[int, int]

# boolean representations of the WHITE and BLACK players
WHITE = True
BLACK = False
#mapping of collumn letters typical in chess noation to a 0-indexed collumn number.
COLUMN_LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
COLUMNS = {"a" : 0, "b" : 1, "c" : 2, "d" : 3,
           "e" : 4, "f" : 5, "g" : 6, "h" : 7}

# the Exit Codes for the game loop
END_GAME = 0
WHITE_CHECKMATE = 1
BLACK_CHECKMATE = 2
STALEMATE = 3


GREEN = (119, 149, 86)
CREAM = (235, 236, 208)
COLORS = [CREAM, GREEN]
GREY = (164, 164, 164)
DARK_GREY = (100, 100, 100)
SQUARE_LENGTH = 80
SCREEN_SIZE = 8*SQUARE_LENGTH
BOARD_POSITION = (0, 0) #top left corner of the board

VALID_MOVE_RADIUS = SQUARE_LENGTH // 8

SELECT_BOX_LENGTH = SQUARE_LENGTH * 0.8
INNER_BOX_LENGTH = SQUARE_LENGTH * 0.6
GAME_OVER_BOX_WIDTH = 4*SQUARE_LENGTH
GAME_OVER_BOX_HEIGHT = 3*SQUARE_LENGTH
GAME_OVER_BUTTON_WIDTH = 2*SQUARE_LENGTH
GAME_OVER_BUTTON_HEIGHT = SQUARE_LENGTH // 1.5

