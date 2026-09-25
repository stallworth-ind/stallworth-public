"""Deliberate dynamic public API for the Modules report."""

from stallworth_nqueens.codeviz_demo.models import DemoStage, remaining_rows, even_row, odd_row


def export_names():
    """Compute the demo API to expose a static-analysis limitation."""
    return [item.__name__ for item in (DemoStage, remaining_rows, even_row, odd_row)]


__all__ = export_names()
