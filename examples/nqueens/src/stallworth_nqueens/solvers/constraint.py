"""Constraint-based solver for N-Queens.

Demonstrates forward-checking by carrying the remaining available columns and
pruning invalid moves before exploring deeper states.
"""

from stallworth_nqueens.abstract.constraints import minor_diagonal, major_diagonal
from stallworth_nqueens.metrics import NQueensSearchMetrics


def solve_n_queens(
    n: int,
    metrics: NQueensSearchMetrics | None = None,
) -> int:
    metrics = metrics or NQueensSearchMetrics()

    def backtrack(row, available_cols, diag1, diag2):
        metrics.enter_search_state(row, root=row == 0)
        if row == n:
            metrics.record_leaf_state()
            return 1

        total = 0
        child_count = 0

        for col in available_cols:
            metrics.consider_placement()
            accepted = not (
                major_diagonal(row, col) in diag1
                or minor_diagonal(row, col) in diag2
            )
            metrics.check_constraint(accepted=accepted)
            if not accepted:
                continue

            child_count += 1
            metrics.enter_child_state()
            total += backtrack(
                row + 1,
                available_cols - {col},
                diag1 | {major_diagonal(row, col)},
                diag2 | {minor_diagonal(row, col)}
            )
            metrics.record_backtrack()

        if child_count == 0:
            metrics.record_leaf_state()
            metrics.record_dead_end()
        return total

    return backtrack(0, set(range(n)), set(), set())
