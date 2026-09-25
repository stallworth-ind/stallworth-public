"""Demonstrate shared bases, inheritance depth, and terminating call cycles."""


class DemoStage:
    """Shared base with three direct subclasses for the Classes report."""


class BoardStage(DemoStage):
    """First direct subclass."""


class SearchStage(DemoStage):
    """Second direct subclass."""


class ResultStage(DemoStage):
    """Third direct subclass."""


class InstrumentedSearchStage(SearchStage):
    """An additional inheritance level."""


class DetailedSearchStage(InstrumentedSearchStage):
    """Depth three demonstrates the inheritance-chain finding."""


def remaining_rows(size):
    """Direct recursion with a decreasing nonnegative bound."""
    if size <= 0:
        return 0
    return 1 + remaining_rows(size - 1)


def even_row(size):
    """Mutual recursion with odd_row, stopping at zero."""
    if size <= 0:
        return True
    return odd_row(size - 1)


def odd_row(size):
    """Mutual recursion with even_row, stopping at zero."""
    if size <= 0:
        return False
    return even_row(size - 1)
