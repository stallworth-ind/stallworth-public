from stallworth_nqueens.common.benchmarking import (
    BenchmarkResult,
    CommonExecutionMetrics,
)


def test_common_execution_metrics_projects_only_demonstrated_fields():
    result = BenchmarkResult(
        domain="nqueens",
        solver="demo",
        time=0.125,
        success=False,
        payload={
            "failure_type": "RuntimeError",
            "failure_message": "captured",
            "states_visited": 12,
            "validation": "verified",
        },
    )

    assert CommonExecutionMetrics.from_benchmark_result(result) == (
        CommonExecutionMetrics(
            elapsed_seconds=0.125,
            execution_success=False,
            failure_type="RuntimeError",
            failure_message="captured",
        )
    )


