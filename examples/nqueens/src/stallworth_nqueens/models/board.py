"""Board model for N-Queens solutions and visualization."""

# models/board.py

from dataclasses import dataclass

from stallworth_nqueens.abstract.constraints import major_diagonal, minor_diagonal


@dataclass(frozen=True)
class NQueensBoard:
    """Represents one N-Queens board using a column index for each row."""

    size: int
    columns_by_row: tuple[int, ...]

    def __post_init__(self):
        if self.size < 1:
            raise ValueError("Board size must be at least 1.")

        if len(self.columns_by_row) != self.size:
            raise ValueError("Exactly one column must be provided for each row.")

        for col in self.columns_by_row:
            if not 0 <= col < self.size:
                raise ValueError("Column positions must be within board bounds.")

    @classmethod
    def from_columns(cls, columns_by_row):
        """Create a board from an ordered collection of column positions."""
        return cls(len(columns_by_row), tuple(columns_by_row))

    @property
    def queen_positions(self) -> tuple[tuple[int, int], ...]:
        """Return queen positions as `(row, col)` pairs."""
        return tuple((row, col) for row, col in enumerate(self.columns_by_row))

    def is_valid(self) -> bool:
        """Check whether the board is a valid N-Queens solution."""
        seen_cols = set()
        seen_diag1 = set()
        seen_diag2 = set()

        for row, col in self.queen_positions:
            if (
                col in seen_cols
                or major_diagonal(row, col) in seen_diag1
                or minor_diagonal(row, col) in seen_diag2
            ):
                return False

            seen_cols.add(col)
            seen_diag1.add(major_diagonal(row, col))
            seen_diag2.add(minor_diagonal(row, col))

        return True

    def to_ascii(self, queen="Q", empty=".", max_size=10) -> str:
        """Render the board as ASCII.

        Visualization is limited by default so large boards do not flood the terminal.
        """
        if self.size > max_size:
            raise ValueError(f"ASCII visualization is limited to boards of size {max_size} or smaller.")

        rows = []

        for row in range(self.size):
            current_row = [empty] * self.size
            current_row[self.columns_by_row[row]] = queen
            rows.append(" ".join(current_row))

        return "\n".join(rows)

    def __str__(self) -> str:
        return self.to_ascii()
