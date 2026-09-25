"""Ten outbound dependencies demonstrate a coordinating module."""

import stallworth_nqueens.codeviz_demo.board as board
import stallworth_nqueens.codeviz_demo.columns as columns
import stallworth_nqueens.codeviz_demo.diagonals as diagonals
import stallworth_nqueens.codeviz_demo.candidates as candidates
import stallworth_nqueens.codeviz_demo.placement as placement
import stallworth_nqueens.codeviz_demo.backtracking as backtracking
import stallworth_nqueens.codeviz_demo.solutions as solutions
import stallworth_nqueens.codeviz_demo.metrics as metrics
import stallworth_nqueens.codeviz_demo.formatting as formatting
import stallworth_nqueens.codeviz_demo.summary as summary


def stage_names():
    """Read demo stage labels; no solver work is performed."""
    return (
        board.NAME,
        columns.NAME,
        diagonals.NAME,
        candidates.NAME,
        placement.NAME,
        backtracking.NAME,
        solutions.NAME,
        metrics.NAME,
        formatting.NAME,
        summary.NAME,
    )
