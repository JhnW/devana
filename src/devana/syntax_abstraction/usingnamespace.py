from devana.syntax_abstraction.codepiece import CodePiece
from clang import cindex
from devana.syntax_abstraction.organizers.codecontainer import CodeContainer
from devana.utility.lazy import LazyNotInit, lazy_invoke
from devana.utility.errors import ParserError
from typing import Optional, List, Union
from devana.syntax_abstraction.organizers.lexicon import Lexicon


class UsingNamespace:
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
                raise ParserError("Template parameter expect USING_DIRECTIVE cursor kind.")
            self._namespace = LazyNotInit
            self._namespaces = LazyNotInit
            self._text_source = LazyNotInit
        self._lexicon = Lexicon.create(self)

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
    def parent(self) -> Optional[any]:
        """Higher in the hierarchy scope, if any. In most cases another CodeContainer."""
        return self._parent

    @property
    def lexicon(self):
        return self._lexicon

    @lexicon.setter
    def lexicon(self, value):
        self._lexicon = value
