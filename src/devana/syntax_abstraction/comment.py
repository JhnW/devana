from enum import Enum, auto
from typing import List, Optional
import re
from devana.syntax_abstraction.codepiece import CodePiece
from devana.syntax_abstraction.codelocation import CodeLocation
from devana.utility.lazy import LazyNotInit, lazy_invoke
from devana.configuration import Configuration


class CommentMarker(Enum):
    """One-line comment marker '//' or multiple lines."""
    ONE_LINE = auto()
    MULTI_LINE = auto()

    @property
    def begin_marker(self) -> str:
        """String representation of start comment marker."""
        if self.value == self.ONE_LINE:
            return "//"
        else:
            return "/*"

    @property
    def end_marker(self) -> Optional[str]:
        """String representation of start comment marker. It may be None for one line comment."""
        if self.value == self.ONE_LINE:
            return None
        else:
            return "*/"


class Comment:
    """The representing class exists in the comments code. Not all existing code comments need to be instantiated.
    In particular, comments inside implementation bodies are not instantiated
    and other, depending on parsing settings."""

    def __init__(self, marker: CommentMarker = CommentMarker.ONE_LINE, begin: Optional[CodeLocation] = None,
                 end: Optional[CodeLocation] = None, parent: Optional = None):
        self._marker = marker
        if (begin is None and end is not None) or (end is None and begin is not None):
            raise ValueError("Both begin and end must have value or be None")
        self._begin = begin
        self._end = end
        if begin is None and end is None:
            self._text = []
        else:
            self._text = LazyNotInit
        # pylint: disable=import-outside-toplevel
        from devana.syntax_abstraction.organizers.sourcefile import SourceFile
        self._parent: SourceFile = parent

    @classmethod
    def from_code_piece(cls, marker: CommentMarker, code_piece: CodePiece, parent: Optional = None):
        return Comment(marker, code_piece.begin, code_piece.end, parent)

    @property
    def marker(self) -> CommentMarker:
        """Defines whether a comment uses multi-line content markers or just a single-line comment style."""
        return self._marker

    @marker.setter
    def marker(self, value: CommentMarker):
        self._marker = value

    @property
    def begin(self) -> Optional[CodeLocation]:
        return self._begin

    @property
    def end(self) -> Optional[CodeLocation]:
        return self._end

    @property
    @lazy_invoke
    def text(self) -> List[str]:
        self._text = self._format_text(self._text_from_location())
        return self._text

    @text.setter
    def text(self, value: List[str]):
        """Text as a list of lines. This form is the preferred."""
        self._text = value

    @property
    def homogeneous_text(self) -> str:
        """Text as a single text string."""
        return "\n".join(self.text)

    @homogeneous_text.setter
    def homogeneous_text(self, value: str):
        self._text = value.split('\n')

    @property
    def parent(self) -> Optional:
        return self._parent

    @parent.setter
    def parent(self, value: Optional):
        self._parent = value

    def _text_from_location(self) -> List[str]:
        if self._parent.path is None:
            return []
        with open(self._parent.path, "r") as file:  # pylint: disable=unspecified-encoding
            lines = file.read().split('\n')
            lines = list(map(lambda e: e.rstrip('\r'), lines))
            if self._marker == CommentMarker.MULTI_LINE and self._begin.row == self._end.row:
                return [lines[self._begin.row - 1][self._begin.col + 1:self._end.col - 2]]
            lines = lines[self._begin.row - 1:self._end.row]
            result = []
            if self._marker == CommentMarker.ONE_LINE:
                for line in lines:
                    result.append(line[self._begin.col + 1:])
                return result
            elif self._marker == CommentMarker.MULTI_LINE:
                lines[0] = lines[0][self._begin.col + 1:]
                lines[-1] = lines[-1][:self._end.col - 2]
                for _index, line in enumerate(lines):
                    result.append(line)
            return result

    def _format_text(self, lines: List[str]) -> List[str]:
        result: List[str] = []
        config: Configuration = self._parent.configuration
        for index, line in enumerate(lines):
            if self.marker == CommentMarker.MULTI_LINE:
                if 0 < index < len(lines) - 1:
                    line = line[self.begin.col - 1:]
            if config.parsing.comments.remove_asterisks:
                if line.startswith("*"):
                    line = line[1:]
            result.append(line)
        if config.parsing.comments.remove_blank_lines:
            if result[0].lstrip() == "":
                result = result[1:]
            if result[-1].lstrip() == "":
                result = result[:-1]

        return result


class CommentsFactory:
    """Internal the class that collects all detected comments in the file.
    Its purpose is to help you find comments requested by specific code elements."""

    def __init__(self, source):
        self._source = source
        self._comments = LazyNotInit

    @property
    @lazy_invoke
    def comments(self) -> List[Comment]:
        self._comments = self._create_comments_list()
        return self._comments

    def get_upper_comment(self, element: CodePiece) -> Optional[Comment]:
        result = None
        line = element.begin.row
        col = element.begin.col
        config: Configuration = self._source.configuration
        for index, comment in enumerate(self.comments):
            if comment.end.row == line - 1 and comment.begin.col == col:
                if comment.marker == CommentMarker.ONE_LINE and config.parsing.comments.accumulate:
                    begin = comment.begin
                    end = comment.end
                    for i in reversed(range(0, index + 1)):
                        if not (self.comments[i].begin.row == line - 1 - (index - i) and self.comments[
                            i].begin.col == col
                                and self.comments[i].marker == CommentMarker.ONE_LINE):
                            break
                        begin = self.comments[i].begin
                    if begin.row == comment.begin.row:
                        result = comment
                    else:
                        result = Comment.from_code_piece(CommentMarker.ONE_LINE,
                                                         CodePiece.from_location(begin, end, self._source.path),
                                                         self._source)
                else:
                    result = comment
                break
        return result

    def preamble(self) -> Optional[Comment]:
        if not self.comments:
            return None
        preamble = self.comments[0]
        if preamble.begin.row == 1:
            return preamble
        return None

    def _create_comments_list(self) -> List[Comment]:
        if self._source.path is None:
            return []
        text = self._source.text_source.text
        lines = text.split('\n')
        lines = list(map(lambda e: e.rstrip('\r'), lines))  # windows \r\n compatibility
        results = []
        is_multi_line_mode = False
        multi_line_begin = None

        for index, line in enumerate(lines):
            if is_multi_line_mode:
                # match  comment */ (multi line begin)
                match = re.search(r"(.*)\*/", line)
                if match:
                    multi_line_end = CodeLocation(index + 1, match.regs[0][1])
                    results.append(Comment.from_code_piece(CommentMarker.MULTI_LINE,
                                                           CodePiece.from_location(multi_line_begin, multi_line_end,
                                                                                   self._source.path),
                                                           self._source))
                    is_multi_line_mode = False
                    multi_line_begin = None
                    continue
            else:

                # match /* comment */
                matches = list(re.finditer(r"/\*(.+?)\*/", line))
                if matches:
                    for match in matches:
                        begin = CodeLocation(index + 1, match.regs[0][0] + 1)
                        end = CodeLocation(index + 1, match.regs[0][1])
                        results.append(Comment.from_code_piece(CommentMarker.MULTI_LINE,
                                                               CodePiece.from_location(begin, end, self._source.path),
                                                               self._source))
                    continue

                # match /* comment (multi line begin)
                match = re.search(r"/\*(.*)", line)
                if match:
                    is_multi_line_mode = True
                    multi_line_begin = CodeLocation(index + 1, match.regs[0][0] + 1)
                    continue

                # match // comment
                match = re.search(r"//(.*)", line)
                if match:
                    begin = CodeLocation(index + 1, match.regs[0][0] + 1)
                    end = CodeLocation(index + 1, len(line))
                    results.append(Comment.from_code_piece(CommentMarker.ONE_LINE,
                                                           CodePiece.from_location(begin, end, self._source.path),
                                                           self._source))
                    continue

        return results
