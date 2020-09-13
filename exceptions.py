class Error(Exception):
    """Base class for other exceptions"""

    pass


class FieldOutOfBoundsError(Error):
    """Raised when field is out of bounds"""


class MoveNotPermittedError(Error):
    """Raised when the move is not permitted"""