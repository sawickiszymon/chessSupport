from abc import ABC, abstractmethod
from settings import *
from utils import *


class Figure(ABC):
    def __init__(self, field: str):
        self.field = field

    @abstractmethod
    def list_available_moves(self):
        pass

    @abstractmethod
    def validate_move(self, dest_field):
        pass


class Context:
    def __init__(self, strategy: Figure) -> None:
        self._strategy = strategy

    # @property
    # def strategy(self) -> Figure:
    #     return self._strategy
    #
    # @strategy.setter
    # def strategy(self, strategy: Figure) -> None:
    #     self._strategy = strategy

    def list_moves(self) -> None:
        result = self._strategy.list_available_moves()
        return result

    def validate_move(self, dest_field) -> None:
        result = self._strategy.validate_move(dest_field)
        return result


class King(Figure):
    def list_available_moves(self) -> list:
        x, y = get_field_coordinates(self.field)
        available_moves = list()
        for xx, yy in king_list(x, y):
            if is_in_bounds(xx, yy):
                available_moves.append((xx, yy))
        Y = np.transpose(available_moves)[0]
        X = np.transpose(available_moves)[1]
        available_moves = chess_board[Y, X]
        return available_moves.tolist()

    def validate_move(self, dest_field: str):
        available_moves = self.list_available_moves()
        for moves in available_moves:
            if moves == dest_field:
                return "valid"
        raise MoveNotPermittedError("Current move is not permitted.")
        # return "invalid"


class Pawn(Figure):
    def list_available_moves(self) -> list:
        available_moves, error = list(), None
        x, y = get_field_coordinates(self.field)
        field_name, field_number = self.__get_field_pole()
        new_field_number = field_number + 1
        available_moves.append(f"{field_name}{new_field_number}")
        return available_moves

    def validate_move(self, dest_field: str) -> str:
        valid_move = self.list_available_moves()
        if valid_move[0] == dest_field:
            return "valid"
        else:
            return "invalid"

    def __get_field_pole(self) -> [str, int]:
        field_number = int(self.field[1])
        field_name = self.field[0]
        return field_name, field_number


class Queen(Figure):
    def list_available_moves(self) -> list:
        available_moves = list()

        x, y = get_field_coordinates(self.field)
        for xint, yint in chessDiagonals + chessCardinals:
            xtemp, ytemp = x + xint, y + yint
            while is_in_bounds(xtemp, ytemp):

                available_moves.append((xtemp, ytemp))

                xtemp, ytemp = xtemp + xint, ytemp + yint

        Y = np.transpose(available_moves)[0]
        X = np.transpose(available_moves)[1]

        available_moves = chess_board[Y, X]
        return available_moves.tolist()

    def validate_move(self, dest_field: str):
        available_moves = self.list_available_moves()
        for moves in available_moves:
            if moves == dest_field:
                return "valid"
        return "invalid"


class Rook(Figure):
    def list_available_moves(self) -> list:
        available_moves = list()

        x, y = get_field_coordinates(self.field)
        for xint, yint in chessCardinals:
            xtemp, ytemp = x + xint, y + yint
            while is_in_bounds(xtemp, ytemp):

                available_moves.append((xtemp, ytemp))

                xtemp, ytemp = xtemp + xint, ytemp + yint

        Y = np.transpose(available_moves)[0]
        X = np.transpose(available_moves)[1]

        available_moves = chess_board[Y, X]
        return available_moves.tolist()

    def validate_move(self, dest_field):
        available_moves = self.list_available_moves()
        for moves in available_moves:
            if moves == dest_field:
                return "valid"
        return "invalid"


class Bishop(Figure):
    def list_available_moves(self) -> list:
        available_moves = list()
        x, y = get_field_coordinates(self.field)
        for xint, yint in chessDiagonals:
            xtemp, ytemp = x + xint, y + yint
            while is_in_bounds(xtemp, ytemp):

                available_moves.append((xtemp, ytemp))

                xtemp, ytemp = xtemp + xint, ytemp + yint

        Y = np.transpose(available_moves)[0]
        X = np.transpose(available_moves)[1]

        available_moves = chess_board[Y, X]
        return available_moves.tolist()

    def validate_move(self, dest_field):
        available_moves = self.list_available_moves()
        for moves in available_moves:
            if moves == dest_field:
                return "valid"
        return "invalid"


class Knight(Figure):
    def list_available_moves(self) -> list:
        x, y = get_field_coordinates(self.field)
        available_moves = list()
        for xx, yy in knight_list(x, y, 2, 1):
            if is_in_bounds(xx, yy):
                available_moves.append((xx, yy))
        Y = np.transpose(available_moves)[0]
        X = np.transpose(available_moves)[1]
        available_moves = chess_board[Y, X]
        return available_moves.tolist()

    def validate_move(self, dest_field: str):
        available_moves = self.list_available_moves()
        for moves in available_moves:
            if moves == dest_field:
                return "valid"
        return "invalid"
