from pieces import Piece, Pawn, Bishop, Knight, Rook, Queen, King
from constants import (COLUMN_LETTERS, COLUMNS, WHITE, BLACK, Coordinate,
                       BoardCoordinate)
import copy

"""
converts a BoardCoordinate representing a square on the board to a string
representing the typical chess notation for a square, where the collumn
is represented by a letter from a-h and the row by a number from 1-8.
args : 
    coords : a coordinate pair representing a collumn and row in the chess
             board.
"""
def coord_to_square(coords: BoardCoordinate) -> str | None:
    if len(coords) != 2:
        print("coord must be a coordinate\n")
        return None
    ans = ''
    num = coords[0]
    for let in COLUMN_LETTERS:
        if COLUMNS[let] == num:
            ans += let
    ans += str(coords[1] + 1)
    return ans


"""
Board represents the state of the Chess game. The main state of the board is
stored in the self._board variable: a 2D list of where each index represents a
square on the board, either containing an object that inherits from Piece, or
None, which represents an empty square. Board handles the legality of many
moves, including castling, enpessant and pawn promotion.
"""
class Board():

    """
    Sets up the board for the start of a chess game. If a custom board is
    provided, it is checked for legality. A board is considered legal if:
        1. it has 8 rows and 8 collumns (i.e. it is a list containing 8
           8-element lists)
        2. it has exactly one white king and one black king
    If the board is not legal, an Exception is raised.
    If no board is provided, the default chess board is used.

    i.e.    |R|N|B|Q|K|B|N|R|
            |P|P|P|P|P|P|P|P|
            | | | | | | | | |
            | | | | | | | | |
            | | | | | | | | |
            |P|P|P|P|P|P|P|P|
            |R|N|B|Q|K|B|N|R|
    """
    def __init__(self, board: list[list[Piece | None]] | None = None):
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
        self.enpessant_piece = None

    
    """
    Returns the board representation.
    """
    def get_board(self) -> list[list[Piece | None]]:
        return self._board

    """
    Gets the turn, where True means it is white's turn, False black's turn
    """
    def get_turn(self) -> bool:
        return self._turn

    """
    Swaps the current turn over
    i.e. if it is white's turn, make it black's, or if it is black's turn make
    it white's.
    """
    def change_turn(self) -> None:
        self._turn = WHITE if self._turn == BLACK else BLACK

    """
    Creates and returns the default board, which appears as the following...

        |R|N|B|Q|K|B|N|R|
        |P|P|P|P|P|P|P|P|
        | | | | | | | | |
        | | | | | | | | |
        | | | | | | | | |
        |P|P|P|P|P|P|P|P|
        |R|N|B|Q|K|B|N|R|

    when printed out. Returned in the form of a 2D list.

    """
    def construct_board(self) -> list[list[Piece | None]]:
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


    """
    returns the string representation of the board.

    e.g. starting board appears like this:

        |R|N|B|Q|K|B|N|R|
        |P|P|P|P|P|P|P|P|
        | | | | | | | | |
        | | | | | | | | |
        | | | | | | | | |
        |P|P|P|P|P|P|P|P|
        |R|N|B|Q|K|B|N|R|

    """
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

    """
    if the player is in check, return True, else False 
    args:
        player: WHITE or BLACK, selects which player is to be checked
        board: A 2D list represetning a board state.
        position: The BoardCoordinate of the king to be checked.
    """
    def in_check(self,
                 player: bool,
                 board: list[list[Piece | None]],
                 position: BoardCoordinate) -> bool:

        for row in board:
            for square in row:
                if square is None:
                    continue
                if (square.get_color() != player 
                    and position in square.get_valid_moves(board)):
                    return True
        return False
 
    """
    moves the king to the specified origin square
    args:
        king : a King object instance to be moved
        origin : a board coordinate of where to move the king.
    """
    def reset_king(self, king: King, origin: BoardCoordinate):
        if len(origin) != 2:
            return
        self.get_board()[origin[1]][origin[0]] = king
        king.set_position(origin)
        if king.get_color() == WHITE:
            self.wking_position = origin
        else:
            self.bking_position = origin


    """
    performs a castle move on the board. Assumes castling is legal (see can_castle)
    args:
        king : a King object instance to be moved
        rook : the Rook object instance to be moved
    """
    def castle(self, king: King, rook: Rook) -> None:
        rook_pos = rook.get_position()
        king_pos = king.get_position()
        if rook_pos[0] == 0:
            #long castle
            new_rook_pos = (rook_pos[0] + 3, rook_pos[1])
            new_king_pos = (king_pos[0] - 2, king_pos[1])
        elif rook_pos[0] == 7:
            #short castle
            new_rook_pos = (rook_pos[0] - 2, rook_pos[1])
            new_king_pos = (king_pos[0] + 2, king_pos[1])
        else:
            raise Exception("rook is not on its starting square\n")
        self.get_board()[rook_pos[1]][rook_pos[0]] = None
        self.get_board()[king_pos[1]][king_pos[0]] = None
        king.move_piece(new_king_pos)
        rook.move_piece(new_rook_pos)
        self.get_board()[new_rook_pos[1]][new_rook_pos[0]] = rook
        self.get_board()[new_king_pos[1]][new_king_pos[0]] = king
        if king.get_color() == WHITE:
            self.wking_postiion = new_king_pos
        else:
            self.bking_position = new_king_pos
            
            
    """
    returns True if the king can castle legally to the given position,
    False otherwise
    args:
        king : a King object instance to be moved
        target : The board coordinate which the king will move to
    """
    def can_castle(self, king: King, target: BoardCoordinate) -> bool:
        board = Board(copy.deepcopy(self.get_board()))
        if king.has_moved():
            return False
        position = king.get_position()
        origin = position
        diff = (target[0] - position[0], target[1] - position[1])
        direction = king.get_delta(diff)
        iteration = 1
        #ensure we are not castling out of check
        if self.in_check(king.get_color(), self.get_board(), position):
            return False
        while True:
         #move one square in direction of castle
            position = (position[0] + direction[0], position[1] + direction[1])
            square = board.get_board()[position[1]][position[0]]
            if (square is not None
                    and isinstance(square, Rook)
                    and not square.has_moved()
                    and square.get_color() == king.get_color()):
                king.set_position(origin)
                return True
            #check for pieces blocking
            if board.get_board()[position[1]][position[0]] is not None:
                king.set_position(origin)
                return False
            if iteration <= 2:
                #move the king across one
                cur_pos = king.get_position()
                board.get_board()[cur_pos[1]][cur_pos[0]] = None
                board.get_board()[position[1]][position[0]] = king
                king.set_position(position)
                if king.get_color() == WHITE:
                    board.wking_position = position
                else:
                    board.bking_position = position
                 #see if its in check
                if self.in_check(king.get_color(), board.get_board(), position):
                    board.get_board()[position[1]][position[0]] = None
                    king.set_position(origin)
                    return False
            #shouldn't reach here but you might so check for out of bounds
            if  position[0] < 0 or position[0] > 7:
                king.set_position(origin)
                return False
            iteration += 1

    """
    Returns True if the move is legal for this board, False otherwise
    args:
        position : a board Coordinate of the piece to be moved
        new : a board Coordinate for the piece to move to
    """
    def can_move_piece(self,
                       position: BoardCoordinate,
                       new: BoardCoordinate) -> bool:

        board = Board(copy.deepcopy(self.get_board()))
        board._turn = self.get_turn()
        board.wking_position = self.wking_position
        board.bking_position = self.bking_position
        piece = board.get_board()[position[1]][position[0]]
        if piece is None:
            return False
        elif piece.get_color() != self.get_turn():
            return False
        else:
            if piece.can_move(new, board.get_board()):
                if (isinstance(piece, King)
                        and abs(position[0] - new[0]) == 2 
                        and position[1] - new[1] == 0):
                    if board.can_castle(piece, new):
                        return True
                    else:
                        return False
                piece.set_position(new)
                board.get_board()[position[1]][position[0]] = None
                board.get_board()[new[1]][new[0]] = piece
                if isinstance(piece, King):
                    if piece.get_color() == WHITE:
                        board.wking_position = new
                    else:
                        board.bking_position = new
                king_pos = (board.wking_position 
                            if board.get_turn() == WHITE 
                            else board.bking_position)
                if board.in_check(board.get_turn(),
                                  board.get_board(),
                                  king_pos):
                    return False
                return True
            else:
                return False

    """
    Moves the piece from its position to the new position (including
    castling/promotion/enpesssant). Assumes the move is valid (see
    can_move_piece). Returns 1 if the move is a pawn promotion, 0 otherwise.
    args :
        position : a board Coordinate of the piece to be moved
        new : a board Coordinate for the piece to move to
    """
    def move_piece(self,
                   position: BoardCoordinate,
                   new: BoardCoordinate) -> int:

        if self.enpessant_piece is not None:
            self.enpessant_piece._just_moved = False
        piece = self.get_board()[position[1]][position[0]]
        if piece is None:
            return 0
        if (isinstance(piece, King) 
                and abs(position[0] - new[0]) == 2 
                and position[1] - new[1] == 0):
            left_rook = self.get_board()[position[1]][0]
            right_rook = self.get_board()[position[1]][7]
            rook = left_rook if (position[0] - new[0]) == 2 else right_rook
            if isinstance(rook, Rook):
                self.castle(piece, rook)
                self.change_turn()
            return 0
        if isinstance(piece, Pawn) and (new[1] == 0 or new[1] == 7):
            return 1
        if isinstance(piece, Pawn) and (abs(new[1] - position[1]) == 2):
            self.enpessant_piece = piece
        else:
            self.enpessant_piece = None
        if isinstance(piece, Pawn) and self.is_enpessant(piece, new):
            self.get_board()[position[1]][new[0]] = None
        piece.move_piece(new)
        self._board[position[1]][position[0]] = None
        self._board[new[1]][new[0]] = piece
        if isinstance(piece, King):
            if piece.get_color() == WHITE:
                self.wking_position = new
            else:
                self.bking_position = new
        self.change_turn()
        return 0

    """
    Returns True if the piece and move form a legal execution of enpessant
    args :
        piece : a Pawn object instance which is to be moved
        move : the board coordinate for the pawn to move to
    """
    def is_enpessant(self, piece: Pawn, move: BoardCoordinate) -> bool:
        position = piece.get_position()
        target = self.get_board()[move[1]][move[0]]
        diff = (move[0] - position[0], move[1] - position[1])
        return target is None and diff[0] != 0 

    """
    swaps the piece at position to the piece_type and moves it to the target
    args :
        position : the board coordinates of the piece to be moved.
        piece_type : an instance of the object for the piece to be reassigned.
        target : the board coordinates where the piece will move to.
    
    """
    def promote_piece(self,
                      position: BoardCoordinate,
                      piece_type: Piece,
                      target: BoardCoordinate) -> None:
        piece = self.get_board()[position[1]][position[0]]
        if not isinstance(piece, Pawn):
            return
        piece = piece_type
        piece.move_piece(target)
        self.get_board()[position[1]][position[0]] = None
        self.get_board()[target[1]][target[0]] = piece
        self.change_turn()
        return
    
    """
    If the player of the given color has at least one legal move available to
    them, returns True, else returns False. If True is returned, the player is
    either in Checkmate or Stalemate.
    args :
        board : a 2D list representing a chess board
        color : WHITE or BLACK, the player to check for legal moves.
    """
    def does_legal_move_exist(self, board: list[list[Piece | None]], color: bool) -> bool:
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
                    king_pos = (self.wking_position
                                if color == WHITE 
                                else self.bking_position)
                    if not self.in_check(color, self.get_board(), king_pos):
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

    """
    checks if the player who's turn it currently is is in checkmate. A player
    is in checkmate if they:
        1. Have no legal moves available to them.
        2. Are in check
    returns True if they are in checkmate, False otherwise.
    """
    def in_checkmate(self) -> bool:
        color =  self.get_turn()
        king_pos = (self.wking_position 
                    if color == WHITE 
                    else self.bking_position)
        board = self.get_board()
        if not self.in_check(color, board, king_pos):
            return False
        return self.does_legal_move_exist(board, color)

    
    """
    Checks if the player for who's turn it currently is is in stalemate. A
    player is in stalemate if they are:
        1. Have no legal moves available to them
        2. Are not in check
    returns True if they are in stalemate, False otherwise.
    """
    def in_stalemate(self) -> bool:
        color =  self.get_turn()
        king_pos = (self.wking_position 
                    if color == WHITE 
                    else self.bking_position)
        board = self.get_board()
        if self.in_check(color, board, king_pos):
            return False
        return self.does_legal_move_exist(board, color)


    """
    returns a list of all valid board coordinates that the piece at position
    can legally move to.
    args:
        position : the board coordinates of the piece
    """
    def get_valid_moves(self,
                position: BoardCoordinate) -> list[BoardCoordinate] | None:
        col, row = position
        piece = self.get_board()[row][col]
        if piece is None:
            return
        ans = []
        for move in piece.get_valid_moves(self.get_board()):
            if self.can_move_piece(position, move):
                ans.append(move)


        if isinstance(piece, King):
            for castle_move in [(position[0] + 2, position[1]),
                                (position[0] - 2, position[1])]:
                if self.can_move_piece(position, castle_move):
                    ans.append(castle_move)
        return ans





