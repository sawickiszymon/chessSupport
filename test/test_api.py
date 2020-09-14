from app import app


def test_get_list_available_moves_response_200():
    response = app.test_client().get("/api/v1/rook/H4")
    assert response.status_code == 200


def test_get_list_available_moves_wrong_position_response_409():
    response = app.test_client().get("/api/v1/rook/H9")
    assert response.status_code == 409


def test_get_list_available_moves_invalid_figure_response_404():
    response = app.test_client().get("/api/v1/paulatubyla/H9")
    assert response.status_code == 404


def test_get_validate_move_wrong_position_response_409():
    response = app.test_client().get("/api/v1/rook/H10/H9")
    error = get_error(response)
    assert response.status_code == 409 and error == "Field does not exist."


def test_get_validate_move_wrong_destination_field_response_409():
    response = app.test_client().get("/api/v1/rook/H7/S4")
    error = get_error(response)
    assert response.status_code == 409 and error == "Current move is not permitted."


def test_get_validate_move_wrong_destination_field_response_invalid_figure_response_404():
    response = app.test_client().get("/api/v1/paulatubyla/H2/G1")
    assert response.status_code == 404


def test_get_validate_valid_move_rook_response_200():
    response = app.test_client().get("/api/v1/rook/H4/H3")
    assert response.status_code == 200


def test_get_validate_valid_move_pawn_response_200():
    response = app.test_client().get("/api/v1/pawn/H4/H5")
    assert response.status_code == 200


def test_get_validate_valid_move_queen_response_200():
    response = app.test_client().get("/api/v1/queen/H4/H3")
    assert response.status_code == 200


def test_get_validate_valid_move_king_response_200():
    response = app.test_client().get("/api/v1/rook/H4/H3")
    assert response.status_code == 200


def test_get_validate_valid_move_bishop_response_200():
    response = app.test_client().get("/api/v1/bishop/H4/G3")
    assert response.status_code == 200


def test_get_validate_valid_move_knight_response_409():
    response = app.test_client().get("/api/v1/knight/H4/F3")
    assert response.status_code == 200


def test_get_validate_invalid_move_rook_response_409():
    response = app.test_client().get("/api/v1/rook/H4/G3")
    assert response.status_code == 409


def test_get_validate_invalid_move_knight_response_409():
    response = app.test_client().get("/api/v1/knight/H4/A5")
    assert response.status_code == 409


def test_get_validate_invalid_move_king_response_409():
    response = app.test_client().get("/api/v1/king/H4/H6")
    assert response.status_code == 409


def test_get_validate_invalid_move_bishop_response_409():
    response = app.test_client().get("/api/v1/king/H4/H6")
    assert response.status_code == 409


def test_get_validate_invalid_move_pawn_response_409():
    response = app.test_client().get("/api/v1/pawn/H4/H7")
    assert response.status_code == 409


def get_error(response: app.response_class) -> str:
    body = response.json
    return body["error"]
