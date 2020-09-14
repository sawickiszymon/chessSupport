import numpy as np

from exceptions import FieldOutOfBoundsError
from settings import CHESS_BOARD, CHESS_DIMENSION


def is_in_bounds(x: int, y: int) -> bool:
    # checks if position in bounds
    if (
        CHESS_DIMENSION[0] <= x < CHESS_DIMENSION[1]
        and CHESS_DIMENSION[0] <= y < CHESS_DIMENSION[1]
    ):
        return True
    return False


def get_field_coordinates(field: str) -> (int, int):
    # checks if position is on the board
    x, y = np.where(CHESS_BOARD == field)
    if not is_in_bounds(x, y):
        raise FieldOutOfBoundsError("Field does not exist.")
    else:
        return x[0], y[0]
