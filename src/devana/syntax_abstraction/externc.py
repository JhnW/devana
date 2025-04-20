from typing import Optional, List, Any
from clang import cindex
from devana.syntax_abstraction.organizers.codecontainer import CodeContainer
from devana.syntax_abstraction.organizers.lexicon import Lexicon
from devana.syntax_abstraction.functioninfo import FunctionInfo
from devana.syntax_abstraction.syntax import ISyntaxElement
from devana.utility.errors import ParserError
from devana.utility.lazy import lazy_invoke
from devana.utility.init_params import init_params


class ExternC(CodeContainer):
    """Object representation of current usage of extern C set of functions. It may contain one or more functions."""

    def __init__(self, cursor: Optional[cindex.Cursor] = None, parent: Optional[CodeContainer] = None):
        super().__init__(cursor, parent)
        if cursor is not None:
            if self._cursor.kind != cindex.CursorKind.LINKAGE_SPEC:
                raise ParserError("It is not a valid type cursor.")
            if len(list(self._cursor.get_children())) <= 0:
                raise ParserError("It is not a valid type cursor.")
            for children in self._cursor.get_children():
                if children.kind != cindex.CursorKind.FUNCTION_DECL:
                    raise ParserError("It is not a valid type cursor. ExternC allow only functions content.")
        self._name = 'extern "C"'
        self._namespace = None
        self._lexicon = Lexicon.create(self)

    @classmethod
    @init_params(skip={"parent"})
    def from_params( # pylint: disable=unused-argument, too-many-positional-arguments
            cls,
            parent: Optional[ISyntaxElement] = None,
            content: Optional[List[Any]] = None,
            namespace: Optional[str] = None,
            name: Optional[str] = None,
            lexicon: Optional[Lexicon] = None
    ):
        return cls(None, parent)

    @staticmethod
    def is_cursor_valid(cursor: cindex.Cursor) -> bool:
        if cursor.kind != cindex.CursorKind.LINKAGE_SPEC:
            return False
        if len(list(cursor.get_children())) <= 0:
            return False
        for children in cursor.get_children():
            if children.kind != cindex.CursorKind.FUNCTION_DECL:
                return False
        return True

    @property
    @lazy_invoke
    def name(self) -> str:
        self._name = self._cursor.displayname
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def lexicon(self) -> Lexicon:
        return self._lexicon

    @lexicon.setter
    def lexicon(self, value):
        self._lexicon = value

    @property
    def _content_types(self) -> List:
        return [FunctionInfo]
