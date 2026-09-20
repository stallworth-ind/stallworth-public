from stallworth_nqueens.execution.runner import execute_all, execute_solver
from stallworth_nqueens.solvers.registry import SOLVERS


def execute(problem_size, choice, solver_names=None, profile_name=None):
    """Run either one N-Queens solver or every registered solver.

    Both single-solver requests and ``all`` mode return domain-focused
    result payloads that are ready for the reporting layer.
    """
    if problem_size < 1:
        raise ValueError("Board size must be at least 1.")

    if choice == "all":
        return {
            "mode": "all",
            "size": problem_size,
            "profile": profile_name,
            "requested_solver": choice,
            "results": execute_all(problem_size, solver_names=solver_names),
        }

    if choice not in SOLVERS:
        raise ValueError(f"Unknown solver: {choice}")

    return {
        "mode": "single",
        "size": problem_size,
        "profile": profile_name,
        "requested_solver": choice,
        "result": execute_solver(problem_size, choice),
    }

#__all__ = ["execute", "get_solver_names"]
