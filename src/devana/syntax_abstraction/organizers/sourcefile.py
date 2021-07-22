from devana.syntax_abstraction.organizers.codecontainer import CodeContainer
from clang import cindex
from typing import Optional, Union, Literal, List, NoReturn
from enum import Enum, auto
from devana.utility.errors import ParserError
from pathlib import Path
from devana.utility.lazy import LazyNotInit, lazy_invoke
from devana.syntax_abstraction.organizers.lexicon import Lexicon
import re


class IncludeInfo:
    """Include present in file."""

    def __init__(self, cursor: Optional[cindex.FileInclusion], parent: Optional[any] = None):
        self._parent = parent
        self._cursor = cursor
        if cursor is None:
            pass
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
            with open(file, "r") as f:
                for i in range(cursor.location.line - 1):
                    next(f)
                self._text = f.readline().rstrip()
            self._value = re.search(pattern, self._text).group(1)
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

    def format_value(self) -> NoReturn:
        """Formats automatically value based on base source parent location."""
        raise NotImplementedError()

    @property
    def is_standard(self) -> bool:
        """Information that include search in compiler headers in first order as include <stdlib> - is_standard true."""
        return self._is_standard

    @is_standard.setter
    def is_standard(self, value):
        self._value = value

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
        for inc in translation_unit.get_includes():
            if inc.depth == 1:
                includes.append(IncludeInfo(inc))
        return includes


class SourceFileType(Enum):
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

    def __init__(self, source: Optional[Union[cindex.Cursor, str]], parent: Optional[any] = None):
        cursor = None
        if source is not None:
            if not isinstance(source, str):
                cursor = source
            else:
                import clang
                index = clang.cindex.Index.create()
                cursor = index.parse(source, args=["-xc++", "-std=c++17"]).cursor
        super().__init__(cursor, parent)
        self._source = source
        self._cursor = cursor
        if source is None:
            self._path = Path()
            self._text_source = ""
            self._type = SourceFileType.HEADER
            self._includes = []
        else:
            if cursor is None:
                self._cursor = cursor
                self._path = None
                self._text_source = LazyNotInit
                self._includes = LazyNotInit
                self._type = LazyNotInit
            else:
                if cursor.kind != cindex.CursorKind.TRANSLATION_UNIT:
                    raise ParserError("It is not valid cursor kind.")
                self._path = Path(cursor.spelling)
                self._text_source = LazyNotInit
                self._includes = LazyNotInit
                self._type = LazyNotInit
        self._lexicon = Lexicon.create(self)

    @property
    @lazy_invoke
    def type(self) -> SourceFileType:
        """Information abut file type."""
        if self.extension in ["c", "cxx", "cpp", "cxx", "cc"]:
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
    def module(self) -> any:
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

    def _create_content(self) -> List[any]:
        from devana.syntax_abstraction.classinfo import ClassInfo, MethodInfo
        from devana.syntax_abstraction.unioninfo import UnionInfo
        from devana.syntax_abstraction.functioninfo import FunctionInfo
        from devana.syntax_abstraction.typedefinfo import TypedefInfo
        from devana.syntax_abstraction.namespaceinfo import NamespaceInfo
        from devana.syntax_abstraction.usingnamespace import UsingNamespace
        from devana.syntax_abstraction.enuminfo import EnumInfo
        from devana.syntax_abstraction.variable import GlobalVariable
        types = [ClassInfo, UnionInfo, FunctionInfo, EnumInfo, TypedefInfo, NamespaceInfo, UsingNamespace, MethodInfo,
                 GlobalVariable]
        content = []
        for children in self._cursor.get_children():
            if Path(children.location.file.name) != self.path:
                continue
            for t in types:
                try:
                    el = t(children, self)
                except ParserError:
                    continue
                content.append(el)
                break
        return content
