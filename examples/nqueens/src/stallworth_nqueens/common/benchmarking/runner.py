import time
from typing import Any

from stallworth_nqueens.common.benchmarking.adapters import DomainBenchmarkAdapter
from stallworth_nqueens.common.benchmarking.models import BenchmarkResult, annotate_speedups


def run_benchmark(
    adapter: DomainBenchmarkAdapter,
    solver: str,
    **kwargs: Any,
) -> BenchmarkResult:
    """Time one adapter-backed solver run and normalize its output."""
    start = time.perf_counter()
    try:
        raw_result = adapter.run(solver=solver, **kwargs)
    except Exception as exc:
        elapsed = time.perf_counter() - start
        failure_converter = getattr(
            adapter,
            "to_failed_benchmark_result",
            None,
        )
        if failure_converter is not None:
            return failure_converter(
                solver=solver,
                error=exc,
                elapsed=elapsed,
                **kwargs,
            )
        return BenchmarkResult(
            domain=adapter.domain,
            solver=solver,
            time=elapsed,
            success=False,
            payload={
                "failure_type": type(exc).__name__,
                "failure_message": str(exc),
            },
        )

    elapsed = time.perf_counter() - start
    return adapter.to_benchmark_result(
        solver=solver,
        raw_result=raw_result,
        elapsed=elapsed,
        **kwargs,
    )


def run_benchmarks(
    adapter: DomainBenchmarkAdapter,
    solvers: list[str],
    baseline_solver: str | None = None,
    **kwargs: Any,
) -> list[BenchmarkResult]:
    """Run and rank multiple solvers through a single domain adapter."""
    results = [
        run_benchmark(adapter, solver=solver, **kwargs)
        for solver in solvers
    ]
    results.sort(
        key=lambda result: (
            not result.success,
            result.time,
        )
    )
    return annotate_speedups(results, baseline_solver=baseline_solver)
