import sys

import pytest

from stallworth_nqueens.main import main
from stallworth_nqueens.execution.engine import execute
from stallworth_nqueens.models.board import NQueensBoard
from stallworth_nqueens.profiles.registry import get_profile, get_profile_names
from stallworth_nqueens.solvers.registry import SOLVERS


def test_example_registry_and_profiles_are_explicit():
    expected = ("dfs_backtracking", "constraint", "bitmask_backtracking")
    assert tuple(SOLVERS) == expected
    assert get_profile_names() == ["toy", "standard"]
    for name, size in (("toy", 4), ("standard", 8)):
        profile = get_profile(name)
        assert profile.problem_size == size
        assert profile.solver_names == expected
        assert profile.baseline_solver == "dfs_backtracking"


@pytest.mark.parametrize("profile", ["toy", "standard"])
def test_profile_cli_completes(monkeypatch, profile):
    monkeypatch.setattr(sys, "argv", ["stallworth-nqueens", "--profile", profile])
    assert main() == 0


@pytest.mark.parametrize("profile_name, expected_count", [("toy", 2), ("standard", 92)])
def test_profile_solvers_agree_and_preserve_observations(profile_name, expected_count):
    profile = get_profile(profile_name)
    execution = execute(profile.problem_size, "all", solver_names=profile.solver_names, profile_name=profile_name)
    assert execution["profile"] == profile_name
    assert tuple(entry["solver"] for entry in execution["results"]) == profile.solver_names
    groups = {
        "dfs_backtracking": {"search_shape", "constraint", "backtracking"},
        "constraint": {"search_shape", "constraint", "backtracking"},
        "bitmask_backtracking": {"search_shape", "backtracking", "bitmask"},
    }
    for entry in execution["results"]:
        result = entry["result"]
        assert result.success
        assert result.payload["solutions"] == expected_count
        assert result.time >= 0
        assert result.payload["states_visited"] > 0
        assert result.payload["candidate_placements_considered"] > 0
        assert set(result.payload["capability_metrics"]) == groups[entry["solver"]]
        board = NQueensBoard.from_columns(result.payload["sample_solution"])
        assert len(result.payload["sample_solution"]) == profile.problem_size
        assert board.is_valid()


@pytest.mark.parametrize("arguments", [
    [], ["0", "dfs_backtracking"], ["4", "missing"],
    ["--profile", "missing"], ["4", "all", "--report"],
    ["4", "all", "--watermark"], ["4", "all", "--archive-dir", "reports"],
])
def test_invalid_arguments_fail(monkeypatch, arguments):
    monkeypatch.setattr(sys, "argv", ["stallworth-nqueens", *arguments])
    assert main() == 1


def test_help_exits_successfully(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["stallworth-nqueens", "--help"])
    with pytest.raises(SystemExit) as exc:
        main()
    assert exc.value.code == 0
    help_text = capsys.readouterr().out
    assert "stallworth-nqueens" in help_text
    assert "--report" not in help_text


@pytest.mark.parametrize("choice", ["dfs_backtracking", "all"])
def test_captured_solver_failure_reaches_entry_point(monkeypatch, choice):
    def fail(n, metrics):
        metrics.visit_state()
        raise RuntimeError("example failure")

    monkeypatch.setitem(SOLVERS, "dfs_backtracking", fail)
    monkeypatch.setattr(sys, "argv", ["stallworth-nqueens", "4", choice])
    assert main() == 1
