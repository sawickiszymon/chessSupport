from flask import Flask

from utils import FieldOutOfBoundsError

app = Flask(__name__)

from objects.Figure import *

CLASS_NAMES = {
    "pawn": Pawn,
    "rook": Rook,
    "king": King,
    "knight": Knight,
    "queen": Queen,
    "bishop": Bishop,
}


@app.route("/")
def hello_world():
    return "Hello World"


@app.route("/api/v1/<chess_figure>/<current_field>")
def handle_available_moves(chess_figure: str, current_field: str):
    error = None
    available_moves = list()
    if chess_figure not in CLASS_NAMES:
        return (
            get_json_object_list(available_moves, error, chess_figure, current_field),
            404,
        )

    context = Context(CLASS_NAMES[chess_figure](current_field))
    try:
        available_moves = context.list_moves()
    except FieldOutOfBoundsError as err:
        error = err.args[0]
        return (
            get_json_object_list(available_moves, error, chess_figure, current_field),
            409,
        )
    return (
        get_json_object_list(available_moves, error, chess_figure, current_field),
        200,
    )


@app.route("/api/v1/<chess_figure>/<current_field>/<dest_field>")
def handle_validate_move(chess_figure: str, current_field: str, dest_field: str):
    error = None
    move = None
    if chess_figure not in CLASS_NAMES:
        return (
            get_json_object_list(move, error, chess_figure, current_field),
            404,
        )
    context = Context(CLASS_NAMES[chess_figure](current_field))
    try:
        context.validate_move(dest_field)
        move = "valid"
    except (MoveNotPermittedError, FieldOutOfBoundsError) as err:
        move = "invalid"
        error = err.args[0]
        return (
            get_json_object_validate(
                move, error, chess_figure, current_field, dest_field
            ),
            409,
        )
    return (
        get_json_object_validate(move, error, chess_figure, current_field, dest_field),
        200,
    )


def get_json_object_list(moves, error, figure, current_field):
    return dict(
        availableMoves=moves, error=error, figure=figure, currentField=current_field
    )


def get_json_object_validate(moves, error, figure, current_field, dest_field):
    return dict(
        move=moves,
        figure=figure,
        error=error,
        currentField=current_field,
        destField=dest_field,
    )


if __name__ == "__main__":
    app.run()
