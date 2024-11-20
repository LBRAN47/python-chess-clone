from pieces import Pawn, Bishop, Rook, Queen, King, Knight
from constants import *


pawn = Pawn((1, 1), WHITE)
pawn2 = Pawn((4, 1), WHITE)
pawn3 = Pawn((5, 1), WHITE)
pawn4 = Pawn((2, 6), BLACK)
pawn5 = Pawn((2, 1), WHITE)

assert pawn.can_move((1, 2))
assert pawn.can_move((1, 3))
assert pawn.can_move((2, 2))
assert pawn.can_move((0, 2))
assert not pawn.can_move((1, 0))

assert pawn4.can_move((2, 5))
assert pawn4.can_move((2, 4))
assert pawn4.can_move((1, 5))
assert pawn4.can_move((3, 5))
assert not pawn4.can_move((2, 7))
assert not pawn4.can_move((-1, 2))
assert not pawn4.can_move((2, 2))

bishop = Bishop((4, 4), WHITE)
bishop2 = Bishop((3, 2), BLACK)

assert bishop.can_move((3, 3))
assert bishop.can_move((3, 5))
assert bishop2.can_move((4, 1))
assert not bishop.can_move((5, 2))

rook = Rook((2, 3), WHITE)
rook2 = Rook((3, 4), BLACK)

assert rook.can_move((2, 7))
assert rook.can_move((1, 3))
assert not rook.can_move((4, 2))
assert not rook.can_move((-1, 3))

queen = Queen((3, 2), WHITE)

assert queen.can_move((3, 6))
assert queen.can_move((1, 2))
assert queen.can_move((4, 3))
assert queen.can_move((5, 4))
assert queen.can_move((5, 0))
assert not queen.can_move((5, 3))

king3 = King((5, 1), WHITE)
king2 = King((5, 7), BLACK)

assert king3.can_move((6, 1))
assert king3.can_move((5, 0))
assert king2.can_move((7, 7))
assert king2.can_move((3, 7))

knight = Knight((4, 4), WHITE)

assert knight.can_move((2, 5))
assert knight.can_move((3, 6))
assert knight.can_move((5, 6))
assert knight.can_move((6, 5))
assert knight.can_move((6, 3))
assert knight.can_move((5, 2))
