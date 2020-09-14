import numpy as np

from exceptions import FieldOutOfBoundsError, MoveNotPermittedError
from factories.figure_factory import FigureFactory
from objects.Figure import Pawn, Bishop, Knight, Rook, Queen, King
from settings import CHESS_BOARD, CHESS_DIAGONALS, CHESS_CARDINALS, CHESS_DIMENSION
from utils import is_in_bounds


class TestPawn:
    def test_list_available_moves_pawn_out_of_board(self):
        data = FigureFactory.build(field="H9")
        error = None
        self.__list_available_moves(data["field"])
        pawn = Pawn(**data)
        try:
            pawn.list_available_moves()
        except FieldOutOfBoundsError as err:
            error = err.args[0]

        assert error == "Field does not exist."

    def test_middle_field_valid_movement(self):
        middle_field = "D4"
        data = FigureFactory.build(field=middle_field)
        pawn = Pawn(**data)
        available_moves = pawn.list_available_moves()
        dest_field = f"{pawn.field[0]}{int(pawn.field[1]) + 1}"
        assert dest_field in available_moves

    def test_edge_field_invalid_movement(self):
        edge_field = "H8"
        data = FigureFactory.build(field=edge_field)
        pawn = Pawn(**data)
        available_moves = pawn.list_available_moves()
        dest_field = []
        assert dest_field == available_moves

    def test_invalid_movement_wrong_field_number(self):
        data = FigureFactory.build()
        pawn = Pawn(**data)
        dest_field = f"{pawn.field[0]}{int(pawn.field[1]) - 3}"
        try:
            pawn.validate_move(dest_field)
        except MoveNotPermittedError as err:
            error = err.args[0]
        assert error == "Current move is not permitted."

    def test_list_available_moves_pawn(self):
        data = FigureFactory.build()
        expected_move = self.__list_available_moves(data["field"])
        pawn = Pawn(**data)
        available_moves = pawn.list_available_moves()
        assert available_moves == expected_move

    def __list_available_moves(self, field: str) -> list:
        available_moves = list()
        field_number = int(field[1])
        field_name = field[0]
        if field_number < CHESS_DIMENSION[1]:
            new_field_number = field_number + 1
            available_moves.append(f"{field_name}{new_field_number}")
        else:
            new_field_number = field_number - 1
            available_moves = [f"{field_name}{new_field_number}"]
        return available_moves


class TestBishop:
    def test_list_available_moves_bishop(self):
        data = FigureFactory.build()
        bishop = Bishop(**data)
        expected_moves = self.__list_available_moves(data["field"])
        available_moves = bishop.list_available_moves()
        assert available_moves == expected_moves

    def test_middle_field_valid_move_bishop(self):
        middle_field = "D4"
        data = FigureFactory.build(field=middle_field)
        bishop = Bishop(**data)
        available_moves = self.__list_available_moves(data["field"])
        dest_field = f"E{int(bishop.field[1]) + 1}"
        assert dest_field in available_moves

    def test_edge_field_valid_move_bishop(self):
        edge_field = "H8"
        data = FigureFactory.build(field=edge_field)
        bishop = Bishop(**data)
        available_moves = self.__list_available_moves(data["field"])
        dest_field = f"E{int(bishop.field[1]) - 3}"
        assert dest_field in available_moves

    def test_invalid_move_bishop(self):
        data = FigureFactory.build()
        bishop = Bishop(**data)
        available_moves = self.__list_available_moves(data["field"])
        dest_field = f"A{int(bishop.field[1]) - 1}"
        assert dest_field not in available_moves

    def __list_available_moves(self, field: str) -> list:
        available_moves = list()

        x, y = np.where(CHESS_BOARD == field)
        for x_shift, y_shift in CHESS_DIAGONALS:
            x_temp, y_temp = x[0] + x_shift, y[0] + y_shift
            while is_in_bounds(x_temp, y_temp):
                available_moves.append((x_temp, y_temp))

                x_temp, y_temp = x_temp + x_shift, y_temp + y_shift

        available_move_y_position = np.transpose(available_moves)[0]
        available_move_x_position = np.transpose(available_moves)[1]

        available_moves = CHESS_BOARD[
            available_move_y_position, available_move_x_position
        ]
        return available_moves.tolist()


class TestKnight:
    def test_list_available_moves_knight(self):
        data = FigureFactory.build()
        knight = Knight(**data)
        expected_moves = self.__list_available_moves(data["field"])
        available_moves = knight.list_available_moves()
        assert available_moves == expected_moves

    def test_middle_field_validate_move_knight(self):
        middle_field = "D4"
        data = FigureFactory.build(field=middle_field)
        knight = Knight(**data)
        available_moves = self.__list_available_moves(data["field"])
        dest_field = f"F{int(knight.field[1]) - 1}"
        assert dest_field in available_moves

    def test_edge_field_validate_move_knight(self):
        edge_field = "H8"
        data = FigureFactory.build(field=edge_field)
        knight = Knight(**data)
        available_moves = self.__list_available_moves(data["field"])
        dest_field = f"F{int(knight.field[1]) - 1}"
        assert dest_field in available_moves

    def __list_available_moves(self, field: str) -> list:
        x, y = np.where(CHESS_BOARD == field)
        available_moves = list()
        for x_position, y_position in self.__knight_list(x[0], y[0], 2, 1):
            if is_in_bounds(x_position, y_position):
                available_moves.append((x_position, y_position))
        available_move_y_position = np.transpose(available_moves)[0]
        available_move_x_position = np.transpose(available_moves)[1]
        available_moves = CHESS_BOARD[
            available_move_y_position, available_move_x_position
        ]
        return available_moves.tolist()

    def __knight_list(self, x: int, y: int, int1: int, int2: int) -> list:

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


class TestRook:
    def test_list_available_moves_rook(self):
        data = FigureFactory.build()
        rook = Rook(**data)
        expected_moves = self.__list_available_moves(data["field"])
        available_moves = rook.list_available_moves()
        assert available_moves == expected_moves

    def test_middle_field_valid_move_rook(self):
        middle_field = "D4"
        data = FigureFactory.build(field=middle_field)
        rook = Rook(**data)
        available_moves = self.__list_available_moves(data["field"])
        dest_field = f"D{int(rook.field[1]) - 1}"
        assert dest_field in available_moves

    def test_edge_field_valid_move_rook(self):
        edge_field = "H8"
        data = FigureFactory.build(field=edge_field)
        rook = Rook(**data)
        available_moves = self.__list_available_moves(data["field"])
        dest_field = f"H{int(rook.field[1]) - 3}"
        assert dest_field in available_moves

    def test_invalid_move_rook(self):
        data = FigureFactory.build()
        rook = Rook(**data)
        available_moves = self.__list_available_moves(data["field"])
        dest_field = f"A{int(rook.field[1]) - 1}"
        assert dest_field not in available_moves

    def __list_available_moves(self, field: str) -> list:
        available_moves = list()

        x, y = np.where(CHESS_BOARD == field)
        for x_shift, y_shift in CHESS_CARDINALS:
            x_temp, y_temp = x[0] + x_shift, y[0] + y_shift
            while is_in_bounds(x_temp, y_temp):
                available_moves.append((x_temp, y_temp))

                x_temp, y_temp = x_temp + x_shift, y_temp + y_shift

        available_move_y_position = np.transpose(available_moves)[0]
        available_move_x_position = np.transpose(available_moves)[1]

        available_moves = CHESS_BOARD[
            available_move_y_position, available_move_x_position
        ]
        return available_moves.tolist()

    class TestQueen:
        def test_list_available_moves_queen(self):
            data = FigureFactory.build()
            queen = Queen(**data)
            expected_moves = self.__list_available_moves(data["field"])
            available_moves = queen.list_available_moves()
            assert available_moves == expected_moves

        def test_edge_field_valid_move_queen(self):
            edge_field = "H8"
            data = FigureFactory.build(field=edge_field)
            queen = Queen(**data)
            available_moves = self.__list_available_moves(data["field"])
            dest_field = f"G{int(queen.field[1]) - 1}"
            assert dest_field in available_moves

        def test_middle_field_valid_move_queen(self):
            middle_field = "D4"
            data = FigureFactory.build(field=middle_field)
            queen = Queen(**data)
            available_moves = self.__list_available_moves(data["field"])
            dest_field = f"E{int(queen.field[1]) - 1}"
            assert dest_field in available_moves

        def test_invalid_move_queen(self):
            data = FigureFactory.build()
            queen = Queen(**data)
            available_moves = self.__list_available_moves(data["field"])
            dest_field = f"A{int(queen.field[1]) - 1}"
            assert dest_field not in available_moves

        def __list_available_moves(self, field: str) -> list:
            available_moves = list()

            x, y = np.where(CHESS_BOARD == field)
            for x_shift, y_shift in CHESS_DIAGONALS + CHESS_CARDINALS:
                x_temp, y_temp = x[0] + x_shift, y[0] + y_shift
                while is_in_bounds(x_temp, y_temp):
                    available_moves.append((x_temp, y_temp))

                    x_temp, y_temp = x_temp + x_shift, y_temp + y_shift

            available_move_y_position = np.transpose(available_moves)[0]
            available_move_x_position = np.transpose(available_moves)[1]

            available_moves = CHESS_BOARD[
                available_move_y_position, available_move_x_position
            ]
            return available_moves.tolist()

    class TestKing:
        def test_list_available_moves_king(self):
            data = FigureFactory.build()
            king = King(**data)
            expected_moves = self.__list_available_moves(data["field"])
            available_moves = king.list_available_moves()
            assert available_moves == expected_moves

        def test_middle_field_validate_move_king(self):
            middle_field = "D4"
            data = FigureFactory.build(field=middle_field)
            king = King(**data)
            available_moves = self.__list_available_moves(data["field"])
            dest_field = f"D{int(king.field[1]) + 1}"
            assert dest_field in available_moves

        def test_edge_field_validate_move_king(self):
            edge_field = "H8"
            data = FigureFactory.build(field=edge_field)
            king = King(**data)
            available_moves = self.__list_available_moves(data["field"])
            dest_field = f"H{int(king.field[1]) -1}"
            assert dest_field in available_moves

        def __list_available_moves(self, field: str) -> list:
            x, y = np.where(CHESS_BOARD == field)
            available_moves = list()
            for x_position, y_position in self.__king_list(x[0], y[0]):
                if is_in_bounds(x_position, y_position):
                    available_moves.append((x_position, y_position))
            available_move_y_position = np.transpose(available_moves)[0]
            available_move_x_position = np.transpose(available_moves)[1]
            available_moves = CHESS_BOARD[
                available_move_y_position, available_move_x_position
            ]
            return available_moves.tolist()

        def __king_list(self, x: int, y: int) -> list:
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
