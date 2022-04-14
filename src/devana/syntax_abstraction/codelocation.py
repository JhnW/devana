class CodeLocation:
    """Class hold information about code coordinates in file."""

    def __init__(self, row, col):
        if col <= 0 or row <= 0:
            raise ValueError("Col and row must be greater than zero.")
        self._row = row
        self._col = col

    @property
    def row(self) -> int:
        return self._row

    @property
    def col(self) -> int:
        return self._col
