import threading
import time

from stallworth_nqueens.common.benchmarking import run_benchmark, run_benchmarks
from stallworth_nqueens.benchmarking.adapter import NQueensAdapter
from stallworth_nqueens.metrics import execute_with_metrics
from stallworth_nqueens.solvers.registry import DEFAULT_BASELINE, SOLVERS


ADAPTER = NQueensAdapter()


def collect_single(problem_size, solver, label, show_timer=False):
    """Execute one raw N-Queens solver and convert it to a benchmark result.

    This helper preserves the older direct-solver flow used in tests and
    ad-hoc benchmarking while still normalizing output through the adapter.
    """
    start = time.perf_counter()

    if show_timer:
        running = True

        def timer():
            while running:
                elapsed = time.perf_counter() - start
                print(f"{label:<18} | running {elapsed:.2f}s", end="\r", flush=True)
                time.sleep(0.1)

        thread = threading.Thread(target=timer)
        thread.start()

    result = None
    error = None
    try:
        result = execute_with_metrics(solver, problem_size)
    except Exception as exc:
        error = exc
    finally:
        if show_timer:
            running = False
            thread.join()

    end = time.perf_counter()

    if error is not None:
        return ADAPTER.to_failed_benchmark_result(
            solver=label,
            error=error,
            elapsed=end - start,
            n=problem_size,
        )

    return ADAPTER.to_benchmark_result(
        solver=label,
        raw_result=result,
        elapsed=end - start,
        n=problem_size,
    )


def collect_all(problem_size, solvers, baseline_label=None):
    """Benchmark every registered N-Queens solver for a given board size."""
    return run_benchmarks(
        ADAPTER,
        list(solvers.keys()),
        baseline_solver=baseline_label,
        n=problem_size,
    )


def execute_solver(problem_size, solver_name):
    """Execute a named N-Queens solver through the shared benchmark runner."""
    if solver_name not in SOLVERS:
        raise ValueError(f"Unknown solver: {solver_name}")

    result = run_benchmark(
        ADAPTER,
        solver=solver_name,
        n=problem_size,
    )

    return {
        "solver": solver_name,
        "result": result,
    }


def execute_all(problem_size, baseline_label=DEFAULT_BASELINE, solver_names=None):
    """Run every selected N-Queens solver through the domain execution path."""
    selected_solver_names = list(solver_names) if solver_names is not None else list(SOLVERS.keys())
    return [
        execute_solver(problem_size, solver_name)
        for solver_name in selected_solver_names
    ]
