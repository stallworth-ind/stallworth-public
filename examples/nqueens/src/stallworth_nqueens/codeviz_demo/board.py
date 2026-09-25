"""Uncalled board stage: one of ten explicit import-graph participants."""

import stallworth_nqueens.codeviz_demo.hub as hub
import stallworth_nqueens.codeviz_demo.models as models

NAME = "board"


def describe(stage: models.DemoStage):
    """Use both dependencies without executing a solver or the stage."""
    return NAME, type(stage).__name__, hub.stage_names()
