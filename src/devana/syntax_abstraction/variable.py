from clang import cindex
from typing import Optional
from devana.syntax_abstraction.codepiece import CodePiece
from devana.syntax_abstraction.typeexpression import TypeExpression
from devana.utility.lazy import LazyNotInit, lazy_invoke
from devana.utility.errors import ParserError
from devana.syntax_abstraction.organizers.lexicon import Lexicon


class Variable:
    """Data about variable used in code"""

    def __init__(self, cursor: Optional[cindex.Cursor] = None, parent: Optional = None):
        self._cursor = cursor
        self._parent = parent
        if cursor is None:
            self._name = ""
            self._type = None
            self._text_source = None
            self._default_value = None
        else:
            self._name = LazyNotInit
            self._type = LazyNotInit
            self._text_source = LazyNotInit
            self._default_value = LazyNotInit
        self._lexicon = Lexicon.create(self)

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
    def default_value(self) -> Optional[any]:
        """Default value assigned to variable."""
        self._default_value = None
        import re
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
    def parent(self) -> any:
        """Object scope of usage this data."""
        return self._parent

    @property
    def lexicon(self):
        return self._lexicon

    @lexicon.setter
    def lexicon(self, value):
        self._lexicon = value


class GlobalVariable(Variable):
    """Data about global, independent variable used in code (out of class scope)"""

    def __init__(self, cursor: Optional[cindex.Cursor] = None, parent: Optional = None):
        super().__init__(cursor, parent)
        if cursor is not None:
            if cursor.kind != cindex.CursorKind.VAR_DECL:
                raise ParserError("Invalid cursor kind of global variable.")
