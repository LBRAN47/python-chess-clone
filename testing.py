from pieces import Pawn, Bishop, Rook, Piece
from constants import *


pawn = Pawn((1, 2), WHITE)
pawn2 = Pawn((4, 2), WHITE)
pawn3 = Pawn((5, 2), WHITE)
pawn4 = Pawn((2, 7), BLACK)
pawn5 = Pawn((2, 2), WHITE)

assert pawn.can_move((1, 3))
assert pawn.can_move((1, 4))
assert pawn.can_move((2, 3))
assert not pawn.can_move((0, 3))
assert not pawn.can_move((1, 1))

assert pawn4.can_move((2, 6))
assert pawn4.can_move((2, 5))
assert pawn4.can_move((1, 6))
assert pawn4.can_move((3, 6))
assert not pawn4.can_move((2, 8))
assert not pawn4.can_move((-1, 3))
assert not pawn4.can_move((2, 3))

bishop = Bishop((4, 4), WHITE)
bishop2 = Bishop((3, 2), BLACK)

assert bishop.can_move((3, 3))
assert bishop.can_move((3, 5))
assert bishop2.can_move((4, 1))
assert not bishop.can_move((5, 2))

rook = Rook((2, 3), WHITE)
rook2 = Rook((3, 4), BLACK)

assert rook.can_move((2, 8))
assert rook.can_move((1, 3))
assert not rook.can_move((4, 2))
assert not rook.can_move((-1, 3))
