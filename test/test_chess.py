import pdb
import numpy as np
from objects.Figure import (
    chess_board,
    chessDiagonals,
    knight_list,
    Knight,
    Rook,
    chessCardinals,
    Queen,
    King,
    king_list,
    is_in_bounds,
)
from factories.figure_factory import FigureFactory
from objects.Figure import Pawn, Bishop


class TestPawn:
    def test_list_available_moves_pawn_out_of_board(self):
        data = FigureFactory.build(field="H9")
        expected_move = self.__list_available_moves(data["field"])
        pawn = Pawn(**data)
        available_moves, error = pawn.list_available_moves()
        assert available_moves == expected_move

    def test_list_available_moves_pawn(self):
        data = FigureFactory.build()
        expected_move = self.__list_available_moves(data["field"])
        pawn = Pawn(**data)
        available_moves = pawn.list_available_moves()
        assert available_moves[0] == expected_move[0]

    def test_valid_movement(self):
        data = FigureFactory.build()
        pawn = Pawn(**data)
        dest_field = f"{pawn.field[0]}{int(pawn.field[1]) + 1}"
        check_move_valid = pawn.validate_move(dest_field)
        assert check_move_valid == "Valid move"

    def test_invalid_movement_wrong_field_name(self):
        data = FigureFactory.build()
        pawn = Pawn(**data)
        dest_field = f"A{int(pawn.field[1]) + 1}"
        check_move_valid = pawn.validate_move(dest_field)
        assert check_move_valid == "Invalid move"

    def test_invalid_movement_wrong_field_number(self):
        data = FigureFactory.build()
        pawn = Pawn(**data)
        dest_field = f"{pawn.field[0]}{int(pawn.field[1]) - 3}"
        check_move_valid = pawn.validate_move(dest_field)
        assert check_move_valid == "Invalid move"

    def __list_available_moves(self, field: str) -> list:
        available_moves = list()
        field_number = int(field[1])
        field_name = field[0]
        new_field_number = field_number + 1
        if field_number < 8:
            available_moves.append(f"{field_name}{new_field_number}")
        return list(available_moves)


class TestBishop:
    def test_list_available_moves_bishop(self):
        data = FigureFactory.build()
        bishop = Bishop(**data)
        expected_moves = self.__list_available_moves(data["field"])
        available_moves = bishop.list_available_moves()
        # numpy arrays need to wrap them to list // might want to wrap before returning
        assert list(available_moves) == list(expected_moves)

    def test_valid_move_bishop(self):
        data = FigureFactory.build()
        bishop = Bishop(**data)
        available_moves = self.__list_available_moves(data["field"])
        if bishop.field == "H1":
            dest_field = f"G{int(bishop.field[1]) + 1}"
        else:
            dest_field = f"G{int(bishop.field[1]) - 1}"
        # numpy arrays need to wrap them to list // might want to wrap before returning
        assert dest_field in available_moves

    def test_invalid_move_bishop(self):
        data = FigureFactory.build()
        bishop = Bishop(**data)
        available_moves = self.__list_available_moves(data["field"])
        dest_field = f"A{int(bishop.field[1]) - 1}"
        # numpy arrays need to wrap them to list // might want to wrap before returning
        assert dest_field not in available_moves

    def __list_available_moves(self, field: str) -> list:
        available_moves = list()

        x, y = np.where(chess_board == field)
        for xint, yint in chessDiagonals:
            xtemp, ytemp = x[0] + xint, y[0] + yint
            while is_in_bounds(xtemp, ytemp):
                available_moves.append((xtemp, ytemp))

                xtemp, ytemp = xtemp + xint, ytemp + yint

        Y = np.transpose(available_moves)[0]
        X = np.transpose(available_moves)[1]

        available_moves = chess_board[Y, X]
        return available_moves


class TestKnight:
    def test_list_available_moves_knight(self):
        data = FigureFactory.build()
        knight = Knight(**data)
        expected_moves = self.__list_available_moves(data["field"])
        available_moves = knight.list_available_moves()
        # numpy arrays need to wrap them to list // might want to wrap before returning
        assert list(available_moves) == list(expected_moves)

    def test_validate_move_knight(self):
        data = FigureFactory.build()
        knight = Knight(**data)
        available_moves = self.__list_available_moves(data["field"])
        if knight.field[1] == "8":
            dest_field = f"F{int(knight.field[1]) - 1}"
        else:
            dest_field = f"F{int(knight.field[1]) + 1}"
        # numpy arrays need to wrap them to list // might want to wrap before returning
        assert dest_field in available_moves

    def __list_available_moves(self, field: str) -> list:
        x, y = np.where(chess_board == field)
        available_moves = list()
        for xx, yy in knight_list(x[0], y[0], 2, 1):
            if is_in_bounds(xx, yy):
                available_moves.append((xx, yy))
        Y = np.transpose(available_moves)[0]
        X = np.transpose(available_moves)[1]
        available_moves = chess_board[Y, X]
        return available_moves


class TestRook:
    def test_list_available_moves_rook(self):
        data = FigureFactory.build()
        rook = Rook(**data)
        expected_moves = self.__list_available_moves(data["field"])
        available_moves = rook.list_available_moves()
        # numpy arrays need to wrap them to list // might want to wrap before returning
        assert list(available_moves) == list(expected_moves)

    def test_valid_move_rook(self):
        data = FigureFactory.build()
        rook = Rook(**data)
        available_moves = self.__list_available_moves(data["field"])
        if rook.field == "H1":
            dest_field = f"H{int(rook.field[1]) + 1}"
        else:
            dest_field = f"H{int(rook.field[1]) - 1}"
        # numpy arrays need to wrap them to list // might want to wrap before returning
        assert dest_field in available_moves

    def test_invalid_move_rook(self):
        data = FigureFactory.build()
        rook = Rook(**data)
        available_moves = self.__list_available_moves(data["field"])
        dest_field = f"A{int(rook.field[1]) - 1}"
        # numpy arrays need to wrap them to list // might want to wrap before returning
        assert dest_field not in available_moves

    def __list_available_moves(self, field: str) -> list:
        available_moves = list()

        x, y = np.where(chess_board == field)
        for xint, yint in chessCardinals:
            xtemp, ytemp = x[0] + xint, y[0] + yint
            while is_in_bounds(xtemp, ytemp):
                available_moves.append((xtemp, ytemp))

                xtemp, ytemp = xtemp + xint, ytemp + yint

        Y = np.transpose(available_moves)[0]
        X = np.transpose(available_moves)[1]

        available_moves = chess_board[Y, X]
        return available_moves


    class TestQueen:
        def test_list_available_moves_queen(self):
            data = FigureFactory.build()
            queen = Queen(**data)
            expected_moves = self.__list_available_moves(data["field"])
            available_moves = queen.list_available_moves()
            # numpy arrays need to wrap them to list // might want to wrap before returning
            assert list(available_moves) == list(expected_moves)

        def test_valid_move_queen(self):
            data = FigureFactory.build()
            queen = Queen(**data)
            available_moves = self.__list_available_moves(data["field"])
            if queen.field == "H1":
                dest_field = f"G{int(queen.field[1]) + 1}"
            else:
                dest_field = f"G{int(queen.field[1]) - 1}"
            # numpy arrays need to wrap them to list // might want to wrap before returning
            assert dest_field in available_moves

        def test_invalid_move_queen(self):
            data = FigureFactory.build()
            queen = Queen(**data)
            available_moves = self.__list_available_moves(data["field"])
            dest_field = f"A{int(queen.field[1]) - 1}"
            # numpy arrays need to wrap them to list // might want to wrap before returning
            assert dest_field not in available_moves

        def __list_available_moves(self, field: str) -> list:
            available_moves = list()

            x, y = np.where(chess_board == field)
            for xint, yint in chessDiagonals + chessCardinals:
                xtemp, ytemp = x[0] + xint, y[0] + yint
                while is_in_bounds(xtemp, ytemp):
                    available_moves.append((xtemp, ytemp))

                    xtemp, ytemp = xtemp + xint, ytemp + yint

            Y = np.transpose(available_moves)[0]
            X = np.transpose(available_moves)[1]

            available_moves = chess_board[Y, X]
            return available_moves

    class TestKing:
        def test_list_available_moves_knight(self):
            data = FigureFactory.build()
            king = King(**data)
            expected_moves = self.__list_available_moves(data["field"])
            available_moves = king.list_available_moves()
            # numpy arrays need to wrap them to list // might want to wrap before returning
            assert list(available_moves) == list(expected_moves)

        def test_validate_move_knight(self):
            data = FigureFactory.build()
            king = King(**data)
            available_moves = self.__list_available_moves(data["field"])
            if king.field[1] == "8":
                dest_field = f"H{int(king.field[1]) - 1}"
            else:
                dest_field = f"H{int(king.field[1]) + 1}"
            # numpy arrays need to wrap them to list // might want to wrap before returning
            assert dest_field in available_moves

        def __list_available_moves(self, field: str) -> list:
            x, y = np.where(chess_board == field)
            available_moves = list()
            for xx, yy in king_list(x[0], y[0]):
                if is_in_bounds(xx, yy):
                    available_moves.append((xx, yy))
            Y = np.transpose(available_moves)[0]
            X = np.transpose(available_moves)[1]
            available_moves = chess_board[Y, X]
            return available_moves
