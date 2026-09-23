Demonstration findings: B404 and B603 are deliberately present in sast_demo.py, an uncalled example module. No solver, CLI, registry, or test imports or calls it. These findings remain active so you can explore source context and review controls. Only this exact example is permitted by the publication gate; unexpected findings still block publication.

# Bandit Report

Project       : stallworth-nqueens
Scan Label    : src
Scan Path     : `src`
Observations  : 2
Active Issues : 2
Active        : 2
Accepted      : 0
Relocated     : 0
Changed       : 0
Stale         : 0
Invalid       : 0

Code scanned:

  Total lines of code        : 1076
  Total lines skipped (#nosec): 0

## Active Findings

### LOW / HIGH - B404

- Location: `src/stallworth_nqueens/sast_demo.py:8`
- State: `active`
- Symbol: `<module>`
- Fingerprint: `sha256:7c6101196620437794553d5da379fc4799b71f579e8e25d502e351b61bed03cf`
- Issue: Consider possible security implications associated with the subprocess module.
- Source context:
          5 | It illustrates findings review; it is not a solver execution mechanism.
          6 | """
          7 | 
    >     8 | import subprocess
          9 | 
         10 | 
         11 | def subprocess_example(arguments: list[str]) -> subprocess.CompletedProcess:
- More Info: https://bandit.readthedocs.io/en/1.9.4/blacklists/blacklist_imports.html#b404-import-subprocess

### LOW / HIGH - B603

- Location: `src/stallworth_nqueens/sast_demo.py:13`
- State: `active`
- Symbol: `subprocess_example`
- Fingerprint: `sha256:de2ecb1a7b318058f251a1b836139dd67e07d1a4d95fe29cd54d3f0e691fd08b`
- Issue: subprocess call - check for execution of untrusted input.
- Source context:
         10 | 
         11 | def subprocess_example(arguments: list[str]) -> subprocess.CompletedProcess:
         12 |     """Illustrate why a subprocess argument list still needs input review."""
    >    13 |     return subprocess.run(arguments, check=True)
- More Info: https://bandit.readthedocs.io/en/1.9.4/plugins/b603_subprocess_without_shell_equals_true.html

## Relocated Findings

No relocated findings require updates.

## Reviewed Findings

No reviewed findings are present in this scan.
