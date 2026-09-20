# tests/nqueens/test_board.py

import pytest

from stallworth_nqueens.models.board import NQueensBoard

def test_board_from_columns_sets_size_and_positions():
    board = NQueensBoard.from_columns([1, 3, 0, 2])

    assert board.size == 4
    assert board.columns_by_row == (1, 3, 0, 2)
    assert board.queen_positions == ((0, 1), (1, 3), (2, 0), (3, 2))


def test_board_detects_valid_solution():
    board = NQueensBoard.from_columns([1, 3, 0, 2])

    assert board.is_valid() is True


def test_board_detects_invalid_solution():
    board = NQueensBoard.from_columns([0, 1, 2, 3])

    assert board.is_valid() is False


def test_board_renders_ascii():
    board = NQueensBoard.from_columns([1, 3, 0, 2])

    assert board.to_ascii() == ". Q . .\n. . . Q\nQ . . .\n. . Q ."


def test_board_rejects_large_ascii_visualization():
    board = NQueensBoard.from_columns([0] * 11)

    with pytest.raises(ValueError, match="limited to boards of size 10 or smaller"):
        board.to_ascii()


def test_board_rejects_out_of_bounds_columns():
    with pytest.raises(ValueError, match="within board bounds"):
        NQueensBoard(4, (0, 1, 2, 4))
