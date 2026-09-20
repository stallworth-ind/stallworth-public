import argparse

from stallworth_nqueens.profiles.registry import get_profile


class NQueensArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ValueError(message)


def build_parser(solver_names, profile_names):
    parser = NQueensArgumentParser(
        prog='stallworth-nqueens',
        description='Run N-Queens solvers',
    )

    parser.add_argument(
        "n",
        type=int,
        nargs="?",
        help="Board size",
    )

    parser.add_argument(
        "solver",
        type=str,
        nargs="?",
        help=f"Solver to run ({', '.join(solver_names)}) or 'all'",
    )

    parser.add_argument(
        "--profile",
        choices=profile_names,
        help=f"Named run profile ({', '.join(profile_names)})",
    )

    parser.add_argument(
        "--log-level",
        default="info",
        choices=["debug", "info", "warning", "error", "critical"],
        help="Set logging verbosity (default: info)",
    )




    return parser


def build_args(solver_names, profile_names):
    parser = build_parser(solver_names, profile_names)
    args = parser.parse_args()

    if args.profile:
        profile = get_profile(args.profile)
        if args.n is None:
            args.n = profile.problem_size
        if args.solver is None:
            args.solver = profile.default_solver

    if args.n is None or args.solver is None:
        raise ValueError("Both n and solver are required unless --profile is provided.")




    return args


def format_usage(solver_names, profile_names):
    parser = build_parser(solver_names, profile_names)
    return parser.format_help()
