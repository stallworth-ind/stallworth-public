from dataclasses import dataclass, field
from typing import Any, Literal


DomainName = Literal["nqueens"]


@dataclass
class BenchmarkResult:
    domain: DomainName
    solver: str
    time: float
    success: bool
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class CommonExecutionMetrics:
    'Common execution observations for the N-Queens example.'

    elapsed_seconds: float
    execution_success: bool
    failure_type: str | None
    failure_message: str | None

    @classmethod
    def from_benchmark_result(
        cls,
        result: BenchmarkResult,
    ) -> "CommonExecutionMetrics":
        """Project only fields with equivalent adapter-level semantics."""

        raw_failure_type = result.payload.get("failure_type")
        raw_failure_message = result.payload.get("failure_message")
        return cls(
            elapsed_seconds=result.time,
            execution_success=result.success,
            failure_type=(
                raw_failure_type
                if isinstance(raw_failure_type, str)
                else None
            ),
            failure_message=(
                raw_failure_message
                if isinstance(raw_failure_message, str)
                else None
            ),
        )


def annotate_speedups(
    results: list[BenchmarkResult],
    baseline_solver: str | None = None,
) -> list[BenchmarkResult]:
    if not results:
        return results

    comparable = [
        result
        for result in results
        if result.success and result.time > 0
    ]
    if not comparable:
        return results

    best_time = min(result.time for result in comparable)
    baseline_entry = next(
        (
            result
            for result in comparable
            if result.solver == baseline_solver
        ),
        None,
    )
    baseline_time = baseline_entry.time if baseline_entry else best_time

    for result in results:
        if not result.success or result.time <= 0:
            result.payload["speedup_best"] = None
            result.payload["speedup_baseline"] = None
            continue
        result.payload["speedup_best"] = best_time / result.time
        result.payload["speedup_baseline"] = baseline_time / result.time

    return results
