from typing import Any, Protocol

from stallworth_nqueens.common.benchmarking.models import BenchmarkResult


class DomainBenchmarkAdapter(Protocol):
    domain: str

    def run(self, solver: str, **kwargs: Any) -> Any:
        ...

    def to_benchmark_result(
        self,
        solver: str,
        raw_result: Any,
        elapsed: float,
        **kwargs: Any,
    ) -> BenchmarkResult:
        ...

    def to_failed_benchmark_result(
        self,
        solver: str,
        error: Exception,
        elapsed: float,
        **kwargs: Any,
    ) -> BenchmarkResult:
        ...
