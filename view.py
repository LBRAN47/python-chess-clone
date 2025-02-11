
from constants import (BOARD_POSITION, COLORS, INNER_BOX_LENGTH,
                       SELECT_BOX_LENGTH, SQUARE_LENGTH, GREY,
                       VALID_MOVE_RADIUS, BLACK, WHITE, DARK_GREY,
                       GAME_OVER_BOX_WIDTH, GAME_OVER_BOX_HEIGHT, SCREEN_SIZE)


from board import Board
from pieces import Bishop, Knight, Rook, Queen

import pygame
import os

#######CONSTANTS###############################################################
WHITE_PROMOTION_PIECES = [Queen((0, 0), WHITE), Rook((0, 0), WHITE),
                          Bishop((0, 0), WHITE), Knight((0, 0), WHITE)]
BLACK_PROMOTION_PIECES = [Queen((0, 0), BLACK), Rook((0, 0), BLACK),
                          Bishop((0, 0), BLACK), Knight((0, 0), BLACK)]
###############################################################################

pygame.init()


"""
The View class handles updating the window display based on the model.
"""
class View():

    """
    Initialises the View window and the board.
    args:
        window : a display Surface, the game window
    """
    def __init__(self, window):
        self.window = window
        self.board = [] #a 2D array of pygame.Image objects

    """
    Draws the board and its pieces.
    args:
        model : a Board instance representing the state of the board
        piece_selected : either the board coordinates of the piece currently
                         held by the player, or None if no piece is held.
                         Defaults to None.
    """
    def draw_board(self,
                   model: Board,
                   piece_selected: tuple[int, int] | None = None) -> None:
        
        board = model.get_board()
        #the top left corner of the board is defined by BOARD_POSITION
        x, y = BOARD_POSITION
        counter = 0
        for row in range(7, -1, -1):
            board_row = []
            for col in range(8):
                rectangle = pygame.Rect(x, y, SQUARE_LENGTH, SQUARE_LENGTH)
                pygame.draw.rect(self.window, COLORS[counter%2], rectangle)
                if board[row][col] is not None:
                    piece_img = pygame.image.load(
                            os.path.join("PIECES",
                            board[row][col].get_filename())).convert_alpha()
                    piece_img = pygame.transform.scale(piece_img,
                                            (SQUARE_LENGTH, SQUARE_LENGTH))
                    if piece_selected is None or piece_selected != (col, row):
                        self.window.blit(piece_img, (x, y))
                    board_row.append(piece_img)
                else:
                    board_row.append(None)
                x += SQUARE_LENGTH
                counter += 1
            self.board.insert(0, board_row)
            x = BOARD_POSITION[0]
            y += SQUARE_LENGTH
            counter += 1

    """
    Draws a grey circle on each square in the list of moves.
    args:
        moves : a list of board coordinates.
    """
    def draw_valid_moves(self, moves: list[tuple[int, int]]):
        if moves is None:
            return
        for move in moves:
            move = (move[0], abs(move[1] - 7))
            x = move[0]*SQUARE_LENGTH + SQUARE_LENGTH // 2
            y = move[1]*SQUARE_LENGTH + SQUARE_LENGTH // 2
            pygame.draw.circle(self.window, GREY, (x, y), VALID_MOVE_RADIUS)
    
    """
    Draws a box on the screen allowing the user to select a piece to promote to.

    args:
        pos : the x,y coordinates on the window to start drawing the box
        color : WHITE or BLACK, represents which color is promoting
    """
    def draw_promotion_options(self, pos: tuple[int, int], color: bool) -> None:

        pieces = (WHITE_PROMOTION_PIECES 
                  if color == WHITE
                  else BLACK_PROMOTION_PIECES)

        for i in range(4):
            x = pos[0] + i*SELECT_BOX_LENGTH
            y = pos[1]
            pygame.draw.rect(self.window,
                             DARK_GREY,
                             pygame.Rect(x, y,
                                         SELECT_BOX_LENGTH, SELECT_BOX_LENGTH))
            x = x + (SELECT_BOX_LENGTH - INNER_BOX_LENGTH) // 2
            y = y + (SELECT_BOX_LENGTH - INNER_BOX_LENGTH) // 2
            pygame.draw.rect(self.window,
                             GREY,
                             pygame.Rect(x, y,
                                         INNER_BOX_LENGTH, INNER_BOX_LENGTH))
            piece_img = pygame.image.load(
                    os.path.join("PIECES",
                                 pieces[i].get_filename())).convert_alpha()
            piece_img = pygame.transform.scale(
                    piece_img,
                    (INNER_BOX_LENGTH, INNER_BOX_LENGTH))
            self.window.blit(piece_img, (x, y))

    """
    draws the game over screen based on exit code. Returns the coords of the
    play again button, and its width and height
    args:
        exit_code : an integer exit_code representing how the game ended.
    """
    def draw_game_over_screen(self,
                              exit_code: int) -> tuple[tuple[int, float],
                                                       int, int] | None:
        if exit_code not in [1, 2, 3]:
            return
        if exit_code == 1:
            color = "White"
        else:
            color ="Black"
        font = pygame.font.SysFont('Comic Sans MS', int(SQUARE_LENGTH // 2.5))
        if exit_code == 3:
            text = font.render('Stalemate!', False, (0, 0, 0))
        else:
            text = font.render(f'{color} Wins By Checkmate!', False, (0, 0, 0))
        box_x = SCREEN_SIZE // 2 - SQUARE_LENGTH * 2
        box_y = SCREEN_SIZE // 2 - GAME_OVER_BOX_HEIGHT // 2
        pygame.draw.rect(self.window,
                         DARK_GREY,
                         pygame.Rect(box_x, box_y,
                                     SQUARE_LENGTH * 4,
                                     GAME_OVER_BOX_HEIGHT
                                     )
                         )
        x = SCREEN_SIZE // 2 - text.get_width() // 2
        y = box_y + text.get_height()*2
        self.window.blit(text, (x, y)) 
        text = font.render('Play Again', False, (0, 0, 0))
        button_x = box_x + GAME_OVER_BOX_WIDTH // 2 - text.get_width() // 2 
        button_y = box_y + GAME_OVER_BOX_HEIGHT // 1.5 - text.get_height() // 2 
        pygame.draw.rect(self.window,
                         GREY,
                         pygame.Rect(button_x-5, button_y-2.5,
                                     text.get_width() + 10,
                                     text.get_height() + 5
                                     )
                         ) 
        x, y = button_x, button_y
        self.window.blit(text, (x, y))
        return ((button_x - 5, button_y-2.5),
                text.get_width() + 10,
                text.get_height() + 5)

            




