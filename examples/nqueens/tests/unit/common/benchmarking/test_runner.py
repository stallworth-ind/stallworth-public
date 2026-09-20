from stallworth_nqueens.common.benchmarking import BenchmarkResult
from stallworth_nqueens.common.benchmarking.runner import run_benchmark, run_benchmarks


class FakeAdapter:
    domain = "fake"

    def __init__(self):
        self.calls = []

    def run(self, solver: str, **kwargs):
        self.calls.append(("run", solver, kwargs))
        return kwargs["value"] + 1

    def to_benchmark_result(self, solver: str, raw_result, elapsed: float, **kwargs):
        self.calls.append(("convert", solver, raw_result, kwargs))
        return BenchmarkResult(
            domain="nqueens",
            solver=solver,
            time=elapsed,
            success=True,
            payload={"value": raw_result},
        )


def test_run_benchmark_times_adapter_and_converts_result():
    adapter = FakeAdapter()

    result = run_benchmark(adapter, "demo", value=4)

    assert result.domain == "nqueens"
    assert result.solver == "demo"
    assert result.success is True
    assert result.payload["value"] == 5
    assert result.time >= 0
    assert adapter.calls[0] == ("run", "demo", {"value": 4})
    assert adapter.calls[1][0:3] == ("convert", "demo", 5)


def test_run_benchmarks_sorts_and_annotates_speedups(monkeypatch):
    fake_results = {
        "slow": BenchmarkResult("nqueens", "slow", 4.0, True, {"solutions": 2}),
        "fast": BenchmarkResult("nqueens", "fast", 1.0, True, {"solutions": 2}),
        "base": BenchmarkResult("nqueens", "base", 2.0, True, {"solutions": 2}),
    }

    monkeypatch.setattr(
        'stallworth_nqueens.common.benchmarking.runner.run_benchmark',
        lambda adapter, solver, **kwargs: fake_results[solver],
    )

    results = run_benchmarks(
        FakeAdapter(),
        ["slow", "fast", "base"],
        baseline_solver="base",
        value=1,
    )

    assert [result.solver for result in results] == ["fast", "base", "slow"]
    assert results[0].payload["speedup_best"] == 1.0
    assert results[0].payload["speedup_baseline"] == 2.0
    assert results[2].payload["speedup_best"] == 0.25


def test_run_benchmark_captures_unhandled_adapter_failure():
    class FailingAdapter(FakeAdapter):
        domain = "nqueens"

        def run(self, solver: str, **kwargs):
            raise RuntimeError("solver exploded")

    result = run_benchmark(FailingAdapter(), "broken", value=4)

    assert result.success is False
    assert result.payload == {
        "failure_type": "RuntimeError",
        "failure_message": "solver exploded",
    }


def test_run_benchmarks_continues_after_solver_failure():
    class MixedAdapter(FakeAdapter):
        domain = "nqueens"

        def run(self, solver: str, **kwargs):
            if solver == "broken":
                raise RuntimeError("solver exploded")
            return kwargs["value"]

    results = run_benchmarks(
        MixedAdapter(),
        ["broken", "working"],
        value=2,
    )

    assert [result.solver for result in results] == [
        "working",
        "broken",
    ]
    assert results[0].success is True
    assert results[1].success is False


def test_run_benchmarks_ranks_successes_and_leaves_failures_unranked(
    monkeypatch,
):
    fake_results = {
        "failed": BenchmarkResult(
            "nqueens",
            "failed",
            0.01,
            False,
            {"solutions": None},
        ),
        "fast": BenchmarkResult(
            "nqueens",
            "fast",
            1.0,
            True,
            {"solutions": 2},
        ),
        "base": BenchmarkResult(
            "nqueens",
            "base",
            2.0,
            True,
            {"solutions": 2},
        ),
    }
    monkeypatch.setattr(
        'stallworth_nqueens.common.benchmarking.runner.run_benchmark',
        lambda adapter, solver, **kwargs: fake_results[solver],
    )

    results = run_benchmarks(
        FakeAdapter(),
        ["failed", "fast", "base"],
        baseline_solver="base",
        value=1,
    )

    assert [result.solver for result in results] == [
        "fast",
        "base",
        "failed",
    ]
    assert results[0].payload["speedup_baseline"] == 2.0
    assert results[2].payload["speedup_best"] is None
    assert results[2].payload["speedup_baseline"] is None
