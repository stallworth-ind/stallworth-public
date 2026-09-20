from stallworth_nqueens.common.benchmarking import BenchmarkResult
from stallworth_nqueens.reporting import display


def test_display_usage_logs_usage_lines(monkeypatch):
    messages = []

    monkeypatch.setattr(display.logger, "info", lambda message, *args: messages.append(message % args if args else message))

    display.display_usage("usage: nqueens\nsecond line\n")

    assert messages == ["usage: nqueens", "second line"]






def test_display_run_header_prints_problem_size(monkeypatch):
    messages = []

    monkeypatch.setattr(display.logger, "info", lambda message, *args: messages.append(message % args if args else message))

    display.display_run_header(8, profile_name="standard")

    assert 'Stallworth N-Queens' in messages
    assert "Board size: 8" in messages
    assert "Profile: standard" in messages
    assert any("=" in message for message in messages)


def test_display_unknown_solver_prints_suggestion_and_solver_list(monkeypatch):
    info_messages = []
    error_messages = []

    monkeypatch.setattr(display.logger, "info", lambda message, *args: info_messages.append(message % args if args else message))
    monkeypatch.setattr(display.logger, "error", lambda message, *args: error_messages.append(message % args if args else message))

    display.display_unknown_solver('constrain', ['constraint'], ['constraint', "dfs_backtracking"])

    assert error_messages == ['Unknown solver: constrain']
    assert 'Did you mean: constraint' in info_messages
    assert 'Available solvers: constraint, dfs_backtracking' in info_messages


def test_display_unexpected_error_prints_message(monkeypatch):
    messages = []

    monkeypatch.setattr(display.logger, "error", lambda message, *args: messages.append(message % args if args else message))

    display.display_unexpected_error("Boom")

    assert messages == ["Boom"]


def test_display_single_result_prints_solver_summary(monkeypatch):
    messages = []

    monkeypatch.setattr(display.logger, "info", lambda message, *args: messages.append(message % args if args else message))

    display.display_single_result(
        {
            "solver": "demo",
            "result": BenchmarkResult(
                "nqueens",
                "demo",
                0.125,
                True,
                {
                    "problem_size": 4,
                    "solutions": 2,
                    "sample_solution": (1, 3, 0, 2),
                },
            ),
        }
    )

    assert "Solver: demo" in messages
    assert "Problem size: 4" in messages
    assert "Solutions found: 2" in messages
    assert "States visited: unavailable" in messages
    assert "Candidate placements considered: unavailable" in messages
    assert "\nSample solution:" in messages
    assert any("Q" in message for message in messages)
    assert "\nValid solution: True" in messages
    assert "Solve time: 0.125000 sec" in messages


def test_display_single_result_handles_missing_sample_solution(monkeypatch):
    messages = []

    monkeypatch.setattr(display.logger, "info", lambda message, *args: messages.append(message % args if args else message))

    display.display_single_result(
        {
            "solver": "demo",
            "result": BenchmarkResult(
                "nqueens",
                "demo",
                0.125,
                True,
                {
                    "problem_size": 3,
                    "solutions": 0,
                    "sample_solution": None,
                },
            ),
        }
    )

    assert "Sample solution: none" in messages


def test_display_single_result_reports_captured_failure(monkeypatch):
    info_messages = []
    error_messages = []
    monkeypatch.setattr(
        display.logger,
        "info",
        lambda message, *args: info_messages.append(
            message % args if args else message
        ),
    )
    monkeypatch.setattr(
        display.logger,
        "error",
        lambda message, *args: error_messages.append(
            message % args if args else message
        ),
    )

    display.display_single_result(
        {
            "solver": "broken",
            "result": BenchmarkResult(
                "nqueens",
                "broken",
                0.125,
                False,
                {
                    "problem_size": 4,
                    "solutions": None,
                    "states_visited": 5,
                    "candidate_placements_considered": 12,
                    "failure_type": "RuntimeError",
                    "failure_message": "branch failed",
                },
            ),
        }
    )

    assert "States visited: 5" in info_messages
    assert "Candidate placements considered: 12" in info_messages
    assert error_messages == [
        "Solver failed: RuntimeError: branch failed"
    ]


def test_display_benchmark_results_prints_table(monkeypatch):
    messages = []

    monkeypatch.setattr(display.logger, "info", lambda message, *args: messages.append(message % args if args else message))

    display.display_benchmark_results(
        4,
        [
            BenchmarkResult(
                "nqueens",
                "fast",
                1.0,
                True,
                {"solutions": 2, "speedup_best": 1.0, "speedup_baseline": 2.0},
            ),
            BenchmarkResult(
                "nqueens",
                "slow",
                4.0,
                True,
                {"solutions": 2, "speedup_best": 0.25, "speedup_baseline": 0.5},
            ),
        ],
    )

    assert "\nBenchmark results for input=4" in messages
    assert any("Solver" in message for message in messages)
    assert any("fast" in message for message in messages)
    assert any("0.250x" in message for message in messages)
    assert any("2.00x" in message for message in messages)


def test_speedup_value_marks_positive_values_below_display_precision():
    assert display._speedup_value(0.0004, 3) == "<0.001x"
    assert display._speedup_value(0.004, 2) == "<0.01x"
    assert display._speedup_value(0.0, 2) == "0.00x"


def test_display_all_results_iterates_single_results(monkeypatch):
    calls = []

    monkeypatch.setattr(display.logger, "info", lambda message, *args: calls.append(("log", message % args if args else message)))
    monkeypatch.setattr(display, "display_single_result", lambda result: calls.append(("single", result)))

    results = [
        {"solver": "demo", "result": BenchmarkResult("nqueens", "demo", 0.1, True, {"problem_size": 4, "solutions": 2})},
        {"solver": "other", "result": BenchmarkResult("nqueens", "other", 0.2, True, {"problem_size": 4, "solutions": 2})},
    ]

    display.display_all_results(results)

    assert calls[0] == ("log", "\nAll solvers:")
    assert ("single", results[0]) in calls
    assert ("single", results[1]) in calls
    assert ("log", "\n" + "-" * 50) in calls


def test_display_execution_result_routes_single_and_all(monkeypatch):
    calls = []

    monkeypatch.setattr(display, "display_single_result", lambda result: calls.append(("single", result)))
    monkeypatch.setattr(display, "display_all_results", lambda results: calls.append(("all", results)))

    single_result = {
        "solver": "demo",
        "result": BenchmarkResult(
            "nqueens",
            "demo",
            0.125,
            True,
            {
                "problem_size": 4,
                "solutions": 2,
                "sample_solution": (1, 3, 0, 2),
            },
        ),
    }

    all_results = [{"solver": "demo", "result": BenchmarkResult("nqueens", "demo", 1.0, True, {"solutions": 2})}]

    display.display_execution_result({"mode": "single", "result": single_result})
    display.display_execution_result({"mode": "all", "results": all_results})

    assert calls == [
        ("single", single_result),
        ("all", all_results),
    ]
