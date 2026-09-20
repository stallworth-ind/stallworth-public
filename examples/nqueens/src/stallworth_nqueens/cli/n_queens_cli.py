import logging

from stallworth_nqueens.common.logging.logger import (
    format_unexpected_error,
    setup_logging,
)
from difflib import get_close_matches

from stallworth_nqueens.cli.args import build_args, format_usage
from stallworth_nqueens.execution.engine import execute
from stallworth_nqueens.profiles.registry import get_profile, get_profile_names
from stallworth_nqueens.reporting.display import display_usage, display_execution_result, display_run_header, display_unknown_solver, display_unexpected_error
from stallworth_nqueens.solvers.registry import get_solver_names


logger = logging.getLogger(__name__)

def run_n_queens_cli():
    solver_names = get_solver_names()
    profile_names = get_profile_names()
    choice = ""
    try:
        args = build_args(solver_names, profile_names)
        setup_logging(args.log_level)
        choice = args.solver.lower()
        profile = get_profile(args.profile) if args.profile else None
        solver_subset = profile.solver_names if profile and choice == "all" else None
        display_run_header(args.n, profile_name=args.profile)
        result = execute(args.n, choice, solver_names=solver_subset, profile_name=args.profile)
        display_execution_result(result)
        entries = result["results"] if result["mode"] == "all" else [result["result"]]
        return 0 if entries and all(entry["result"].success for entry in entries) else 1
    except ValueError as exc:
        message = str(exc)
        setup_logging("info")
        if message == "Both n and solver are required unless --profile is provided.":
            display_usage(format_usage(solver_names, profile_names))
        elif "unrecognized arguments" in message.lower() or "required" in message.lower():
            display_usage(format_usage(solver_names, profile_names))
            display_unexpected_error(message)
        elif message.startswith("Unknown solver:"):
            suggestions = get_close_matches(choice, solver_names, n=1)
            display_unknown_solver(choice, suggestions, solver_names)
        else:
            display_unexpected_error(message)
        return 1
    except OSError as exc:
        display_unexpected_error(str(exc))
        return 1
    except Exception as exc:
        display_unexpected_error(format_unexpected_error(exc))
        return 1
