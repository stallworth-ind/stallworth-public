# Source provenance

This is generated example source. Domain changes belong in the upstream AlgoBox
project; packaging and extraction changes belong in the versioned recipe.

- Upstream AlgoBox commit: `5b54bdbc8a56d08c879d32421eb345805cc5a2f9`
- Recipe: `nqueens`, schema `1.0`, version `1.3`
- Recipe content revision: `sha256:23eaa088530a98dae4d68f8b97fcd32b135d43c890b5ddd1066d646917be866c`
- Extractor content revision: `sha256:54ce9bbc590f1a4a330a029589a91590ec47476dd24fea956208279df5ce2c68`
- Example version: `0.2.1`

Source paths below are relative to the upstream repository. Output paths are
relative to this example. The separate extraction manifest records hashes and
applied transformations for each file. It is outside the source tree so that
source identity has no dependency on its own hash or a run timestamp.

The uncalled `src/stallworth_nqueens/sast_demo.py` module is supplied by the
Pipelines extraction recipe for the SAST/CodeViz demonstration. It is not
copied from AlgoBox. Its template origin and hash are recorded in the extraction
manifest alongside the upstream-derived files.

The uncalled `src/stallworth_nqueens/codeviz_demo/` package also comes from
explicit recipe templates. It demonstrates Codeviz findings without changing
solver execution. Each template origin and content hash is recorded in the
extraction manifest.

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
