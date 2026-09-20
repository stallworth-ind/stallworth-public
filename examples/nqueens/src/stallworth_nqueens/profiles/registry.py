from dataclasses import dataclass


@dataclass(frozen=True)
class NQueensProfile:
    """Named preset for common N-Queens runs."""

    name: str
    problem_size: int
    default_solver: str = "all"
    solver_names: tuple[str, ...] | None = None
    description: str = ""
    baseline_solver: str = "dfs_backtracking"
    comparison_metric_groups: tuple[str, ...] = ("common",)
    finding_priorities: tuple[str, ...] = (
        "elapsed_seconds",
        "states_visited",
        "candidate_placements_considered",
    )


PROFILES: dict[str, NQueensProfile] = {'toy': NQueensProfile(name='toy', problem_size=4, description='Small board for quick correctness checks.', default_solver='all', solver_names=('dfs_backtracking', 'constraint', 'bitmask_backtracking'), baseline_solver='dfs_backtracking', comparison_metric_groups=('common',)), 'standard': NQueensProfile(name='standard', problem_size=8, description='Classic N=8 run across the default domain flow.', comparison_metric_groups=('common', 'search_shape', 'constraint', 'backtracking', 'bitmask'), default_solver='all', solver_names=('dfs_backtracking', 'constraint', 'bitmask_backtracking'), baseline_solver='dfs_backtracking')}


def get_profile_names() -> list[str]:
    """Return the registered N-Queens profile names."""
    return list(PROFILES.keys())


def get_profile(name: str) -> NQueensProfile:
    """Resolve one registered N-Queens profile by name."""
    try:
        return PROFILES[name]
    except KeyError as exc:
        raise ValueError(f"Unknown profile: {name}") from exc
