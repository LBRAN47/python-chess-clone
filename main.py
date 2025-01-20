from pieces import Pawn, Bishop, Rook, Queen, King, Knight
from constants import *
from board import *
from view import *

import pygame
import time

"""
takes in the input of the user, which must be in the form "charintcharint" e.g. "d4e5".
returns a list of two tuples, the coordinates of the piece to move, and the target square.
"""
def interpreter(text: str) -> list[tuple[int]]:
    
    if len(text) != 4:
        print("text must be of length 4\n")
        return
    pos = text[0:2]
    target = text[2:]
    squares = []
    for coord in [pos, target]:
        if coord[0] not in COLUMNS.keys() or not coord[1].isdigit() or int(coord[1]) not in range(1, 9):
            print(f"{coord} is not a letter in range a-h followed by a number in range 1-8\n")
            return
        col = COLUMNS[coord[0]]
        row = int(coord[1]) - 1
        squares.append((col, row))
    return squares

board = Board()
print(board)
board.move_piece((1, 1), (1, 3))
board.move_piece((2, 6), (2, 4))
board.move_piece((2, 4), (1, 3))
board.move_piece((1, 3), (1, 2))
board.move_piece((1, 2), (1, 1))
board.move_piece((1, 1), (0, 0))
print(board)

board = Board()

board.move_piece((3, 1), (3, 3))
board.move_piece((2, 0), (5, 3))
board.move_piece((4, 1), (4, 2))
board.move_piece((4, 6), (4, 4))
board.move_piece((5, 3), (4, 4))
board.move_piece((4, 4), (3, 3))
board.move_piece((5, 0), (3, 2))
board.move_piece((5, 7), (3, 5))
board.move_piece((3, 5), (2, 6))


print(board)

board = Board()

my_board = board.get_board()
for row in my_board:
    for square in row:
        if square is None:
            continue
        print(f"Piece: {square}, position: {square.get_position()}\nPossible Moves: {square.get_valid_moves(my_board)}")





print("=====================")
print("new game")
print("=====================")


class Controller():

    def __init__(self, board: list[list[Piece]] | None = None):
        self.window = pygame.display.set_mode((8*SQUARE_LENGTH, 8*SQUARE_LENGTH), pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption("CHESS")
        self.window.fill((255, 200, 0))
        self.board = Board(board)
        self.view = View(self.board, self.window)

        self.is_piece_held = False
        self.piece_held = None
        self.piece_held_coords = None

        self.is_promotion = False #indicates whether we are in promotion selection mode
        self.promotion_selected = None #the piece type chosen for promotion

        self.gui_game_loop()
        pygame.quit()

    """
    converts a set of x, y coordinates of a mouse event to coordinates on the chess board. Returns
    None if mouse event occurs somewhere other than the chess board.
    """
    def coords_to_square(self, coords: tuple[int]):
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
    takes in a set of coordinates from a pygame event, if we are not in promotion mode, return None,
    else return the piece to be promoted to based on the position.
    """
    def coords_to_promotion_piece(self, pos: tuple[int]) -> Piece | None:
        if not self.is_promotion:
            return
        pieces = WHITE_PROMOTION_PIECES if self.board.get_turn() == WHITE else BLACK_PROMOTION_PIECES
        for i in range(4):
            min_x = self.promotion_coords[0] + i*SELECT_BOX_LENGTH
            min_y = self.promotion_coords[1]
            max_x = min_x + SELECT_BOX_LENGTH
            max_y = min_y + SELECT_BOX_LENGTH
            if pos[0] >= min_x and pos[0] <= max_x and pos[1] >= min_y and pos[1] <= max_y:
                return pieces[i]
        return


    def terminal_game_loop(self):
        while True:
            move = input("enter 4 characters representing the move e.g. e2e4\n")
            move = interpreter(move)
            if move is None:
                continue
            pos, target = move
            if self.board.can_move_piece(pos, target):
                self.board.move_piece(pos, target)
            print(self.board)
            if self.board.in_checkmate():
                color = "white" if self.board.get_turn() != WHITE else "black"
                print(f"Game Over! {color} wins by checkmate!")
                break
            if self.board.in_stalemate():
                print(f"Game Over! Stalemate!")
                break
            self.view.update_display(self.board.get_board())
            self.view.board = self.board
            time.sleep(0.1)
    
    def gui_game_loop(self):
        while True:
            self.window.fill((0, 0, 0))
            self.view.update_display(self.board, self.piece_held_coords)
            for event in pygame.event.get():
                if event.type == pygame.WINDOWCLOSE:
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.left_mouse_handler(event)
                if event.type == pygame.MOUSEMOTION:
                    self.mouse_movement_handler(event)
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.left_mouse_up_handler(event)
                    if self.board.in_checkmate():
                        color = "white" if self.board.get_turn() != WHITE else "black"
                        print(f"Game Over! {color} wins by checkmate!")
                        return
                    if self.board.in_stalemate():
                        print(f"Game Over! Stalemate!")
                        return
            
            if self.is_piece_held:
                x = self.cur_mouse_x - (SQUARE_LENGTH // 2)
                y = self.cur_mouse_y - (SQUARE_LENGTH // 2)
                self.view.draw_valid_moves(self.board.get_valid_moves(self.piece_held_coords))
                self.window.blit(self.piece_held, (x, y))
            if self.is_promotion:
                self.view.draw_promotion_options((self.promotion_coords), self.board.get_turn())

            pygame.display.flip()
            time.sleep(0.0167)

        return

    def left_mouse_up_handler(self, event):
        if not self.is_piece_held and self.promotion_selected is None:
            return
        if self.promotion_selected is not None:
            self.board.promote_piece(self.promotion_piece_coords, self.promotion_selected, self.promotion_target_coords)
            self.is_promotion = False
            self.promotion_selected = None
            return
        coords = self.coords_to_square(event.pos)
        if coords is None:
            return
        col, row = coords
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

    def mouse_movement_handler(self, event):
        self.cur_mouse_x, self.cur_mouse_y = event.pos



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
            self.piece_held = self.view.board[row][col] #the image of the piece
            self.piece_held_obj = self.board.get_board()[row][col] #the instance of the piece in board
            self.is_piece_held = True
            self.piece_held_coords = coords
        return
            


if __name__ == "__main__":
    Controller()
