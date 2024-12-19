
from constants import *
from board import *
from pieces import *

import pygame
import os

pygame.init()


class View():

    def __init__(self, board: list[list[Piece]], window):
        self.window = window
        self.board = []
        self.update_display(board)

    def update_display(self, board: list[list[Piece]]):
        self.draw_board(board)
        pygame.display.flip()

    def draw_board(self, board: list[list[Piece]]) -> None:
        #the top left corner of the board is defined by BOARD_POSITION
        x, y = BOARD_POSITION
        counter = 0
        for row in range(7, -1, -1):
            board_row = []
            for col in range(8):
                pygame.draw.rect(self.window, COLORS[counter%2], pygame.Rect(x, y, SQUARE_LENGTH, SQUARE_LENGTH))
                if board[row][col] is not None:
                    piece_img = pygame.image.load(os.path.join("PIECES", board[row][col].get_filename())).convert_alpha()
                    piece_img = pygame.transform.scale(piece_img, (SQUARE_LENGTH, SQUARE_LENGTH))
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



