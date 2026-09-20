# tests/nqueens/test_solvers.py

import pytest

from stallworth_nqueens.metrics import NQueensSearchMetrics
from stallworth_nqueens.solvers.registry import SOLVERS

KNOWN_COUNTS = {1: 1, 2: 0, 3: 0, 4: 2, 5: 10, 8: 92}


@pytest.mark.parametrize("solver_name", sorted(SOLVERS))
@pytest.mark.parametrize("n, expected", KNOWN_COUNTS.items())
def test_solver_matches_known_solution_counts(solver_name, n, expected):
    solver = SOLVERS[solver_name]
    assert solver(n) == expected


@pytest.mark.parametrize("solver_name", sorted(SOLVERS))
def test_solver_collects_common_search_metrics(solver_name):
    metrics = NQueensSearchMetrics()

    solutions = SOLVERS[solver_name](4, metrics=metrics)

    assert solutions == 2
    assert metrics.states_visited > 0
    assert metrics.candidate_placements_considered > 0


@pytest.mark.parametrize(
    ("solver_name", "expected_groups"),
    [
        (
            "dfs_backtracking",
            {"search_shape", "constraint", "backtracking"},
        ),
        (
            "constraint",
            {"search_shape", "constraint", "backtracking"},
        ),
        (
            "bitmask_backtracking",
            {"search_shape", "backtracking", "bitmask"},
        ),
    ],
)
def test_solver_collects_declared_capability_metric_contracts(
    solver_name,
    expected_groups,
):
    metrics = NQueensSearchMetrics()

    assert SOLVERS[solver_name](4, metrics=metrics) == 2

    payload = metrics.capability_metrics_payload()
    assert set(payload) == expected_groups
    assert payload["search_shape"] == {
        "schema_version": "1.0",
        "root_entries": 1,
        "leaf_states": 6,
        "child_states_entered": 16,
        "maximum_depth_reached": 4,
    }
