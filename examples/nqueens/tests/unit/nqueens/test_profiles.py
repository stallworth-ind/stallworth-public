import pytest

from stallworth_nqueens.profiles.registry import get_profile, get_profile_names


def test_get_profile_names_lists_registered_profiles():
    assert get_profile_names() == ['toy', 'standard']


def test_get_profile_returns_named_profile():
    profile = get_profile("standard")
    assert profile.problem_size == 8
    assert profile.default_solver == "all"
    assert profile.solver_names == ('dfs_backtracking', 'constraint', 'bitmask_backtracking')
    assert profile.baseline_solver == "dfs_backtracking"
    assert profile.comparison_metric_groups == ('common', 'search_shape', 'constraint', 'backtracking', 'bitmask')




def test_get_profile_rejects_unknown_name():
    with pytest.raises(ValueError, match="Unknown profile: missing"):
        get_profile("missing")
