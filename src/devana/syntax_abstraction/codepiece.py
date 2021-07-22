from clang import cindex
from typing import Optional


class CodePiece:
    """Class represented code as raw characters sequence seen as sees it programmer with comments
    and not replaced preprocessor stuff. Only white character correction is allowed.

    Code can be bind to existing file if it source is file or CodePiece is used as representative of
    code generation result."""

    class CodeLocation:
        """Class hold information about code coordinates in file."""

        def __init__(self, row, col):
            self._row = row
            self._col = col

        @property
        def row(self) -> int:
            return self._row

        @property
        def col(self) -> int:
            return self._col

    def __init__(self, cursor: cindex.Cursor):
        self._cursor = cursor

    @property
    def file(self) -> Optional[str]:
        """Absolute string path to code file. None value mean unnamed, virtual file used in code generation process."""
        if self._cursor.kind == cindex.CursorKind.TRANSLATION_UNIT:
            return self._cursor.spelling
        return self._cursor.location.file.name

    @property
    def begin(self) -> CodeLocation:
        """Start of code."""
        return CodePiece.CodeLocation(self._cursor.extent.start.line, self._cursor.extent.start.column)

    @property
    def end(self) -> CodeLocation:
        """End of code."""
        return CodePiece.CodeLocation(self._cursor.extent.end.line, self._cursor.extent.end.column)

    @property
    def text(self) -> str:
        """Raw text of code, from begin to end."""
        try:
            # standard file
            with open(self.file, "rb") as f:
                begin = self._cursor.extent.start.offset
                end = self._cursor.extent.end.offset
                f.seek(begin)
                return self._remove_base_indent(f.read(end - begin).decode())
        except IOError:
            # clang in memory file (special dragon case) - do not look
            return self._cursor.spelling

    @staticmethod
    def _remove_base_indent(text: Optional[str]) -> Optional[str]:
        split_text = text.split("\n")
        last_line = split_text[-1]
        indent_len = len(last_line) - len(last_line.lstrip())
        prefix = ""
        for i in range(indent_len):
            prefix += " "
        result = ""
        for line in split_text:
            result += line[line.startswith(prefix) and len(prefix):]
            result += "\n"
        return result[:-1]
