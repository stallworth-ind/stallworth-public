"""Recursive DFS backtracking solver for N-Queens.

Demonstrates the classic depth-first strategy of placing one queen per row,
then exploring and undoing moves as the search backtracks.
"""

from stallworth_nqueens.abstract.constraints import is_safe, major_diagonal, minor_diagonal
from stallworth_nqueens.metrics import NQueensSearchMetrics


def solve_n_queens(
    n: int,
    metrics: NQueensSearchMetrics | None = None,
) -> int:
    metrics = metrics or NQueensSearchMetrics()
    count = 0

    def backtrack(row, cols, diag1, diag2):
        nonlocal count
        metrics.enter_search_state(row, root=row == 0)

        if row == n:
            metrics.record_leaf_state()
            count += 1
            return

        child_count = 0
        for col in range(n):
            metrics.consider_placement()
            accepted = is_safe(row, col, cols, diag1, diag2)
            metrics.check_constraint(accepted=accepted)
            if not accepted:
                continue

            child_count += 1
            metrics.enter_child_state()
            cols.add(col)
            diag1.add(major_diagonal(row, col))
            diag2.add(minor_diagonal(row, col))
            backtrack(row + 1, cols, diag1, diag2)
            metrics.record_backtrack()
            cols.remove(col)
            diag1.remove(major_diagonal(row, col))
            diag2.remove(minor_diagonal(row, col))

        if child_count == 0:
            metrics.record_leaf_state()
            metrics.record_dead_end()

    backtrack(0, set(), set(), set())
    return count
