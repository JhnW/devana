from devana.utility.lazy import LazyNotInit, lazy_invoke
from devana.syntax_abstraction.organizers.codecontainer import CodeContainer
from devana.syntax_abstraction.organizers.lexicon import Lexicon
from clang import cindex
from typing import Optional, List
from devana.syntax_abstraction.classinfo import FieldInfo
from devana.utility.errors import ParserError


class UnionInfo(CodeContainer):
    """Named or anonymous union."""

    def __init__(self, cursor: Optional[cindex.Cursor] = None, parent: Optional[CodeContainer] = None):
        super().__init__(cursor, parent)
        if cursor is None:
            self._name = None
            self._is_declaration = False
        else:
            self._name = LazyNotInit
            self._is_declaration = LazyNotInit
        if cursor.kind != cindex.CursorKind.UNION_DECL:
            raise ParserError("It is not a valid type cursor.")
        self._lexicon = Lexicon.create(self)

    @property
    @lazy_invoke
    def name(self) -> Optional[str]:
        """Name of union or None is is anonymous."""
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
    def definition(self) -> Optional[any]:
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

    def _create_content(self) -> List[any]:
        types = [FieldInfo]
        content = []
        for children in self._cursor.get_children():
            for t in types:
                try:
                    el = t(children, self)
                except ValueError:
                    continue
                content.append(el)
                break
        return content
