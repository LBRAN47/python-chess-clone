from constants import (COLUMNS, SQUARE_LENGTH, BOARD_POSITION,
                SELECT_BOX_LENGTH, WHITE, END_GAME, WHITE_CHECKMATE,
                BLACK_CHECKMATE, STALEMATE, Coordinate, BoardCoordinate)
from pieces import Piece
from board import Board
from view import View, WHITE_PROMOTION_PIECES, BLACK_PROMOTION_PIECES
import pygame
import time



def interpreter(text: str) -> list[BoardCoordinate] | None:
    """Converts text into a set of BoardCordinates.

    Args:
        text (str): two squares on the chess board representing the move e.g. "d4e5"
    Returns:
        list[BoardCoordinate]: two BoardCoordinates, one for the starting square and one for the ending square.
    """
    
    if len(text) != 4:
        print("text must be of length 4\n")
        return
    pos = text[0:2]
    target = text[2:]
    squares = []
    for coord in [pos, target]:
        if coord[0] not in COLUMNS.keys() or not coord[1].isdigit() or \
        int(coord[1]) not in range(1, 9):
            print(f"{coord} is not a letter in range a-h followed by a " +
                  "number in range 1-8\n")
            return
        col = COLUMNS[coord[0]]
        row = int(coord[1]) - 1
        squares.append((col, row))
    return squares

"""
The Controller class contains the logic for the game, controlling the  flow of
information between the Board (model) class and the View class. When
instantiated, this class runs the game loop indefinately until the user exits
the game window (or force quits if running in terminal).
"""
class Controller():

    """
    Sets up the game window, then runs the game loop. The game loop consists of
    3 stages:
        1. initialise the game variables for the start of a new game
        2. run the game until it finishes
        3. Display the relevant game over screen
    During the game over screen, if the player chooses to play again, the loop
    will perform another iteration. If the player chooses to close the game
    either during the game or in the game over screen. The loop will break
    and the window will close.
    args:
        board : A 2D list representing the board grid. Each 'cell' contains
                either a class that extends Piece, or None (representing an
                empty square)
    """
    def __init__(self, board: list[list[Piece | None]] | None = None):

        self.window = pygame.display.set_mode(
                (8*SQUARE_LENGTH, 8*SQUARE_LENGTH),
                pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption("CHESS")
        self.window.fill((255, 255, 255))


        #run the game loop
        while True:
            self.initialise_game(board)
            exit_code = self.gui_game_loop()
            if exit_code == 0:
                break
            self.game_over_screen(exit_code)
        pygame.quit()

    """
    Sets all the game variables to their required states for the start of the game.
    args:
        board : A 2D list representing the board grid. Each 'cell' contains
                either a class that extends Piece, or None (representing an
                empty square)
    """
    def initialise_game(self, board: list[list[Piece | None]] | None = None) -> None:
        self.board = Board(board)
        self.view = View(self.window)

        self.is_piece_held = False
        self.piece_held = None
        self.piece_held_coords = None

        self.is_promotion = False #indicates whether we are in promotion
                                  #selection mode
        self.promotion_selected = None #the piece type chosen for promotion


    """
    Converts a set of x, y coordinates of a mouse event to coordinates on the
    chess board.

    args:
        coords : a tuple of two integers, representing a coordinate where the
                 first integer is the x value and the second is the y value.
    returns: another tuple of two integers, this time representing a 0-indexed
             coordinate on the chess board, the row and the collumn, unless the
             provided coordinates were outside the range of the board, then None
             is returned.
    """
    def coords_to_square(self,
                         coords: Coordinate) -> Coordinate | None:
        targ_x, targ_y = coords
        x, y = BOARD_POSITION
        targ_row_num = None
        for row in range(7, -1, -1):
            if targ_y > y and targ_y < (y + SQUARE_LENGTH):
                targ_row_num = row
                break
            y += SQUARE_LENGTH
        if targ_row_num is None:
            print("y not in range :(")
            return
        targ_col_num = None
        for col in range(8):
            if targ_x > x and targ_x < (x + SQUARE_LENGTH):
                targ_col_num = col
                break
            x += SQUARE_LENGTH
        if targ_col_num is None:
            print("x not in range :(")
            return
        return targ_col_num, targ_row_num

    """
    takes in a set of coordinates from a pygame event, if we are not in
    promotion mode, return None, else return the piece to be promoted to based
    on the position.
    """
    def coords_to_promotion_piece(self, coords: Coordinate) -> Piece | None:
        if not self.is_promotion:
            return
        pieces = (WHITE_PROMOTION_PIECES
                  if self.board.get_turn() == WHITE
                  else BLACK_PROMOTION_PIECES)
        for i in range(4):
            min_x = self.promotion_coords[0] + i*SELECT_BOX_LENGTH
            min_y = self.promotion_coords[1]
            max_x = min_x + SELECT_BOX_LENGTH
            max_y = min_y + SELECT_BOX_LENGTH
            if (coords[0] >= min_x and coords[0] <= max_x and
                    coords[1] >= min_y and coords[1] <= max_y):
                return pieces[i]
        return
    

    """
    Runs the Chess game in the window. For each iteration of this game loop
    the following occurs in order:
        - The window is cleared
        - The board and pieces are drawn (with the exception of the piece
          held by the player, which is drawn later)
        - The relevant events are handled(if the event is MOUSEBUTTONUP, the
          Board's state may have updated, so we check if the game has ended,
          if it has, we exit the game loop and return an exit code)
        - If a piece is held by the player, we draw it next to the cursor, and
          we show the valid move options.
        - If we are promoting a piece we display the promotion options
        - the window updates
    Each loop occurs with a slight delay to prevent lag.
    returns : an integer exit code representing the way the game ended. There
              are 4 ways for the game to end: BLACK_CHECKMATE if black wins by
              checkmate, WHITE_CHECKMATE if white wins by checkmate, STALEMATE,
              and END_GAME if the player closes the window during the game.
    """
    def gui_game_loop(self) -> int:
        while True:
            self.window.fill((0, 0, 0))
            self.view.draw_board(self.board, self.piece_held_coords)
            for event in pygame.event.get():
                if event.type == pygame.WINDOWCLOSE:
                    return END_GAME
                elif (event.type == pygame.MOUSEBUTTONDOWN
                      and event.button == 1):
                    self.left_mouse_handler(event)
                elif event.type == pygame.MOUSEMOTION:
                    self.mouse_movement_handler(event)
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.left_mouse_up_handler(event)
                    if self.board.in_checkmate():
                        color = ("white"
                                 if self.board.get_turn() != WHITE
                                 else "black")
                        exit_code = (WHITE_CHECKMATE
                                     if color == "white"
                                     else BLACK_CHECKMATE)
                        print(f"Game Over! {color} wins by checkmate!")
                        return exit_code
                    if self.board.in_stalemate():
                        print("Game Over! Stalemate!")
                        return STALEMATE
            
            if self.is_piece_held:
                x = self.cur_mouse_x - (SQUARE_LENGTH // 2)
                y = self.cur_mouse_y - (SQUARE_LENGTH // 2)
                self.view.draw_valid_moves(
                        self.board.get_valid_moves(self.piece_held_coords))
                self.window.blit(self.piece_held, (x, y))

            if self.is_promotion:
                self.view.draw_promotion_options((self.promotion_coords),
                                                 self.board.get_turn())

            pygame.display.flip()
            time.sleep(0.01)


    """
    Handles the player lifting the left mouse button.

    If the player is selecting a promotion piece, we perform the promotion in
    the model, and exit promotion mode.

    If the player is placing a piece, we move it in the model if it is valid.
    If the move is a pawn promotion, we update the relevant member variables.
    
    Finally we 'deselect' the piece by changing the relevant member variables.
    args:
        event : a pygame.event.Event instance 
    """
    def left_mouse_up_handler(self, event) -> None:
        if not self.is_piece_held and self.promotion_selected is None:
            return
        if self.promotion_selected is not None:
            self.board.promote_piece(self.promotion_piece_coords,
                                     self.promotion_selected,
                                     self.promotion_target_coords)
            self.is_promotion = False
            self.promotion_selected = None
            return
        coords = self.coords_to_square(event.pos)
        if coords is None:
            return
        col, row = coords
        if self.piece_held_coords is None:
            return
        piece_col, piece_row = self.piece_held_coords
        if self.board.can_move_piece((piece_col, piece_row), (col, row)):
            flag = self.board.move_piece((piece_col, piece_row), (col, row))
            if flag: #promotion
                self.is_promotion = True
                self.promotion_piece_coords = self.piece_held_coords
                self.promotion_target_coords = coords
                self.promotion_coords = event.pos

        self.is_piece_held = False
        self.piece_held = None
        self.piece_held_coords = None


    """
    Sets the current mouse position to the x,y position of the event
    args:
        event : a pygame.event.Event instance 
    """
    def mouse_movement_handler(self, event):
        self.cur_mouse_x, self.cur_mouse_y = event.pos



    """
    Event handler for pushing mouse-1.

    If we are in promotion mode and have selected a piece to promote to, we set
    its member variable. 

    If we have yet to select a piece, we select the piece at the position of
    event.

    args:
        event : a pygame.event.Event instance 
    """
    def left_mouse_handler(self, event):
        if self.is_piece_held:
            return
        x, y = event.pos
        self.promotion_selected = self.coords_to_promotion_piece((x, y))
        if self.promotion_selected is not None or self.is_promotion:
            return
        coords  = self.coords_to_square(event.pos)
        if coords is None:
            return
        col, row = coords
        if self.view.board[row][col] is not None:
            #the image of the piece
            self.piece_held = self.view.board[row][col] 
            #the instance of the piece in board
            self.piece_held_obj = self.board.get_board()[row][col] 
            self.is_piece_held = True
            self.piece_held_coords = coords
        return


    """
    Displays the game over screen until the player chooses to play again or
    exit the game. If they choose to play again, the method returns, if they
    choose to exit, the method calls quit().
    args:
        exit_code: an integer exit code representing how the game ended
    """
    def game_over_screen(self, exit_code: int) -> None:
        if exit_code == 0:
            return
        while True:
            game_over_info = self.view.draw_game_over_screen(exit_code)
            if game_over_info is None:
                raise ValueError("invalid exit_code provided")
            coords, width, height = game_over_info
            min_x, max_x = coords[0], coords[0] + width
            min_y, max_y = coords[1], coords[1] + height
            for event in pygame.event.get():
                if event.type == pygame.WINDOWCLOSE:
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos
                    if x >= min_x and x <= max_x and y >= min_y and y <= max_y:
                        return
            pygame.display.flip()
            


def main():
    Controller()
