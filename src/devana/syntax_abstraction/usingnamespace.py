from typing import Optional, List, Union
from clang import cindex
from devana.syntax_abstraction.codepiece import CodePiece
from devana.syntax_abstraction.organizers.codecontainer import CodeContainer
from devana.syntax_abstraction.organizers.lexicon import Lexicon
from devana.utility.lazy import LazyNotInit, lazy_invoke
from devana.utility.errors import ParserError
from devana.utility.traits import IFromCursorCreatable, ICursorValidate
from devana.syntax_abstraction.syntax import ISyntaxElement


class UsingNamespace(IFromCursorCreatable, ICursorValidate, ISyntaxElement):
    """Using namespace in scope."""

    def __init__(self, cursor: Optional[cindex.Cursor] = None, parent: Optional[CodeContainer] = None):
        self._cursor = cursor
        self._parent = parent
        if cursor is None:
            self._namespace = None
            self._namespaces = []
            self._text_source = None
        else:
            if cursor.kind != cindex.CursorKind.USING_DIRECTIVE:
                raise ParserError("Expect USING_DIRECTIVE cursor kind.")
            self._namespace = LazyNotInit
            self._namespaces = LazyNotInit
            self._text_source = LazyNotInit
        self._lexicon = Lexicon.create(self)

    @classmethod
    def from_cursor(cls, cursor: cindex.Cursor, parent: Optional = None) -> Optional["UsingNamespace"]:
        if not cls.is_cursor_valid(cursor):
            return None
        return cls(cursor, parent)

    @classmethod
    def from_namespace(cls, namespace: str, parent: Optional = None) -> "UsingNamespace":
        result = cls(None, parent)
        result._namespace = namespace
        return result

    @staticmethod
    def is_cursor_valid(cursor: cindex.Cursor) -> bool:
        return cursor.kind == cindex.CursorKind.USING_DIRECTIVE

    @property
    @lazy_invoke
    def namespaces(self) -> Union[List[str], List[Lexicon]]:
        self._namespaces = []
        if self._lexicon is None:
            for children in self._cursor.get_children():
                self._namespaces.append(children.spelling)
        else:
            def get_namespaces(children_list: List, container: Lexicon, result: List):
                if not children_list:
                    return result
                content = [n for n in container.nodes if n.namespace == children_list[0].spelling]
                if not content:
                    return result
                if content[0].parent is None:
                    return result
                result.append(content[0])
                return get_namespaces(children_list[1:], content[0], result)

            self._namespaces = get_namespaces(list(self._cursor.get_children()), self.lexicon, [])
        return self._namespaces

    @namespaces.setter
    def namespaces(self, value):
        self._namespaces = value

    @property
    @lazy_invoke
    def namespace(self) -> Optional[str]:
        if len(self.namespaces) == 0:
            return None
        return self.namespaces[-1]

    @property
    @lazy_invoke
    def text_source(self) -> Optional[CodePiece]:
        """Source of this element."""
        self._text_source = CodePiece(self._cursor)
        return self._text_source

    @property
    def parent(self) -> Optional[ISyntaxElement]:
        """Higher in the hierarchy scope, if any. In most cases, another CodeContainer."""
        return self._parent

    @property
    def lexicon(self):
        return self._lexicon

    @lexicon.setter
    def lexicon(self, value):
        self._lexicon = value

    def __repr__(self):
        namespace = "NONE" if self.namespace is None else self.namespace
        return f"{type(self).__name__}:{namespace} ({super().__repr__()})"
