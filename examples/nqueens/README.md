# Stallworth N-Queens

A standalone N-Queens example derived from AlgoBox for Stallworth Workbench.
It includes DFS backtracking, constraint forward checking, and bitmask
backtracking, with board models, profiles, execution metrics, and tests.

Python 3.12 or newer is required. The installed runtime uses the standard
library. Create a virtual environment with `python -m venv .venv`, then activate
it using `.venv\Scripts\Activate.ps1` on PowerShell or
`source .venv/bin/activate` on Linux/macOS. Install a downloaded release wheel
with `python -m pip install <wheel-file>`, or install the source from this directory:

```text
python -m pip install .
stallworth-nqueens --help
stallworth-nqueens 4 dfs_backtracking
stallworth-nqueens 8 all
stallworth-nqueens --profile toy
stallworth-nqueens --profile standard
python -m stallworth_nqueens.main --profile toy
```

`toy` uses size 4; `standard` uses size 8. Both select the three included solvers
in the order shown above. `all` runs only this example's registry. These sizes
have 2 and 92 solutions respectively. Results include counts, timings, supported
search counters, and a representative valid board when one exists. The sample
board is found separately from the measured solver execution.

Profiles supply defaults: explicit board size and solver arguments take
precedence. For example, `stallworth-nqueens 4 constraint --profile standard`
runs only `constraint` at size 4. A size must be a positive integer. Sizes 2
and 3 have zero solutions, which is a successful run without a sample board.
Larger sizes can take substantially longer; the two profiles provide bounded
starting workloads.

Successful execution and `--help` exit with status 0. Missing or invalid inputs
and failed solver execution exit with status 1. For example,
`stallworth-nqueens 0 all` reports that the board size must be at least 1.
`--log-level` accepts `debug`, `info`, `warning`, `error`, and `critical`;
`info` is the default. Terminal results use Python logging, normally on stderr.

HTML/JSON report generation belongs to the internal
Stallworth Workbench automation. Published reports can be opened with their
companion assets; generation tools are not runtime dependencies of this example.

The `src/stallworth_nqueens/codeviz_demo/` package contains uncalled examples
for Codeviz: shared base classes and deep inheritance, direct and mutual
recursion, and dynamic module exports. Ten explicit demo
stages give the hub ten inbound and ten outbound internal dependencies; the
orchestrator has ten outbound dependencies and the models module is shared
by all ten stages. These produce findings at `orchestration_hub_threshold = 10`.
The CLI, solvers, and registries do not import this package. The examples are
recipe-supplied teaching source, separate from the N-Queens implementation.

The `src/stallworth_nqueens/sast_demo.py` module is an uncalled demonstration
for the SAST and CodeViz reports. Its subprocess import and call intentionally
produce Bandit B404 and B603, with source context and interactive review controls.
No solver, CLI, registry, or test imports or calls it. The example publication
gate permits only these two findings from the exact demonstration source;
unexpected findings and scanner failures still block publication.

To run the source tests with publicly available dependencies:

```text
python -m pip install ".[test]"
python -m pytest
```

The test extra installs pytest and pytest-cov. The tests use this installed
package and their own configuration; an editable AlgoBox installation is not
required. Build dependencies (setuptools and wheel) are separate from runtime
and test dependencies. The package has no required data files; license and
source attribution accompany the package metadata.

The selected source is refreshed through the versioned extraction recipe.
See [PROVENANCE.md](PROVENANCE.md) for its origin and [LICENSE](LICENSE) for the
preserved upstream license. This snapshot is version 0.2.2.
