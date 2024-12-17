
from constants import *
from board import *
from pieces import *

import pygame
import os

pygame.init()

window = pygame.display.set_mode((500, 500))

pygame.display.set_caption("CHESS")


window.fill((255, 200, 0))

def draw_board(board: list[list[Piece]]) -> None:
    x = 0
    y = 0
    counter = 0
    for row in range(7, -1, -1):
        for col in range(8):
            pygame.draw.rect(window, COLORS[counter%2], pygame.Rect(x, y, SQUARE_LENGTH, SQUARE_LENGTH))
            if board[row][col] is not None:
                piece_img = pygame.image.load(os.path.join("PIECES", board[row][col].get_filename())).convert_alpha()
                piece_img = pygame.transform.scale(piece_img, (SQUARE_LENGTH, SQUARE_LENGTH))
                window.blit(piece_img, (x, y))
            x += SQUARE_LENGTH
            counter += 1
        x = 0
        y += SQUARE_LENGTH
        counter += 1
class View():

    def __init__(self, board: list[list[Piece]]):
        self.update_display(board)

    def update_display(self, board: list[list[Piece]]):
        draw_board(board)
        pygame.display.flip()
