import pytest

from stallworth_nqueens.common.benchmarking.runner import run_benchmark
from stallworth_nqueens.benchmarking.adapter import NQueensAdapter, find_sample_solution
from stallworth_nqueens.metrics import (
    CAPABILITY_METRIC_SCHEMA_VERSIONS,
    NQueensSearchMetrics,
    NQueensSolverExecution,
)


def test_find_sample_solution_returns_valid_board_for_solvable_size():
    solution = find_sample_solution(4)

    assert solution is not None
    assert len(solution) == 4


def test_find_sample_solution_returns_none_when_unsolvable():
    assert find_sample_solution(2) is None


def test_adapter_runs_registered_solver(monkeypatch):
    adapter = NQueensAdapter()
    calls = []

    monkeypatch.setattr(
        'stallworth_nqueens.benchmarking.adapter.SOLVERS',
        {"demo": lambda n: calls.append(n) or 9},
    )

    result = adapter.run("demo", n=8)

    assert result.solution_count == 9
    assert result.metrics == NQueensSearchMetrics()
    assert calls == [8]


def test_capability_contract_versions_are_independent_and_ordered():
    assert CAPABILITY_METRIC_SCHEMA_VERSIONS == {
        "search_shape": "1.0",
        "constraint": "1.0",
        "backtracking": "1.0",
        "bitmask": "1.0",
    }


def test_adapter_rejects_unknown_solver():
    adapter = NQueensAdapter()

    with pytest.raises(ValueError, match="Unknown solver: missing"):
        adapter.run("missing", n=8)


def test_adapter_converts_raw_result_to_benchmark_result():
    adapter = NQueensAdapter()

    result = adapter.to_benchmark_result(
        solver="demo",
        raw_result=92,
        elapsed=0.25,
        n=8,
    )

    assert result.domain == "nqueens"
    assert result.solver == "demo"
    assert result.time == 0.25
    assert result.success is True
    assert result.payload == {
        "problem_size": 8,
        "solutions": 92,
        "sample_solution": (0, 4, 7, 5, 2, 6, 1, 3),
        "states_visited": None,
        "candidate_placements_considered": None,
    }


def test_adapter_converts_instrumented_solver_result():
    adapter = NQueensAdapter()

    result = adapter.to_benchmark_result(
        solver="demo",
        raw_result=NQueensSolverExecution(
            solution_count=2,
            metrics=NQueensSearchMetrics(
                states_visited=17,
                candidate_placements_considered=40,
            ),
        ),
        elapsed=0.25,
        n=4,
    )

    assert result.payload["solutions"] == 2
    assert result.payload["states_visited"] == 17
    assert result.payload["candidate_placements_considered"] == 40


def test_adapter_serializes_only_observed_capability_metric_groups():
    adapter = NQueensAdapter()
    metrics = NQueensSearchMetrics()
    metrics.enter_search_state(0, root=True)
    metrics.enter_child_state()
    metrics.enter_search_state(1)
    metrics.record_leaf_state()
    metrics.check_constraint(accepted=False)
    metrics.record_backtrack()
    metrics.record_dead_end()
    metrics.compute_available_mask(0)
    metrics.extract_candidate_bit()

    result = adapter.to_benchmark_result(
        solver="demo",
        raw_result=NQueensSolverExecution(
            solution_count=0,
            metrics=metrics,
        ),
        elapsed=0.25,
        n=2,
    )

    assert set(result.payload["capability_metrics"]) == {
        "search_shape",
        "constraint",
        "backtracking",
        "bitmask",
    }
    assert result.payload["capability_metrics"]["search_shape"] == {
        "schema_version": "1.0",
        "root_entries": 1,
        "leaf_states": 1,
        "child_states_entered": 1,
        "maximum_depth_reached": 1,
    }
    assert "capability_metrics" not in adapter.to_benchmark_result(
        solver="legacy",
        raw_result=0,
        elapsed=0.25,
        n=2,
    ).payload


def test_adapter_captures_failure_with_partial_metrics(monkeypatch):
    def failing_solver(n, metrics):
        metrics.enter_search_state(0, root=True)
        metrics.visit_state(2)
        metrics.consider_placement(7)
        metrics.check_constraint(accepted=False)
        raise RuntimeError(f"failed at n={n}")

    monkeypatch.setattr(
        'stallworth_nqueens.benchmarking.adapter.SOLVERS',
        {"failing": failing_solver},
    )

    result = run_benchmark(NQueensAdapter(), "failing", n=8)

    assert result.success is False
    assert result.payload["solutions"] is None
    assert result.payload["states_visited"] == 3
    assert result.payload["candidate_placements_considered"] == 7
    assert set(result.payload["capability_metrics"]) == {
        "search_shape",
        "constraint",
    }
    assert (
        result.payload["capability_metrics"]["constraint"]
        ["constraint_checks"]
        == 1
    )
    assert result.payload["failure_type"] == "RuntimeError"
    assert result.payload["failure_message"] == "failed at n=8"
