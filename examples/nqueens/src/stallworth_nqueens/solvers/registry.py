from stallworth_nqueens.solvers.dfs import backtracking as dfs_backtracking
from stallworth_nqueens.solvers import constraint
from stallworth_nqueens.solvers.bitmask import backtracking as bitmask_backtracking


DEFAULT_BASELINE = "dfs_backtracking"


SOLVERS = {
    'dfs_backtracking': dfs_backtracking.solve_n_queens,
    'constraint': constraint.solve_n_queens,
    'bitmask_backtracking': bitmask_backtracking.solve_n_queens,
}

def get_solver_names():
    return list(SOLVERS.keys())