from pathlib import Path
from typing import Optional, Union, Literal, List, Any
from enum import Enum, auto
import re
from clang import cindex
from devana.syntax_abstraction.organizers.codecontainer import CodeContainer
from devana.syntax_abstraction.comment import CommentMarker, Comment, CommentsFactory
from devana.syntax_abstraction.organizers.lexicon import Lexicon
from devana.syntax_abstraction.codepiece import CodePiece
from devana.utility.lazy import LazyNotInit, lazy_invoke
from devana.configuration import Configuration, ParsingErrorPolicy
from devana.utility.errors import ParserError
from devana.syntax_abstraction.syntax import ISyntaxElement


class IncludeInfo(ISyntaxElement):
    """Include present in file."""

    def __init__(self, cursor: Optional[cindex.FileInclusion] = None, parent: Optional[Any] = None):
        self._parent = parent
        self._cursor = cursor
        if cursor is None:
            self._value = ""
            self._text = None
            self._is_standard = False
            self._source_file = None
        else:
            self._source_file = LazyNotInit
            self._value = None
            self._is_standard = False
            self._text = ""
            pattern = r'#\s*include\s*[<"](.+)[">]'
            file = cursor.source.name
            with open(file, "r") as f:  # pylint: disable=unspecified-encoding
                for _ in range(cursor.location.line - 1):
                    next(f)
                self._text = f.readline().rstrip()
            value: Optional = re.search(pattern, self._text)
            if not value:
                raise ParserError("Wrong include directive (include_next?).")
            self._value = value.group(1)
            self._path = cursor.include.name
            if "<" in self._text:
                self._is_standard = True

    @property
    def value(self) -> str:
        """Value of include."""
        return self._value

    @value.setter
    def value(self, v):
        self._value = v

    @property
    def is_standard(self) -> bool:
        """Information that include search in compiler headers in first order as include <stdlib> - is_standard true."""
        return self._is_standard

    @is_standard.setter
    def is_standard(self, value):
        self._is_standard = value

    @property
    def path(self) -> str:
        """Unrolled path of element of include."""
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    @property
    def text(self) -> Optional[str]:
        """Source text of this element."""
        return self._text

    @property
    def parent(self) -> Optional:
        """Source file parent."""
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value

    @property
    @lazy_invoke
    def source_file(self) -> Optional:
        self._source_file = None
        if self.parent is None:
            self._source_file = SourceFile(self.path)
        else:
            raise NotImplementedError()
        return self._source_file

    @source_file.setter
    def source_file(self, value):
        self._source_file = value

    @staticmethod
    def get_includes(translation_unit: cindex.TranslationUnit):
        includes = []
        pattern = r'#\s*include\s*[<"](.+)[">]'
        code_piece = CodePiece(translation_unit.cursor)
        match = re.findall(pattern, code_piece.text)
        file_root_path: Path = Path(code_piece.file).parent
        text_includes = [(file_root_path / Path(inc)).absolute() for inc in match]

        for inc in translation_unit.get_includes():
            path_cursor = Path(inc.include.name).absolute()
            # pylint: disable=cell-var-from-loop
            result = list(filter(lambda p: p == path_cursor or p.name == path_cursor.name, text_includes))
            if len(result) != 0:
                includes.append(IncludeInfo(inc))
                if len(text_includes) > 0 and len(result) > 0:
                    text_includes.remove(result[0])

        return includes


class SourceFileType(Enum):
    """Description of whether we are dealing with a header or source type."""
    HEADER = auto()
    IMPLEMENTATION = auto()

    @property
    def is_header(self) -> bool:
        return self.value == self.HEADER

    @property
    def is_implementation(self) -> bool:
        return self.value == self.IMPLEMENTATION


class SourceFile(CodeContainer):
    """Information about specific source code file."""

    def __init__(self, source: Optional[Union[cindex.Cursor, str]] = None, parent: Optional[Any] = None,
                 configuration: Optional[Configuration] = None):
        cursor = None
        if configuration is None:
            self._configuration = Configuration.get_configuration(self)
        else:
            self._configuration = configuration
        self._configuration.validate()
        if source is not None:
            if not isinstance(source, str):
                cursor = source
            else:
                import clang  # pylint: disable=import-outside-toplevel
                index = clang.cindex.Index.create()
                cursor = index.parse(source, args=self.configuration.parsing.parsing_options()).cursor
        super().__init__(cursor, parent)
        self._source = source
        self._cursor = cursor
        if source is None:
            self._path = Path()
            self._text_source = ""
            self._type = SourceFileType.HEADER
            self._includes = []
            self._header_guard = None
            self._preamble = None
            self._comments_factory = None
        else:
            if cursor is None:
                self._cursor = cursor
                self._path = None
                self._text_source = LazyNotInit
                self._includes = LazyNotInit
                self._type = LazyNotInit
                self._preamble = LazyNotInit
                self._comments_factory = None
            else:
                if not self.is_cursor_valid(cursor):
                    raise ParserError("It is not valid cursor kind.")
                self._path = Path(cursor.spelling)
                self._text_source = LazyNotInit
                self._includes = LazyNotInit
                self._type = LazyNotInit
                self._header_guard = LazyNotInit
                self._comments_factory = CommentsFactory(self)
        self._lexicon = Lexicon.create(self)

    @staticmethod
    def is_cursor_valid(cursor: cindex.Cursor) -> bool:
        return cursor.kind == cindex.CursorKind.TRANSLATION_UNIT

    @classmethod
    def create_default(cls, parent: Optional[ISyntaxElement] = None) -> Any:
        return cls(None, parent)

    @classmethod
    def from_cursor(cls, cursor: cindex.Cursor, parent: Optional = None,
                    configuration: Optional[Configuration] = None) -> Optional:
        if not cls.is_cursor_valid(cursor):
            return None
        return cls(cursor, parent, configuration)

    @classmethod
    def from_path(cls, source: str, parent: Optional[Any] = None, configuration: Optional[Configuration] = None):
        return cls(source, parent, configuration)

    @property
    @lazy_invoke
    def type(self) -> SourceFileType:
        """Information abut file type."""
        if self.extension in ["c", "cxx", "cpp", "cc"]:
            self._type = SourceFileType.IMPLEMENTATION
        else:
            self._type = SourceFileType.HEADER
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def name(self) -> str:
        """Name of source file without extension."""
        return self.path.name

    @property
    def extension(self) -> Union[Literal["h", "hpp", "hxx", "c", "cpp", "cxx", "cc"], str]:
        """File extension. In most common way, it will be standard, well know C++ extension."""
        return self.path.suffix.lstrip(".")

    @property
    def path(self) -> Optional[Path]:
        """Relative to module source file path."""
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    @property
    def module(self) -> Any:
        """Parent module of source file."""
        return super().parent

    @property
    def lexicon(self):
        return self._lexicon

    @lexicon.setter
    def lexicon(self, value):
        self._lexicon = value

    @property
    def namespace(self) -> Optional[str]:
        """Namespace name if any."""
        return None

    @property
    @lazy_invoke
    def includes(self) -> List[IncludeInfo]:
        self._includes = []
        self._includes = IncludeInfo.get_includes(self._cursor.translation_unit)
        return self._includes

    @includes.setter
    def includes(self, value):
        self._includes = value

    @property
    @lazy_invoke
    def preamble(self) -> Optional[Comment]:
        """First comment in file - Must start with the first line. Standard comment grouping policies apply. """
        self._preamble = None
        if self._comments_factory.comments:
            preamble = self._comments_factory.comments[0]
            if preamble.marker == CommentMarker.MULTI_LINE and preamble.begin.row == 1 and preamble.begin.col == 1:
                self._preamble = preamble
        return self._preamble

    @preamble.setter
    def preamble(self, value: Optional[Comment]):
        self._preamble = value

    @property
    @lazy_invoke
    def header_guard(self) -> Optional[str]:
        self._header_guard = None
        def_name = None
        if not self.text_source:
            return self._header_guard

        line_fist_content = -1
        line_last_content = -1
        if len(self.content) > 0:
            line_fist_content = self.content[0].text_source.begin.row
            line_last_content = self.content[-1].text_source.end.row

        lines = self.text_source.text.split("\n")

        for i, line in enumerate(lines[:line_fist_content]):
            match = re.match(r"^#ifndef\s(\S+)", line)
            if not match:
                continue
            if len(match.group()) < 1:
                continue
            def_name = match.group(1)
            if line_fist_content > i:
                match = re.match(r"^#define\s(\S+)", lines[i + 1])
                if not match:
                    return self._header_guard
                if len(match.group()) < 1:
                    return self._header_guard
                if match.group(1) != def_name:
                    return self._header_guard
                break
            else:
                return self._header_guard

        for line in reversed(lines[line_last_content:]):
            match = re.match(r"^#endif", line)
            if match:
                self._header_guard = def_name
                break

        return self._header_guard

    @header_guard.setter
    def header_guard(self, value):
        self._header_guard = value

    @property
    def configuration(self) -> Configuration:
        return self._configuration

    @configuration.setter
    def configuration(self, value: Configuration):
        self._configuration = value

    def bind_comment(self, element) -> Optional[Comment]:
        """Function take code element present in this source file and return associated comment
        depending on the configuration. A common use case is when specific instances of code elements use this."""
        if not hasattr(element, "text_source"):
            return None
        if self._comments_factory is None:
            return None
        return self._comments_factory.get_upper_comment(element.text_source)

    @property
    def diagnostics(self) -> List:
        """Information about backend parsing warnings and errors."""
        if self._cursor is None:
            return []
        return list(self._cursor.translation_unit.diagnostics)

    @property
    def _content_types(self) -> List:
        # pylint: disable=import-outside-toplevel
        from devana.syntax_abstraction.classinfo import ClassInfo, MethodInfo
        from devana.syntax_abstraction.unioninfo import UnionInfo
        from devana.syntax_abstraction.functioninfo import FunctionInfo
        from devana.syntax_abstraction.typedefinfo import TypedefInfo
        from devana.syntax_abstraction.namespaceinfo import NamespaceInfo
        from devana.syntax_abstraction.usingnamespace import UsingNamespace
        from devana.syntax_abstraction.enuminfo import EnumInfo
        from devana.syntax_abstraction.variable import GlobalVariable
        from devana.syntax_abstraction.externc import ExternC
        from devana.syntax_abstraction.using import Using
        types = [ClassInfo, UnionInfo, FunctionInfo, EnumInfo, TypedefInfo, NamespaceInfo, UsingNamespace,
                 MethodInfo, GlobalVariable, ExternC, Using]
        return types

    def _create_content(self) -> List[Any]:
        """Overwrite this method to filter witch content should be parsed inside class."""
        types = self._content_types
        content = []
        config = Configuration.get_configuration(self)
        is_abort_on_error = config.parsing.error_strategy == ParsingErrorPolicy.ABORT
        is_ignore_on_error = config.parsing.error_strategy == ParsingErrorPolicy.IGNORE
        for children in self._cursor.get_children():
            if Path(children.location.file.name) != self.path:
                continue
            element: Optional = None
            for t in types:
                try:
                    element = t.from_cursor(children, self)
                    if element is None:
                        continue
                    break
                except ParserError:
                    if is_ignore_on_error:
                        continue
                    if is_abort_on_error:
                        raise
                    config.logger.warning("Parser error during create content of %s in type %s "
                                          "for cursor %s.", self, t, children.spelling)
                    continue
            if element is None:
                if children.kind in (cindex.CursorKind.CLASS_TEMPLATE,
                                     cindex.CursorKind.CLASS_TEMPLATE.CLASS_TEMPLATE_PARTIAL_SPECIALIZATION):
                    continue  # ignore templates error for special dragon case
                if is_ignore_on_error:
                    continue
                if is_abort_on_error:
                    raise ParserError(f"Cannot match any type for content of {self} n cursor {children.spelling}.")
                config.logger.warning("Cannot match any type for content of %s n cursor %s.",
                                      self, children.spelling)
                continue
            content.append(element)
        return content

    def __repr__(self):
        return f"{type(self).__name__}:{self.type}:{self.name} ({super().__repr__()})"
