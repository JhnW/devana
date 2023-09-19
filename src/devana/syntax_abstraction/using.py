from typing import Optional, Union
from clang import cindex
from devana.syntax_abstraction.codepiece import CodePiece
from devana.syntax_abstraction.typeexpression import TypeExpression
from devana.syntax_abstraction.organizers.codecontainer import CodeContainer
from devana.syntax_abstraction.comment import Comment
from devana.syntax_abstraction.organizers.lexicon import Lexicon
from devana.utility.errors import ParserError
from devana.utility.lazy import LazyNotInit, lazy_invoke
from devana.utility.traits import IFromCursorCreatable, ICursorValidate
from devana.syntax_abstraction.syntax import ISyntaxElement


class Using(IFromCursorCreatable, ICursorValidate, ISyntaxElement):
    """Class represented typedef declaration e.g., using AliasTypeName = const namespace::namespace::Type.
    Using without "=" as using namespace::Type; is not supported."""

    def __init__(self, cursor: Optional[cindex.Cursor] = None, parent: Optional[CodeContainer] = None):
        self._cursor = cursor
        self._parent = parent
        if cursor is None:
            self._type_info = None
            self._text_source = None
            self._name = ""
            self._associated_comment = None
        else:
            if not self.is_cursor_valid(cursor):
                raise ParserError("Element is not using type alias.")
            self._type_info = LazyNotInit
            self._text_source = LazyNotInit
            self._name = LazyNotInit
            self._associated_comment = LazyNotInit
        self._lexicon = Lexicon.create(self)

    @classmethod
    def from_cursor(cls, cursor: cindex.Cursor, parent: Optional = None) -> Optional["Using"]:
        if not cls.is_cursor_valid(cursor):
            return None
        return cls(cursor, parent)

    @staticmethod
    def is_cursor_valid(cursor: cindex.Cursor) -> bool:
        return cursor.kind == cindex.CursorKind.TYPE_ALIAS_DECL

    @property
    @lazy_invoke
    def type_info(self) -> Union[TypeExpression, "ISyntaxElement"]:
        """Type alias can be true type or next typedef."""
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

    @property
    @lazy_invoke
    def associated_comment(self) -> Optional[Comment]:
        parent = self.parent
        while parent is not None:
            if hasattr(parent, "bind_comment"):
                self._associated_comment = parent.bind_comment(self)
                return self._associated_comment
            parent = parent.parent

        return None

    @associated_comment.setter
    def associated_comment(self, value):
        self._associated_comment = value

    def __repr__(self):
        return f"{type(self).__name__}:{self.name} ({super().__repr__()})"
