
from constants import *
from board import *
from pieces import *

import pygame
import os

pygame.init()


class View():

    def __init__(self, board: Board, window):
        self.window = window
        self.board = []
        self.update_display(board)

    def update_display(self, board: Board, piece_selected: tuple[int] | None = None):
        self.draw_board(board, piece_selected)

    def draw_board(self, model: Board, piece_selected: tuple[int] | None = None) -> None:
        #the top left corner of the board is defined by BOARD_POSITION
        
        board = model.get_board()
        x, y = BOARD_POSITION
        counter = 0
        for row in range(7, -1, -1):
            board_row = []
            for col in range(8):
                pygame.draw.rect(self.window, COLORS[counter%2], pygame.Rect(x, y, SQUARE_LENGTH, SQUARE_LENGTH))
                if board[row][col] is not None:
                    piece_img = pygame.image.load(
                            os.path.join("PIECES", board[row][col].get_filename())).convert_alpha()
                    piece_img = pygame.transform.scale(piece_img, (SQUARE_LENGTH, SQUARE_LENGTH))
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

    def draw_valid_moves(self, moves: list[tuple[int]]):
        if moves is None:
            return
        for move in moves:
            move = (move[0], abs(move[1] - 7))
            x = move[0]*SQUARE_LENGTH + SQUARE_LENGTH // 2
            y = move[1]*SQUARE_LENGTH + SQUARE_LENGTH // 2
            pygame.draw.circle(self.window, GREY, (x, y), VALID_MOVE_RADIUS)
    
    def draw_promotion_options(self, pos: tuple[int], color: bool) -> None:

        pieces = [Queen((0, 0), color), Rook((0, 0), color), Bishop((0, 0), color), Knight((0, 0), color)]

        for i in range(4):
            x = pos[0] + i*SELECT_BOX_LENGTH
            y = pos[1]
            pygame.draw.rect(
                    self.window, DARK_GREY, pygame.Rect(x, y, SELECT_BOX_LENGTH, SELECT_BOX_LENGTH))
            x = x + (SELECT_BOX_LENGTH - INNER_BOX_LENGTH)//2
            y = y + (SELECT_BOX_LENGTH - INNER_BOX_LENGTH)//2
            pygame.draw.rect(
                    self.window, GREY, pygame.Rect(x, y, INNER_BOX_LENGTH, INNER_BOX_LENGTH))
            piece_img = pygame.image.load(
                    os.path.join("PIECES", pieces[i].get_filename())).convert_alpha()
            piece_img = pygame.transform.scale(piece_img, (INNER_BOX_LENGTH, INNER_BOX_LENGTH))
            self.window.blit(piece_img, (x, y))

    """
    draws the game over screen based on exit code. Returns the coords of the play again button, and its
    width and height
    """
    def draw_game_over_screen(self, exit_code: int):
        if exit_code not in [1, 2, 3]:
            return
        if exit_code == 1:
            color = "White"
        else:
            color ="Black"
        font = pygame.font.SysFont('Comic Sans MS', 30)
        if exit_code == 3:
            text = font.render('Stalemate!', False, (0, 0, 0))
        else:
            text = font.render(f'{color} Wins By Checkmate!', False, (0, 0, 0))
        box_x = SCREEN_SIZE // 2 - SQUARE_LENGTH * 2
        box_y = SCREEN_SIZE // 2 - GAME_OVER_BOX_HEIGHT // 2
        pygame.draw.rect(self.window, DARK_GREY, pygame.Rect(box_x, box_y, SQUARE_LENGTH * 4, GAME_OVER_BOX_HEIGHT))
        x = SCREEN_SIZE // 2 - text.get_width() // 2
        y = box_y + text.get_height()*2
        self.window.blit(text, (x, y)) 
        text = font.render('Play Again', False, (0, 0, 0))
        button_x = box_x + GAME_OVER_BOX_WIDTH // 2 - text.get_width() // 2 
        button_y = box_y + GAME_OVER_BOX_HEIGHT // 1.5 - text.get_height() // 2 
        pygame.draw.rect(self.window, GREY, pygame.Rect(button_x-5, button_y-2.5, text.get_width() + 10, text.get_height() + 5)) 
        x, y = button_x, button_y
        self.window.blit(text, (x, y))
        return (button_x - 5, button_y-2.5), text.get_width() + 10, text.get_height() + 5

            




