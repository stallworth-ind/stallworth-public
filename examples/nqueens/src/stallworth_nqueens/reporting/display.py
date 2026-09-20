import logging

from stallworth_nqueens.models.board import NQueensBoard

logger = logging.getLogger(__name__)


def _metric_value(value):
    return f"{value:,}" if isinstance(value, int) else "unavailable"


def _speedup_value(value, precision):
    if not isinstance(value, (int, float)):
        return "n/a"
    threshold = 10**-precision
    if 0 < value < threshold:
        return f"<{threshold:.{precision}f}x"
    return f"{value:.{precision}f}x"




def display_usage(usage: str):
    """Log preformatted CLI usage text line by line."""
    for line in usage.splitlines():
        logger.info(line)


def display_run_header(problem_size, profile_name=None):
    logger.info("\n" + "=" * 50)
    logger.info('Stallworth N-Queens')
    logger.info("=" * 50)
    logger.info("Board size: %s", problem_size)
    if profile_name:
        logger.info("Profile: %s", profile_name)


def display_unknown_solver(choice, suggestions, solver_names):
    logger.error("Unknown solver: %s", choice)

    if suggestions:
        logger.info("Did you mean: %s", suggestions[0])

    logger.info("Available solvers: %s", ", ".join(solver_names))


def display_unexpected_error(message):
    logger.error(message)


def display_single_result(result):
    solver = result["solver"]
    data = result["result"]
    size = data.payload["problem_size"]
    solutions = data.payload["solutions"]
    sample_solution = data.payload.get("sample_solution")

    logger.info("Solver: %s", solver)
    logger.info("Problem size: %s", size)
    logger.info("Solve time: %.6f sec", data.time)
    logger.info(
        "States visited: %s",
        _metric_value(data.payload.get("states_visited")),
    )
    logger.info(
        "Candidate placements considered: %s",
        _metric_value(
            data.payload.get("candidate_placements_considered")
        ),
    )

    if not data.success:
        failure_type = data.payload.get("failure_type", "Error")
        failure_message = data.payload.get(
            "failure_message",
            "Solver execution failed.",
        )
        logger.error("Solver failed: %s: %s", failure_type, failure_message)
        return

    logger.info("Solutions found: %s", solutions)

    if sample_solution is None:
        logger.info("Sample solution: none")
        return

    board = NQueensBoard.from_columns(sample_solution)

    logger.info("\nSample solution:")
    try:
        for row in board.to_ascii().splitlines():
            logger.info("  %s", row)
    except ValueError:
        logger.info("  Columns: %s", sample_solution)

    logger.info("\nValid solution: %s", board.is_valid())


def display_benchmark_results(problem_size, results):
    logger.info("\nBenchmark results for input=%s", problem_size)
    logger.info("-" * 90)
    logger.info(
        f"{'Solver':<22} | "
        f"{'Solutions':<9} | "
        f"{'Time (sec)':<10} | "
        f"{'Speed (best)':<12} | "
        f"{'Speed (vs baseline)'}"
    )
    logger.info("-" * 90)

    for result in results:
        logger.info(
            f"{result.solver:<22} | "
            f"{result.payload['solutions']:<9} | "
            f"{result.time:.6f}   | "
            f"{_speedup_value(result.payload.get('speedup_best'), 3):<12} | "
            f"{_speedup_value(result.payload.get('speedup_baseline'), 2)}"
        )


def display_all_results(results):
    logger.info("\nAll solvers:")

    for index, result in enumerate(results):
        if index:
            logger.info("\n" + "-" * 50)

        display_single_result(result)


def display_execution_result(execution_result):
    if execution_result["mode"] == "all":
        display_all_results(
            execution_result["results"],
        )
        return

    display_single_result(execution_result["result"])
