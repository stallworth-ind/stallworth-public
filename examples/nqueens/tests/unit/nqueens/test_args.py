import sys

from stallworth_nqueens.cli.args import build_args, format_usage


def test_build_args_parses_required_values(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["nqueens", "8", 'constraint'])

    args = build_args(['constraint', "dfs_backtracking"], ["standard", "toy"])

    assert args.n == 8
    assert args.solver == 'constraint'
    assert args.log_level == "info"


def test_build_args_parses_optional_log_level(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["nqueens", "8", 'constraint', "--log-level", "debug"])

    args = build_args(['constraint', "dfs_backtracking"], ["standard", "toy"])

    assert args.log_level == "debug"










def test_build_args_uses_profile_defaults(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["nqueens", "--profile", "standard"])

    args = build_args(['constraint', "dfs_backtracking"], ["standard", "toy"])

    assert args.profile == "standard"
    assert args.n == 8
    assert args.solver == "all"


def test_format_usage_lists_available_solvers():
    usage = format_usage(["dfs_backtracking", 'constraint'], ["standard", "toy"])

    assert 'usage: stallworth-nqueens' in usage
    assert 'Run N-Queens solvers' in usage
    assert 'constraint' in usage
    assert "--profile" in usage
    assert '--report' not in usage
    assert '--watermark' not in usage
    assert '--archive-dir' not in usage
