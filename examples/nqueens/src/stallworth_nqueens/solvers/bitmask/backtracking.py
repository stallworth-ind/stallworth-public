"""Bitmask backtracking solver for N-Queens.

Demonstrates how bit operations can replace sets for fast tracking of blocked
columns and diagonals during recursive search.
"""

from stallworth_nqueens.abstract.bitmask import available_positions, full_mask, next_state
from stallworth_nqueens.metrics import NQueensSearchMetrics


def solve_n_queens(
    n: int,
    metrics: NQueensSearchMetrics | None = None,
) -> int:
    metrics = metrics or NQueensSearchMetrics()
    full = full_mask(n)

    def solve(cols, diag1, diag2, depth=0):
        metrics.enter_search_state(depth, root=depth == 0)
        if cols == full:
            metrics.record_leaf_state()
            return 1

        available = available_positions(full, cols, diag1, diag2)
        metrics.compute_available_mask(available)
        total = 0
        child_count = 0

        while available:
            metrics.consider_placement()
            metrics.extract_candidate_bit()
            bit = available & -available
            available -= bit
            child_count += 1
            metrics.enter_child_state()
            total += solve(
                *next_state(cols, diag1, diag2, bit),
                depth + 1,
            )
            metrics.record_backtrack()

        if child_count == 0:
            metrics.record_leaf_state()
            metrics.record_dead_end()
        return total

    return solve(0, 0, 0)
