"""Uncalled example code for the N-Queens SAST and CodeViz reports.

The subprocess import and call deliberately produce Bandit B404 and B603.
No solver, CLI, registry, or test imports or calls this demonstration module.
It illustrates findings review; it is not a solver execution mechanism.
"""

import subprocess


def subprocess_example(arguments: list[str]) -> subprocess.CompletedProcess:
    """Illustrate why a subprocess argument list still needs input review."""
    return subprocess.run(arguments, check=True)
