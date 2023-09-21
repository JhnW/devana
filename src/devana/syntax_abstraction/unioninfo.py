from typing import Optional, List, Any
from clang import cindex
from devana.syntax_abstraction.organizers.codecontainer import CodeContainer
from devana.syntax_abstraction.organizers.lexicon import Lexicon
from devana.syntax_abstraction.classinfo import FieldInfo
from devana.syntax_abstraction.comment import Comment
from devana.utility.lazy import LazyNotInit, lazy_invoke
from devana.utility.errors import ParserError
from devana.syntax_abstraction.syntax import ISyntaxElement


class UnionInfo(CodeContainer):
    """Named or anonymous union."""

    def __init__(self, cursor: Optional[cindex.Cursor] = None, parent: Optional[CodeContainer] = None):
        super().__init__(cursor, parent)
        if cursor is None:
            self._name = "TestUnion"
            self._is_declaration = False
            self._associated_comment = None
        else:
            self._name = LazyNotInit
            self._is_declaration = LazyNotInit
            if not self.is_cursor_valid(cursor):
                raise ParserError("It is not a valid type cursor.")
            self._associated_comment = LazyNotInit
        self._lexicon = Lexicon.create(self)

    @staticmethod
    def is_cursor_valid(cursor: cindex.Cursor) -> bool:
        return cursor.kind == cindex.CursorKind.UNION_DECL

    @property
    @lazy_invoke
    def name(self) -> Optional[str]:
        """Name of union or None is anonymous."""
        tokens = list(self._cursor.get_tokens())
        is_set = False
        if len(tokens) >= 2:
            if tokens[0].spelling == "union" and tokens[1].spelling == "{":
                self._name = None
                is_set = True
        if not is_set:
            self._name = self._cursor.displayname
        if not self._name:
            self._name = None
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    @lazy_invoke
    def is_declaration(self) -> bool:
        """Determine kind, definition or declaration."""
        self._is_declaration = True
        for token in self._cursor.get_tokens():
            if "{" == token.spelling:
                self._is_declaration = False
                break
        return self._is_declaration

    @is_declaration.setter
    def is_declaration(self, value):
        self._is_declaration = value

    @property
    def is_definition(self) -> bool:
        """Determine function kind, definition or declaration."""
        return not self.is_declaration

    @is_definition.setter
    def is_definition(self, value):
        self._is_declaration = not value

    @property
    def definition(self) -> Optional[Any]:
        """Definition of union."""
        if self.name in None:
            return None
        if self.is_definition:
            return self
        return self._lexicon.find_type(self.name)

    @property
    def lexicon(self):
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

    @property
    def _content_types(self) -> List:
        return [FieldInfo]

    def __repr__(self):
        return f"{type(self).__name__}:{self.name} ({super().__repr__()})"
