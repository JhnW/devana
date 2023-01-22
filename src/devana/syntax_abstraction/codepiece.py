from typing import Optional
from clang import cindex
from devana.syntax_abstraction.codelocation import CodeLocation
from devana.utility.lazy import LazyNotInit, lazy_invoke


class CodePiece:
    """Class represented code as raw characters sequence seen as sees it programmer with comments
    and not replaced preprocessor stuff. Only white character correction is allowed.

    Code can be bind to existing file if its source is file or CodePiece is used as representative of
    code generation result."""

    def __init__(self, cursor: Optional[cindex.Cursor] = None):
        self._cursor = cursor
        if self._cursor is not None:
            self._begin = LazyNotInit
            self._end = LazyNotInit
            self._file = LazyNotInit
        else:
            self._begin = CodeLocation(1, 1)
            self._end = CodeLocation(1, 2)
            self._file = ""
        self._text = None

    @classmethod
    def from_location(cls, begin: CodeLocation, end: CodeLocation, file: str):
        instance = cls(None)
        instance.begin = begin
        instance.end = end
        instance.file = file
        return instance

    @property
    @lazy_invoke
    def file(self) -> Optional[str]:
        """Absolute string path to code file. None value mean unnamed, virtual file used in code generation process."""
        if self._cursor.kind == cindex.CursorKind.TRANSLATION_UNIT:
            self._file = self._cursor.spelling
        else:
            self._file = self._cursor.location.file.name
        return self._file

    @file.setter
    def file(self, value: str):
        self._file = value

    @property
    @lazy_invoke
    def begin(self) -> CodeLocation:
        """Start of code."""
        self._begin = CodeLocation(self._cursor.extent.start.line, self._cursor.extent.start.column)
        return self._begin

    @begin.setter
    def begin(self, value: CodeLocation):
        self._begin = value

    @property
    @lazy_invoke
    def end(self) -> CodeLocation:
        """End of code."""
        self._end = CodeLocation(self._cursor.extent.end.line, self._cursor.extent.end.column)
        return self._end

    @end.setter
    def end(self, value: CodeLocation):
        self._end = value

    @property
    def text(self) -> str:
        """Raw text of code, from begin to end."""
        if self._text is None:
            try:
                # standard file
                with open(self.file, "rb") as f:
                    if self._cursor is None:
                        lines = f.read().split(b'\n')
                        row_start = self.begin.row - 1
                        row_end = self.end.row - 1
                        col_start = self.begin.col - 1
                        col_end = self.end.col
                        text = b""
                        if len(lines) < row_start or len(lines) < row_end:
                            raise ValueError("Code begin and end extend file size.")
                        for index, line in enumerate(lines):
                            if row_start == index and row_end == index:
                                text = line[col_start:col_end + 1]
                                if len(lines) != index + 1:
                                    text += b'\n'
                                return str(text)
                            elif row_start == index:
                                text += line[col_start:] + b'\n'
                            elif row_end == index:
                                text += line[:col_end]
                            elif row_start <= index <= row_end:
                                text += line + b'\n'
                            elif row_end < index:
                                break
                        return str(text)
                    else:
                        begin = self._cursor.extent.start.offset
                        end = self._cursor.extent.end.offset
                        f.seek(begin)
                        return self._remove_base_indent(f.read(end - begin).decode())
            except IOError:
                # clang in memory file (special dragon case) - do not look
                return self._cursor.spelling
        return self._text

    @text.setter
    def text(self, value: str):
        self._text = value

    @staticmethod
    def _remove_base_indent(text: Optional[str]) -> Optional[str]:
        split_text = text.split("\n")
        last_line = split_text[-1]
        indent_len = len(last_line) - len(last_line.lstrip())
        prefix = ""
        for _ in range(indent_len):
            prefix += " "
        result = ""
        for line in split_text:
            result += line[line.startswith(prefix) and len(prefix):]
            result += "\n"
        return result[:-1]
