# Source provenance

This is generated example source. Domain changes belong in the upstream AlgoBox
project; packaging and extraction changes belong in the versioned recipe.

- Upstream AlgoBox commit: `5b54bdbc8a56d08c879d32421eb345805cc5a2f9`
- Recipe: `nqueens`, schema `1.0`, version `1.0`
- Recipe content revision: `sha256:a3c1174783d0621c3d3c6ff8863db68c5faeff2d866ca2082805416c8b9f723a`
- Extractor content revision: `sha256:f3bc4321d19c492382b702a81d8b8d2334d229d5b3c28e68555c057b9c66f589`
- Example version: `0.1.0`

Source paths below are relative to the upstream repository. Output paths are
relative to this example. The separate extraction manifest records hashes and
applied transformations for each file. It is outside the source tree so that
source identity has no dependency on its own hash or a run timestamp.

| Upstream source | Example output |
| --- | --- |
| `LICENSE` | `LICENSE` |
| `src/algobox/nqueens/__init__.py` | `src/stallworth_nqueens/__init__.py` |
| `src/algobox/nqueens/abstract/__init__.py` | `src/stallworth_nqueens/abstract/__init__.py` |
| `src/algobox/nqueens/abstract/bitmask.py` | `src/stallworth_nqueens/abstract/bitmask.py` |
| `src/algobox/nqueens/abstract/constraints.py` | `src/stallworth_nqueens/abstract/constraints.py` |
| `src/algobox/nqueens/benchmarking/__init__.py` | `src/stallworth_nqueens/benchmarking/__init__.py` |
| `src/algobox/nqueens/benchmarking/adapter.py` | `src/stallworth_nqueens/benchmarking/adapter.py` |
| `src/algobox/nqueens/cli/__init__.py` | `src/stallworth_nqueens/cli/__init__.py` |
| `src/algobox/nqueens/cli/args.py` | `src/stallworth_nqueens/cli/args.py` |
| `src/algobox/nqueens/cli/n_queens_cli.py` | `src/stallworth_nqueens/cli/n_queens_cli.py` |
| `src/algobox/common/__init__.py` | `src/stallworth_nqueens/common/__init__.py` |
| `src/algobox/common/benchmarking/__init__.py` | `src/stallworth_nqueens/common/benchmarking/__init__.py` |
| `src/algobox/common/benchmarking/adapters.py` | `src/stallworth_nqueens/common/benchmarking/adapters.py` |
| `src/algobox/common/benchmarking/models.py` | `src/stallworth_nqueens/common/benchmarking/models.py` |
| `src/algobox/common/benchmarking/runner.py` | `src/stallworth_nqueens/common/benchmarking/runner.py` |
| `src/algobox/common/logging/__init__.py` | `src/stallworth_nqueens/common/logging/__init__.py` |
| `src/algobox/common/logging/logger.py` | `src/stallworth_nqueens/common/logging/logger.py` |
| `src/algobox/nqueens/execution/__init__.py` | `src/stallworth_nqueens/execution/__init__.py` |
| `src/algobox/nqueens/execution/engine.py` | `src/stallworth_nqueens/execution/engine.py` |
| `src/algobox/nqueens/execution/runner.py` | `src/stallworth_nqueens/execution/runner.py` |
| `src/algobox/nqueens/main.py` | `src/stallworth_nqueens/main.py` |
| `src/algobox/nqueens/metrics.py` | `src/stallworth_nqueens/metrics.py` |
| `src/algobox/nqueens/models/__init__.py` | `src/stallworth_nqueens/models/__init__.py` |
| `src/algobox/nqueens/models/board.py` | `src/stallworth_nqueens/models/board.py` |
| `src/algobox/nqueens/profiles/__init__.py` | `src/stallworth_nqueens/profiles/__init__.py` |
| `src/algobox/nqueens/profiles/registry.py` | `src/stallworth_nqueens/profiles/registry.py` |
| `src/algobox/nqueens/reporting/__init__.py` | `src/stallworth_nqueens/reporting/__init__.py` |
| `src/algobox/nqueens/reporting/display.py` | `src/stallworth_nqueens/reporting/display.py` |
| `src/algobox/nqueens/solvers/__init__.py` | `src/stallworth_nqueens/solvers/__init__.py` |
| `src/algobox/nqueens/solvers/bitmask/__init__.py` | `src/stallworth_nqueens/solvers/bitmask/__init__.py` |
| `src/algobox/nqueens/solvers/bitmask/backtracking.py` | `src/stallworth_nqueens/solvers/bitmask/backtracking.py` |
| `src/algobox/nqueens/solvers/constraint.py` | `src/stallworth_nqueens/solvers/constraint.py` |
| `src/algobox/nqueens/solvers/dfs/__init__.py` | `src/stallworth_nqueens/solvers/dfs/__init__.py` |
| `src/algobox/nqueens/solvers/dfs/backtracking.py` | `src/stallworth_nqueens/solvers/dfs/backtracking.py` |
| `src/algobox/nqueens/solvers/registry.py` | `src/stallworth_nqueens/solvers/registry.py` |
| `tests/__init__.py` | `tests/__init__.py` |
| `tests/integration/__init__.py` | `tests/integration/__init__.py` |
| `tests/integration/nqueens/__init__.py` | `tests/integration/nqueens/__init__.py` |
| `tests/integration/nqueens/test_cli.py` | `tests/integration/nqueens/test_cli.py` |
| `tests/integration/nqueens/test_solvers.py` | `tests/integration/nqueens/test_solvers.py` |
| `tests/unit/__init__.py` | `tests/unit/__init__.py` |
| `tests/unit/common/__init__.py` | `tests/unit/common/__init__.py` |
| `tests/unit/common/benchmarking/__init__.py` | `tests/unit/common/benchmarking/__init__.py` |
| `tests/unit/common/benchmarking/test_common_metrics.py` | `tests/unit/common/benchmarking/test_common_metrics.py` |
| `tests/unit/common/benchmarking/test_runner.py` | `tests/unit/common/benchmarking/test_runner.py` |
| `tests/unit/common/test_logging.py` | `tests/unit/common/test_logging.py` |
| `tests/unit/nqueens/__init__.py` | `tests/unit/nqueens/__init__.py` |
| `tests/unit/nqueens/test_args.py` | `tests/unit/nqueens/test_args.py` |
| `tests/unit/nqueens/test_benchmark_adapter.py` | `tests/unit/nqueens/test_benchmark_adapter.py` |
| `tests/unit/nqueens/test_board.py` | `tests/unit/nqueens/test_board.py` |
| `tests/unit/nqueens/test_execution.py` | `tests/unit/nqueens/test_execution.py` |
| `tests/unit/nqueens/test_profiles.py` | `tests/unit/nqueens/test_profiles.py` |
| `tests/unit/nqueens/test_reporting.py` | `tests/unit/nqueens/test_reporting.py` |
