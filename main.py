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
def interpreter(text: str) -> list[tuple[int]] | None:
    
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


class Controller():

    def __init__(self, board: list[list[Piece]] | None = None):
        self.window = pygame.display.set_mode((8*SQUARE_LENGTH, 8*SQUARE_LENGTH), pygame.HWSURFACE | pygame.DOUBLEBUF)
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

    def initialise_game(self, board: list[list[Piece]] | None = None) -> None:
        self.board = Board(board)
        self.view = View(self.board, self.window)

        self.is_piece_held = False
        self.piece_held = None
        self.piece_held_coords = None

        self.is_promotion = False #indicates whether we are in promotion selection mode
        self.promotion_selected = None #the piece type chosen for promotion


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
    
    def gui_game_loop(self) -> int:
        while True:
            self.window.fill((0, 0, 0))
            self.view.update_display(self.board, self.piece_held_coords)
            for event in pygame.event.get():
                if event.type == pygame.WINDOWCLOSE:
                    return END_GAME
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.left_mouse_handler(event)
                elif event.type == pygame.MOUSEMOTION:
                    self.mouse_movement_handler(event)
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.left_mouse_up_handler(event)
                    if self.board.in_checkmate():
                        color = "white" if self.board.get_turn() != WHITE else "black"
                        exit_code = WHITE_CHECKMATE if color == "white" else BLACK_CHECKMATE
                        print(f"Game Over! {color} wins by checkmate!")
                        return exit_code
                    if self.board.in_stalemate():
                        print(f"Game Over! Stalemate!")
                        return STALEMATE
            
            if self.is_piece_held:
                x = self.cur_mouse_x - (SQUARE_LENGTH // 2)
                y = self.cur_mouse_y - (SQUARE_LENGTH // 2)
                self.view.draw_valid_moves(self.board.get_valid_moves(self.piece_held_coords))
                self.window.blit(self.piece_held, (x, y))
            if self.is_promotion:
                self.view.draw_promotion_options((self.promotion_coords), self.board.get_turn())

            pygame.display.flip()
            time.sleep(0.01)

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

    def game_over_screen(self, exit_code: int) -> None:
        if exit_code == 0:
            return
        while True:
            coords, width, height = self.view.draw_game_over_screen(exit_code)
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
            


if __name__ == "__main__":
    Controller()
