import re
from typing import Optional
from clang import cindex
from devana.syntax_abstraction.codepiece import CodePiece
from devana.syntax_abstraction.typeexpression import TypeExpression
from devana.syntax_abstraction.comment import Comment
from devana.syntax_abstraction.organizers.lexicon import Lexicon
from devana.utility.lazy import LazyNotInit, lazy_invoke
from devana.utility.errors import ParserError
from devana.utility.traits import IBasicCreatable, ICursorValidate
from devana.syntax_abstraction.syntax import ISyntaxElement


class Variable(IBasicCreatable, ISyntaxElement):
    """Data about variable used in code"""

    def __init__(self, cursor: Optional[cindex.Cursor] = None, parent: Optional = None):
        self._cursor = cursor
        self._parent = parent
        if cursor is None:
            self._name = "myVariable"
            self._type = TypeExpression.create_default(parent)
            self._text_source = None
            self._default_value = None
        else:
            self._name = LazyNotInit
            self._type = LazyNotInit
            self._text_source = LazyNotInit
            self._default_value = LazyNotInit
        self._lexicon = Lexicon.create(self)

    @classmethod
    def create_default(cls, parent: Optional = None) -> "Variable":
        result = cls(None, parent)
        return result

    @classmethod
    def from_cursor(cls, cursor: cindex.Cursor, parent: Optional = None) -> Optional["Variable"]:
        result = cls(cursor, parent)
        return result

    @property
    @lazy_invoke
    def name(self) -> str:
        """Variable name."""
        self._name = self._cursor.spelling
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    @lazy_invoke
    def type(self) -> TypeExpression:
        """Variable type."""
        self._type = TypeExpression(self._cursor, self)
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    @lazy_invoke
    def default_value(self) -> Optional[str]:
        """Default value assigned to variable."""
        self._default_value = None
        pattern = r".+=\s*(.+)"
        matches = re.search(pattern, self.text_source.text)
        if matches is not None:
            self._default_value = matches.group(1)
        return self._default_value

    @default_value.setter
    def default_value(self, value):
        self._default_value = value

    @property
    @lazy_invoke
    def text_source(self) -> CodePiece:
        """Source of this element."""
        self._text_source = CodePiece(self._cursor)
        return self._text_source

    @property
    def parent(self) -> ISyntaxElement:
        """Object scope of usage this data."""
        return self._parent

    @property
    def lexicon(self):
        return self._lexicon

    @lexicon.setter
    def lexicon(self, value):
        self._lexicon = value

    def __repr__(self):
        return f"{type(self).__name__}:{self.name} ({super().__repr__()})"


class GlobalVariable(Variable, ICursorValidate):
    """Data about global, independent variable used in code (out of class scope)"""

    def __init__(self, cursor: Optional[cindex.Cursor] = None, parent: Optional = None):
        super().__init__(cursor, parent)
        if cursor is not None:
            if not self.is_cursor_valid(cursor):
                raise ParserError("Invalid cursor kind of global variable.")
        if cursor is None:
            self._associated_comment = None
        else:
            self._associated_comment = LazyNotInit

    @staticmethod
    def is_cursor_valid(cursor: cindex.Cursor) -> bool:
        return cursor.kind == cindex.CursorKind.VAR_DECL

    @classmethod
    def from_cursor(cls, cursor: cindex.Cursor, parent: Optional = None) -> Optional["GlobalVariable"]:
        if not cls.is_cursor_valid(cursor):
            return None
        result = cls(cursor, parent)
        return result

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
