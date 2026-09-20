"""Shared helpers for set-based N-Queens constraint checks."""


def major_diagonal(row: int, col: int) -> int:
    """Return the major diagonal key for a board position."""
    return row - col


def minor_diagonal(row: int, col: int) -> int:
    """Return the minor diagonal key for a board position."""
    return row + col


def is_safe(row: int, col: int, cols, diag1, diag2) -> bool:
    """Return whether a queen can be placed at `(row, col)`."""
    return (
        col not in cols
        and major_diagonal(row, col) not in diag1
        and minor_diagonal(row, col) not in diag2
    )


def place(row: int, col: int, cols, diag1, diag2):
    """Return updated constraint sets after placing a queen."""
    return (
        cols | {col},
        diag1 | {major_diagonal(row, col)},
        diag2 | {minor_diagonal(row, col)},
    )


def valid_columns(row: int, n: int, cols, diag1, diag2) -> list[int]:
    """Return all safe columns for a row under the current constraints."""
    return [col for col in range(n) if is_safe(row, col, cols, diag1, diag2)]
