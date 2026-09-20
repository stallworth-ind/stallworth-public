"""Shared helpers for bitmask-based N-Queens solvers."""


def full_mask(n: int) -> int:
    return (1 << n) - 1


def available_positions(full: int, cols: int, diag1: int, diag2: int) -> int:
    return ~(cols | diag1 | diag2) & full


def next_state(cols: int, diag1: int, diag2: int, bit: int) -> tuple[int, int, int]:
    return (
        cols | bit,
        (diag1 | bit) << 1,
        (diag2 | bit) >> 1,
    )
