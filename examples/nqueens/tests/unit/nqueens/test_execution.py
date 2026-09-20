import pytest

from stallworth_nqueens.common.benchmarking import BenchmarkResult
from stallworth_nqueens.execution import engine, runner


def test_collect_single_returns_result_metadata():
    def solver(problem_size):
        return problem_size + 1

    result = runner.collect_single(4, solver, "demo")

    assert result.domain == "nqueens"
    assert result.solver == "demo"
    assert result.success is True
    assert result.payload["problem_size"] == 4
    assert result.payload["solutions"] == 5
    assert result.time >= 0


def test_collect_single_with_timer_prints_status_line(capsys):
    def solver(problem_size):
        return problem_size

    result = runner.collect_single(4, solver, "demo", show_timer=True)

    captured = capsys.readouterr()
    assert result.solver == "demo"
    assert result.payload["solutions"] == 4
    assert "demo" in captured.out
    assert "running" in captured.out


def test_collect_single_captures_solver_failure_with_partial_metrics():
    def solver(problem_size, metrics):
        metrics.visit_state(2)
        metrics.consider_placement(6)
        raise RuntimeError(f"failed at n={problem_size}")

    result = runner.collect_single(4, solver, "demo")

    assert result.success is False
    assert result.payload["states_visited"] == 2
    assert result.payload["candidate_placements_considered"] == 6
    assert result.payload["failure_type"] == "RuntimeError"
    assert result.payload["failure_message"] == "failed at n=4"


def test_collect_all_sorts_results_and_computes_speedups(monkeypatch):
    calls = {}
    expected = [
        BenchmarkResult("nqueens", "fast", 1.0, True, {"solutions": 2, "speedup_best": 1.0, "speedup_baseline": 2.0}),
        BenchmarkResult("nqueens", "base", 2.0, True, {"solutions": 2, "speedup_best": 0.5, "speedup_baseline": 1.0}),
        BenchmarkResult("nqueens", "slow", 4.0, True, {"solutions": 2, "speedup_best": 0.25, "speedup_baseline": 0.5}),
    ]

    def fake_run_benchmarks(adapter, solvers, baseline_solver=None, **kwargs):
        calls["args"] = (adapter, solvers, baseline_solver, kwargs)
        return expected

    monkeypatch.setattr(runner, "run_benchmarks", fake_run_benchmarks)

    results = runner.collect_all(
        4,
        {
            "slow": object(),
            "fast": object(),
            "base": object(),
        },
        baseline_label="base",
    )

    assert results == expected
    assert calls["args"] == (
        runner.ADAPTER,
        ["slow", "fast", "base"],
        "base",
        {"n": 4},
    )
    assert [result.solver for result in results] == ["fast", "base", "slow"]
    assert results[0].payload["speedup_best"] == 1.0
    assert results[0].payload["speedup_baseline"] == 2.0
    assert results[2].payload["speedup_best"] == 0.25
    assert results[2].payload["speedup_baseline"] == 0.5


def test_collect_all_uses_best_time_when_baseline_is_missing(monkeypatch):
    expected = [
        BenchmarkResult("nqueens", "beta", 1.5, True, {"solutions": 2, "speedup_best": 1.0, "speedup_baseline": 1.0}),
        BenchmarkResult("nqueens", "alpha", 3.0, True, {"solutions": 2, "speedup_best": 0.5, "speedup_baseline": 0.5}),
    ]

    monkeypatch.setattr(
        runner,
        "run_benchmarks",
        lambda adapter, solvers, baseline_solver=None, **kwargs: expected,
    )

    results = runner.collect_all(
        4,
        {
            "alpha": object(),
            "beta": object(),
        },
        baseline_label="missing",
    )

    assert results == expected
    assert results[0].solver == "beta"
    assert results[0].payload["speedup_baseline"] == 1.0
    assert results[1].payload["speedup_baseline"] == 0.5


def test_runner_execute_solver_dispatches_to_registered_solver(monkeypatch):
    calls = {}
    expected_result = BenchmarkResult(
        "nqueens",
        "demo",
        0.1,
        True,
        {"solutions": 2},
    )

    def fake_run_benchmark(adapter, solver, **kwargs):
        calls["single"] = (adapter, solver, kwargs)
        return expected_result

    monkeypatch.setattr(runner, "run_benchmark", fake_run_benchmark)
    monkeypatch.setattr(runner, "SOLVERS", {"demo": object()})

    result = runner.execute_solver(4, "demo")

    assert calls["single"] == (runner.ADAPTER, "demo", {"n": 4})
    assert result == {
        "solver": "demo",
        "result": expected_result,
    }


def test_runner_execute_all_delegates_to_collect_all(monkeypatch):
    calls = []

    monkeypatch.setattr(runner, "SOLVERS", {"demo": object(), "other": object()})
    monkeypatch.setattr(
        runner,
        "execute_solver",
        lambda problem_size, solver_name: calls.append((problem_size, solver_name)) or {"solver": solver_name},
    )

    result = runner.execute_all(5, baseline_label="demo")

    assert calls == [
        (5, "demo"),
        (5, "other"),
    ]
    assert result == [
        {"solver": "demo"},
        {"solver": "other"},
    ]


def test_runner_execute_all_uses_selected_solver_names(monkeypatch):
    calls = []

    monkeypatch.setattr(runner, "SOLVERS", {"demo": object(), "other": object(), "third": object()})
    monkeypatch.setattr(
        runner,
        "execute_solver",
        lambda problem_size, solver_name: calls.append((problem_size, solver_name)) or {"solver": solver_name},
    )

    result = runner.execute_all(5, solver_names=["other", "demo"])

    assert calls == [
        (5, "other"),
        (5, "demo"),
    ]
    assert result == [
        {"solver": "other"},
        {"solver": "demo"},
    ]


def test_engine_execute_runs_all(monkeypatch):
    monkeypatch.setattr(
        engine,
        "execute_all",
        lambda problem_size, baseline_label=None, solver_names=None: [
            {"solver": "demo"}
        ],
    )

    result = engine.execute(4, "all", solver_names=["demo"], profile_name="standard")

    assert result["mode"] == "all"
    assert result["size"] == 4
    assert result["profile"] == "standard"
    assert result["results"] == [
        {"solver": "demo"}
    ]


def test_engine_execute_runs_single_solver(monkeypatch):
    monkeypatch.setattr(engine, "SOLVERS", {"demo": object()})
    monkeypatch.setattr(engine, "execute_solver", lambda problem_size, solver_name: {"solver": solver_name})

    result = engine.execute(4, "demo")

    assert result == {
        "mode": "single",
        "size": 4,
        "profile": None,
        "requested_solver": "demo",
        "result": {"solver": "demo"},
    }


def test_engine_execute_validates_inputs(monkeypatch):
    monkeypatch.setattr(engine, "SOLVERS", {"demo": object()})

    with pytest.raises(ValueError, match="Board size must be at least 1."):
        engine.execute(0, "demo")

    with pytest.raises(ValueError, match="Unknown solver: missing"):
        engine.execute(4, "missing")
