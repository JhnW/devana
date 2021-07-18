from clang import cindex
from typing import Optional, List, Tuple
from devana.utility.lazy import LazyNotInit, lazy_invoke
from devana.syntax_abstraction.codepiece import CodePiece


class CodeContainer:
    """Class representing part of code source who is able to hold other sources in his body."""

    def __init__(self, cursor: Optional[cindex.Cursor] = None, parent: Optional = None):
        self._cursor = cursor
        self._parent = parent
        if cursor is None:
            self._namespace = None
            self._content = []
            self._text_source = None
        else:
            self._namespace = LazyNotInit
            self._content = LazyNotInit
            self._text_source = LazyNotInit

    @property
    @lazy_invoke
    def content(self) -> Tuple[any]:
        """List of source code objects."""
        self._content = tuple(self._create_content())
        return self._content

    @content.setter
    def content(self, value):
        self._content = value

    @property
    @lazy_invoke
    def namespace(self) -> Optional[str]:
        """Namespace name if any."""
        self._namespace = self._cursor.spelling
        return self._namespace

    @namespace.setter
    def namespace(self, value):
        self._namespace = value

    @property
    def parent(self) -> Optional[any]:
        """Higher in the hierarchy scope, if any. In most cases another CodeContainer."""
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value

    @property
    def lexicon(self) -> any:
        """Current lexicon storage of object."""
        return None

    @property
    def allowed_namespaces(self) -> List:
        """List of all other allowed namespaces in container without Name:: prefix given by using namespace."""
        if self.lexicon is not None:
            return self.lexicon.allowed_namespaces
        from devana.syntax_abstraction.usingnamespace import UsingNamespace
        allowed = []
        for c in self.content:
            if isinstance(c, UsingNamespace):
                if c.namespace is not None:
                    allowed += c.namespace.allowed_namespaces
        if self.namespace is not None:
            allowed.append(self)
        return allowed

    @property
    @lazy_invoke
    def text_source(self) -> Optional[CodePiece]:
        self._text_source = CodePiece(self._cursor)
        return self._text_source

    def _create_content(self) -> List[any]:
        """Overwrite this method to filter witch content should be parsed inside class."""
        types = []
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
