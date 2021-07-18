from clang import cindex
from typing import Optional, Union
from devana.syntax_abstraction.codepiece import CodePiece
from devana.syntax_abstraction.typeexpression import TypeExpression
from devana.syntax_abstraction.organizers.codecontainer import CodeContainer
from devana.utility.errors import ParserError
from devana.utility.lazy import LazyNotInit, lazy_invoke
from devana.syntax_abstraction.organizers.lexicon import Lexicon


class TypedefInfo:
    """Class represented typedef declaration."""

    def __init__(self, cursor: Optional[cindex.Cursor] = None, parent: Optional[CodeContainer] = None):
        self._cursor = cursor
        self._parent = parent
        if cursor is None:
            self._type_info = None
            self._text_source = None
            self._name = ""
        else:
            if self._cursor.kind != cindex.CursorKind.TYPEDEF_DECL:
                raise ParserError("Element is not typedef.")
            self._type_info = LazyNotInit
            self._text_source = LazyNotInit
            self._name = LazyNotInit
        self._lexicon = Lexicon.create(self)

    @property
    @lazy_invoke
    def type_info(self) -> Union[TypeExpression, any]:
        """Type alias, can be true type or next typedef."""
        self._type_info = TypeExpression(self._cursor, self)
        return self._type_info

    @type_info.setter
    def type_info(self, value):
        self._type_info = value

    @property
    @lazy_invoke
    def name(self) -> str:
        """Typedef alias name."""
        self._name = self._cursor.type.get_typedef_name()
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    @lazy_invoke
    def text_source(self) -> Optional[CodePiece]:
        """Source of this element."""
        self._text_source = CodePiece(self._cursor)
        return self._text_source

    @property
    def parent(self) -> CodeContainer:
        """Structural parent element like file, namespace or class."""
        return self._parent

    @property
    def lexicon(self) -> CodeContainer:
        """Current lexicon storage of object."""
        return self._lexicon

    @lexicon.setter
    def lexicon(self, value):
        self._lexicon = value
