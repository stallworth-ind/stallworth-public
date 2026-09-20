from stallworth_nqueens.common.benchmarking import BenchmarkResult
from stallworth_nqueens.metrics import (
    NQueensSolverExecution,
    NQueensSolverFailure,
    execute_with_metrics,
)
from stallworth_nqueens.solvers.registry import SOLVERS


def find_sample_solution(n: int) -> tuple[int, ...] | None:
    """Return one valid N-Queens placement for display, if one exists."""
    columns: list[int] = []
    used_cols: set[int] = set()
    used_diag1: set[int] = set()
    used_diag2: set[int] = set()

    def backtrack(row: int) -> bool:
        if row == n:
            return True

        for col in range(n):
            diag1 = row - col
            diag2 = row + col

            if col in used_cols or diag1 in used_diag1 or diag2 in used_diag2:
                continue

            columns.append(col)
            used_cols.add(col)
            used_diag1.add(diag1)
            used_diag2.add(diag2)

            if backtrack(row + 1):
                return True

            columns.pop()
            used_cols.remove(col)
            used_diag1.remove(diag1)
            used_diag2.remove(diag2)

        return False

    if backtrack(0):
        return tuple(columns)

    return None


class NQueensAdapter:
    """Translate N-Queens solver execution into shared benchmark results."""

    domain = "nqueens"

    def run(self, solver: str, **kwargs):
        """Execute a registered N-Queens solver using the shared adapter contract."""
        n = kwargs["n"]

        if solver not in SOLVERS:
            raise ValueError(f"Unknown solver: {solver}")

        return execute_with_metrics(SOLVERS[solver], n)

    def to_benchmark_result(
        self,
        solver: str,
        raw_result,
        elapsed: float,
        **kwargs,
    ) -> BenchmarkResult:
        """Convert a raw N-Queens solution count into a normalized benchmark record."""
        n = kwargs["n"]
        if isinstance(raw_result, NQueensSolverExecution):
            solution_count = raw_result.solution_count
            states_visited = raw_result.metrics.states_visited
            candidates_considered = (
                raw_result.metrics.candidate_placements_considered
            )
            capability_metrics = (
                raw_result.metrics.capability_metrics_payload()
            )
        else:
            solution_count = raw_result
            states_visited = None
            candidates_considered = None
            capability_metrics = None

        sample_solution = (
            find_sample_solution(n)
            if solution_count > 0
            else None
        )

        payload = {
            "problem_size": n,
            "solutions": solution_count,
            "sample_solution": sample_solution,
            "states_visited": states_visited,
            "candidate_placements_considered": candidates_considered,
        }
        if capability_metrics:
            payload["capability_metrics"] = capability_metrics

        return BenchmarkResult(
            domain="nqueens",
            solver=solver,
            time=elapsed,
            success=True,
            payload=payload,
        )

    def to_failed_benchmark_result(
        self,
        solver: str,
        error: Exception,
        elapsed: float,
        **kwargs,
    ) -> BenchmarkResult:
        """Convert a solver exception into a reportable failed result."""

        n = kwargs["n"]
        if isinstance(error, NQueensSolverFailure):
            cause = error.cause
            states_visited = error.metrics.states_visited
            candidates_considered = (
                error.metrics.candidate_placements_considered
            )
            capability_metrics = error.metrics.capability_metrics_payload()
        else:
            cause = error
            states_visited = None
            candidates_considered = None
            capability_metrics = None

        payload = {
            "problem_size": n,
            "solutions": None,
            "sample_solution": None,
            "states_visited": states_visited,
            "candidate_placements_considered": candidates_considered,
            "failure_type": type(cause).__name__,
            "failure_message": str(cause),
        }
        if capability_metrics:
            payload["capability_metrics"] = capability_metrics

        return BenchmarkResult(
            domain="nqueens",
            solver=solver,
            time=elapsed,
            success=False,
            payload=payload,
        )
