import numpy as np
from settings import chess_board

def king_list(x, y):
    return [
        (x + 1, y),
        (x + 1, y + 1),
        (x + 1, y - 1),
        (x, y + 1),
        (x, y - 1),
        (x - 1, y),
        (x - 1, y + 1),
        (x - 1, y - 1),
    ]


def knight_list(x, y, int1, int2):

    return [
        (x + int1, y + int2),
        (x - int1, y + int2),
        (x + int1, y - int2),
        (x - int1, y - int2),
        (x + int2, y + int1),
        (x - int2, y + int1),
        (x + int2, y - int1),
        (x - int2, y - int1),
    ]


class Error(Exception):
    """Base class for other exceptions"""

    pass


class FieldOutOfBoundsError(Error):
    """Raised when field is out of bounds"""


class MoveNotPermittedError(Error):
    """Raised when the move is not permitted"""


def is_in_bounds(x: int, y: int) -> bool:
    # checks if a position is on the board
    if x >= 0 and x < 8 and y >= 0 and y < 8:
        return True
    return False


def get_field_coordinates(field: str) -> (int, int):
    # checks if a position is on the board
    x, y = np.where(chess_board == field)
    if not is_in_bounds(x, y):
        raise FieldOutOfBoundsError("Field does not exist.")

    return x[0], y[0]

