
from constants import *
import board
import pieces

import pygame

pygame.init()

window = pygame.display.set_mode((500, 500))

pygame.display.set_caption("CHESS")

exit = False

window.fill((255, 200, 0))

def draw_board() -> None:
    x = 0
    y = 0
    counter = 0
    for row in range(8):
        for col in range(8):
            pygame.draw.rect(window, COLORS[counter%2], pygame.Rect(x, y, SQUARE_LENGTH, SQUARE_LENGTH))
            x += SQUARE_LENGTH
            counter += 1
        x = 0
        y += SQUARE_LENGTH
        counter += 1

draw_board()
while not exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
    pygame.display.update()
