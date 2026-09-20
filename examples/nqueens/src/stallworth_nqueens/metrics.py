from __future__ import annotations

from dataclasses import dataclass
from inspect import Parameter, signature
from typing import Callable


SEARCH_SHAPE_METRICS_SCHEMA_VERSION = "1.0"
CONSTRAINT_METRICS_SCHEMA_VERSION = "1.0"
BACKTRACKING_METRICS_SCHEMA_VERSION = "1.0"
BITMASK_METRICS_SCHEMA_VERSION = "1.0"

CAPABILITY_METRIC_SCHEMA_VERSIONS: dict[str, str] = {
    "search_shape": SEARCH_SHAPE_METRICS_SCHEMA_VERSION,
    "constraint": CONSTRAINT_METRICS_SCHEMA_VERSION,
    "backtracking": BACKTRACKING_METRICS_SCHEMA_VERSION,
    "bitmask": BITMASK_METRICS_SCHEMA_VERSION,
}


@dataclass(slots=True)
class NQueensSearchShapeCounters:
    """Raw events describing the executed search tree or forest."""

    root_entries: int = 0
    leaf_states: int = 0
    child_states_entered: int = 0
    maximum_depth_reached: int = 0


@dataclass(slots=True)
class NQueensConstraintCounters:
    """Candidate-level constraint evaluations."""

    constraint_checks: int = 0
    constraint_rejections: int = 0


@dataclass(slots=True)
class NQueensBacktrackingCounters:
    """Logical returns and dead ends in backtracking search."""

    backtracks: int = 0
    dead_ends: int = 0


@dataclass(slots=True)
class NQueensBitmaskCounters:
    """Algorithm-level bitmask search events, not processor instructions."""

    available_masks_computed: int = 0
    candidate_bits_extracted: int = 0
    zero_availability_masks: int = 0


@dataclass(slots=True)
class NQueensSearchMetrics:
    """Mutable common counters collected during one solver execution.

    A state is counted whenever a solver enters or removes one search state,
    including initial and terminal states. A candidate is counted whenever
    the solver explicitly evaluates or generates a queen placement extension.
    Repeated visits, such as iterative-deepening passes, are counted again.
    """

    states_visited: int = 0
    candidate_placements_considered: int = 0
    search_shape: NQueensSearchShapeCounters | None = None
    constraint: NQueensConstraintCounters | None = None
    backtracking: NQueensBacktrackingCounters | None = None
    bitmask: NQueensBitmaskCounters | None = None

    def visit_state(self, count: int = 1) -> None:
        self.states_visited += count

    def consider_placement(self, count: int = 1) -> None:
        self.candidate_placements_considered += count

    def enter_search_state(
        self,
        depth: int,
        *,
        root: bool = False,
    ) -> None:
        """Count one state occurrence and its depth in the executed search."""

        self.visit_state()
        counters = self._search_shape()
        if root:
            counters.root_entries += 1
        counters.maximum_depth_reached = max(
            counters.maximum_depth_reached,
            depth,
        )

    def enter_child_state(self, count: int = 1) -> None:
        self._search_shape().child_states_entered += count

    def record_leaf_state(self, count: int = 1) -> None:
        self._search_shape().leaf_states += count

    def check_constraint(
        self,
        *,
        accepted: bool,
        count: int = 1,
    ) -> None:
        counters = self._constraint()
        counters.constraint_checks += count
        if not accepted:
            counters.constraint_rejections += count

    def record_backtrack(self, count: int = 1) -> None:
        self._backtracking().backtracks += count

    def record_dead_end(self, count: int = 1) -> None:
        self._backtracking().dead_ends += count

    def compute_available_mask(self, available: int) -> None:
        counters = self._bitmask()
        counters.available_masks_computed += 1
        if available == 0:
            counters.zero_availability_masks += 1

    def extract_candidate_bit(self, count: int = 1) -> None:
        self._bitmask().candidate_bits_extracted += count

    def capability_metrics_payload(self) -> dict[str, dict[str, int | str]]:
        """Return only capability groups observed during this execution."""

        payload: dict[str, dict[str, int | str]] = {}
        if self.search_shape is not None:
            payload["search_shape"] = {
                "schema_version": SEARCH_SHAPE_METRICS_SCHEMA_VERSION,
                "root_entries": self.search_shape.root_entries,
                "leaf_states": self.search_shape.leaf_states,
                "child_states_entered": self.search_shape.child_states_entered,
                "maximum_depth_reached": (
                    self.search_shape.maximum_depth_reached
                ),
            }
        if self.constraint is not None:
            payload["constraint"] = {
                "schema_version": CONSTRAINT_METRICS_SCHEMA_VERSION,
                "constraint_checks": self.constraint.constraint_checks,
                "constraint_rejections": (
                    self.constraint.constraint_rejections
                ),
            }
        if self.backtracking is not None:
            payload["backtracking"] = {
                "schema_version": BACKTRACKING_METRICS_SCHEMA_VERSION,
                "backtracks": self.backtracking.backtracks,
                "dead_ends": self.backtracking.dead_ends,
            }
        if self.bitmask is not None:
            payload["bitmask"] = {
                "schema_version": BITMASK_METRICS_SCHEMA_VERSION,
                "available_masks_computed": (
                    self.bitmask.available_masks_computed
                ),
                "candidate_bits_extracted": (
                    self.bitmask.candidate_bits_extracted
                ),
                "zero_availability_masks": (
                    self.bitmask.zero_availability_masks
                ),
            }
        return payload

    def _search_shape(self) -> NQueensSearchShapeCounters:
        if self.search_shape is None:
            self.search_shape = NQueensSearchShapeCounters()
        return self.search_shape

    def _constraint(self) -> NQueensConstraintCounters:
        if self.constraint is None:
            self.constraint = NQueensConstraintCounters()
        return self.constraint

    def _backtracking(self) -> NQueensBacktrackingCounters:
        if self.backtracking is None:
            self.backtracking = NQueensBacktrackingCounters()
        return self.backtracking

    def _bitmask(self) -> NQueensBitmaskCounters:
        if self.bitmask is None:
            self.bitmask = NQueensBitmaskCounters()
        return self.bitmask


@dataclass(frozen=True, slots=True)
class NQueensSolverExecution:
    """Raw solver output plus its common search counters."""

    solution_count: int
    metrics: NQueensSearchMetrics


class NQueensSolverFailure(RuntimeError):
    """Preserve partial metrics when an instrumented solver raises."""

    def __init__(
        self,
        cause: Exception,
        metrics: NQueensSearchMetrics,
    ) -> None:
        super().__init__(str(cause))
        self.cause = cause
        self.metrics = metrics


def execute_with_metrics(
    solver: Callable[..., int],
    problem_size: int,
) -> NQueensSolverExecution:
    """Execute a solver with common counters while supporting legacy callables."""

    metrics = NQueensSearchMetrics()
    try:
        parameters = signature(solver).parameters.values()
        accepts_metrics = any(
            parameter.name == "metrics"
            or parameter.kind == Parameter.VAR_KEYWORD
            for parameter in parameters
        )
    except (TypeError, ValueError):
        accepts_metrics = False

    try:
        if accepts_metrics:
            solution_count = solver(problem_size, metrics=metrics)
        else:
            solution_count = solver(problem_size)
    except Exception as exc:
        raise NQueensSolverFailure(exc, metrics) from exc

    return NQueensSolverExecution(
        solution_count=solution_count,
        metrics=metrics,
    )
