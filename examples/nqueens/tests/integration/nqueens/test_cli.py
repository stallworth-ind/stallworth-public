from stallworth_nqueens.common.benchmarking import BenchmarkResult
import sys
from argparse import Namespace

import pytest

from stallworth_nqueens.cli import n_queens_cli


def test_cli_prints_usage_when_arguments_are_missing(monkeypatch):
    calls = {}

    monkeypatch.setattr(sys, "argv", ["main.py"])
    monkeypatch.setattr(n_queens_cli, "get_solver_names", lambda: ["dfs_backtracking", 'constraint'])
    monkeypatch.setattr(n_queens_cli, "get_profile_names", lambda: ["standard", "toy"])
    monkeypatch.setattr(n_queens_cli, "setup_logging", lambda level: calls.setdefault("log_level", level))
    monkeypatch.setattr(n_queens_cli, "display_usage", lambda usage: calls.setdefault("usage", usage))

    assert n_queens_cli.run_n_queens_cli() == 1

    assert calls["log_level"] == "info"
    assert 'usage: stallworth-nqueens' in calls["usage"]
    assert 'Run N-Queens solvers' in calls["usage"]


def test_cli_prints_usage_for_malformed_arguments(monkeypatch):
    calls = {}

    monkeypatch.setattr(sys, "argv", ["main.py", "9", "9", "9", "bfs"])
    monkeypatch.setattr(n_queens_cli, "get_solver_names", lambda: ["dfs_backtracking", 'constraint'])
    monkeypatch.setattr(n_queens_cli, "get_profile_names", lambda: ["standard", "toy"])
    monkeypatch.setattr(n_queens_cli, "setup_logging", lambda level: calls.setdefault("log_level", level))
    monkeypatch.setattr(n_queens_cli, "display_usage", lambda usage: calls.setdefault("usage", usage))

    assert n_queens_cli.run_n_queens_cli() == 1

    assert calls["log_level"] == "info"
    assert 'usage: stallworth-nqueens' in calls["usage"]
    assert 'Run N-Queens solvers' in calls["usage"]


def test_cli_dispatches_all_to_execution_engine(monkeypatch):
    calls = {}
    args = Namespace(n=4, solver='all', log_level='info', profile=None)

    monkeypatch.setattr(n_queens_cli, "get_solver_names", lambda: ["dfs_backtracking", 'constraint'])
    monkeypatch.setattr(n_queens_cli, "get_profile_names", lambda: ["standard", "toy"])
    monkeypatch.setattr(n_queens_cli, "build_args", lambda solver_names, profile_names: args)
    monkeypatch.setattr(n_queens_cli, "setup_logging", lambda level: calls.setdefault("log_level", level))
    monkeypatch.setattr(n_queens_cli, "display_run_header", lambda size, profile_name=None: calls.setdefault("header", (size, profile_name)))
    def fake_execute(problem_size, choice, solver_names=None, profile_name=None):
        calls["execute"] = (problem_size, choice, solver_names, profile_name)
        return {
            "mode": "all",
            "size": problem_size,
            "results": [{'solver': 'dfs_backtracking', 'result': BenchmarkResult('nqueens', 'dfs_backtracking', 0.1, True, {'solutions': 2})}],
        }

    monkeypatch.setattr(n_queens_cli, "execute", fake_execute)
    monkeypatch.setattr(
        n_queens_cli,
        "display_execution_result",
        lambda result: calls.setdefault("display", result),
    )

    assert n_queens_cli.run_n_queens_cli() == 0

    assert calls["log_level"] == "info"
    assert calls["header"] == (4, None)
    assert calls["execute"] == (4, "all", None, None)
    assert calls["display"] == {
        "mode": "all",
        "size": 4,
        "results": [{'solver': 'dfs_backtracking', 'result': BenchmarkResult('nqueens', 'dfs_backtracking', 0.1, True, {'solutions': 2})}],
    }


def test_cli_dispatches_single_solver_to_execution_engine(monkeypatch):
    calls = {}
    args = Namespace(n=4, solver='bitmask_backtracking', log_level='debug', profile=None)

    monkeypatch.setattr(n_queens_cli, "get_solver_names", lambda: ['bitmask_backtracking'])
    monkeypatch.setattr(n_queens_cli, "get_profile_names", lambda: ["standard", "toy"])
    monkeypatch.setattr(n_queens_cli, "build_args", lambda solver_names, profile_names: args)
    monkeypatch.setattr(n_queens_cli, "setup_logging", lambda level: calls.setdefault("log_level", level))
    monkeypatch.setattr(n_queens_cli, "display_run_header", lambda size, profile_name=None: calls.setdefault("header", (size, profile_name)))
    def fake_execute(problem_size, choice, solver_names=None, profile_name=None):
        calls["execute"] = (problem_size, choice, solver_names, profile_name)
        return {
            "mode": "single",
            "size": problem_size,
            "result": {'solver': choice, 'result': BenchmarkResult('nqueens', choice, 0.1, True, {'solutions': 2})},
        }

    monkeypatch.setattr(n_queens_cli, "execute", fake_execute)
    monkeypatch.setattr(
        n_queens_cli,
        "display_execution_result",
        lambda result: calls.setdefault("display", result),
    )

    assert n_queens_cli.run_n_queens_cli() == 0

    assert calls["log_level"] == "debug"
    assert calls["header"] == (4, None)
    assert calls["execute"] == (4, 'bitmask_backtracking', None, None)
    assert calls["display"] == {
        "mode": "single",
        "size": 4,
        "result": {'solver': 'bitmask_backtracking', 'result': BenchmarkResult('nqueens', 'bitmask_backtracking', 0.1, True, {'solutions': 2})},
    }


def test_cli_uses_profile_defaults_and_solver_subset(monkeypatch):
    calls = {}
    args = Namespace(n=8, solver='all', log_level='info', profile='standard')

    class FakeProfile:
        solver_names = ("dfs_backtracking", 'bitmask_backtracking')

    monkeypatch.setattr(n_queens_cli, "get_solver_names", lambda: ["dfs_backtracking", 'bitmask_backtracking', 'constraint'])
    monkeypatch.setattr(n_queens_cli, "get_profile_names", lambda: ['standard'])
    monkeypatch.setattr(n_queens_cli, "build_args", lambda solver_names, profile_names: args)
    monkeypatch.setattr(n_queens_cli, "get_profile", lambda name: FakeProfile())
    monkeypatch.setattr(n_queens_cli, "setup_logging", lambda level: calls.setdefault("log_level", level))
    monkeypatch.setattr(n_queens_cli, "display_run_header", lambda size, profile_name=None: calls.setdefault("header", (size, profile_name)))

    def fake_execute(problem_size, choice, solver_names=None, profile_name=None):
        calls["execute"] = (problem_size, choice, solver_names, profile_name)
        return {"mode": "all", "size": problem_size, "results": [{'solver': 'dfs_backtracking', 'result': BenchmarkResult('nqueens', 'dfs_backtracking', 0.1, True, {'solutions': 2})}]}

    monkeypatch.setattr(n_queens_cli, "execute", fake_execute)
    monkeypatch.setattr(
        n_queens_cli,
        "display_execution_result",
        lambda result: calls.setdefault("display", result),
    )

    assert n_queens_cli.run_n_queens_cli() == 0

    assert calls["header"] == (8, 'standard')
    assert calls["execute"] == (8, "all", ("dfs_backtracking", 'bitmask_backtracking'), 'standard')








def test_cli_rejects_unknown_solver_with_suggestion(monkeypatch):
    calls = []
    args = Namespace(n=4, solver='bitmask_backtraking', log_level='info', profile=None)

    monkeypatch.setattr(n_queens_cli, "get_solver_names", lambda: ['bitmask_backtracking', 'constraint'])
    monkeypatch.setattr(n_queens_cli, "get_profile_names", lambda: ["standard", "toy"])
    monkeypatch.setattr(n_queens_cli, "build_args", lambda solver_names, profile_names: args)
    monkeypatch.setattr(n_queens_cli, "setup_logging", lambda level: None)
    monkeypatch.setattr(n_queens_cli, "display_run_header", lambda size, profile_name=None: calls.append(("header", size, profile_name)))

    def fake_execute(problem_size, choice, solver_names=None, profile_name=None):
        raise ValueError(f"Unknown solver: {choice}")

    monkeypatch.setattr(n_queens_cli, "execute", fake_execute)
    monkeypatch.setattr(
        n_queens_cli,
        "display_unknown_solver",
        lambda choice, suggestions, solver_names: calls.append(("unknown", choice, suggestions, solver_names)),
    )

    assert n_queens_cli.run_n_queens_cli() == 1

    assert ("header", 4, None) in calls
    assert ("unknown", 'bitmask_backtraking', ['bitmask_backtracking'], ['bitmask_backtracking', 'constraint']) in calls


def test_cli_exits_on_other_value_errors(monkeypatch):
    args = Namespace(n=0, solver='all', log_level='info', profile=None)
    messages = []

    monkeypatch.setattr(n_queens_cli, "get_solver_names", lambda: ["dfs_backtracking"])
    monkeypatch.setattr(n_queens_cli, "get_profile_names", lambda: ["standard", "toy"])
    monkeypatch.setattr(n_queens_cli, "build_args", lambda solver_names, profile_names: args)
    monkeypatch.setattr(n_queens_cli, "setup_logging", lambda level: None)
    monkeypatch.setattr(n_queens_cli, "display_run_header", lambda size, profile_name=None: None)
    monkeypatch.setattr(n_queens_cli, "execute", lambda problem_size, choice, solver_names=None, profile_name=None: (_ for _ in ()).throw(ValueError("Board size must be at least 1.")))
    monkeypatch.setattr(n_queens_cli, "display_unexpected_error", lambda message: messages.append(message))

    assert n_queens_cli.run_n_queens_cli() == 1

    assert messages == ["Board size must be at least 1."]


def test_cli_exits_on_unexpected_exception(monkeypatch):
    args = Namespace(n=4, solver='all', log_level='info', profile=None)
    messages = []

    monkeypatch.setattr(n_queens_cli, "get_solver_names", lambda: ["dfs_backtracking"])
    monkeypatch.setattr(n_queens_cli, "get_profile_names", lambda: ["standard", "toy"])
    monkeypatch.setattr(n_queens_cli, "build_args", lambda solver_names, profile_names: args)
    monkeypatch.setattr(n_queens_cli, "setup_logging", lambda level: None)
    monkeypatch.setattr(n_queens_cli, "display_run_header", lambda size, profile_name=None: None)
    monkeypatch.setattr(n_queens_cli, "execute", lambda problem_size, choice, solver_names=None, profile_name=None: (_ for _ in ()).throw(RuntimeError("boom")))
    monkeypatch.setattr(n_queens_cli, "display_unexpected_error", lambda message: messages.append(message))

    assert n_queens_cli.run_n_queens_cli() == 1

    assert messages == ["Unexpected error (RuntimeError): boom"]
