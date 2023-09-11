from abc import ABC, abstractmethod
from typing import Optional, List, Any
from clang import cindex
from devana.syntax_abstraction.codepiece import CodePiece
from devana.utility.lazy import LazyNotInit, lazy_invoke
from devana.utility.traits import IBasicCreatable, ICursorValidate
from devana.configuration import Configuration, ParsingErrorPolicy
from devana.utility.errors import ParserError
from devana.syntax_abstraction.syntax import ISyntaxElement


class CodeContainer(IBasicCreatable, ICursorValidate, ISyntaxElement, ABC):
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

    @classmethod
    def from_cursor(cls, cursor: cindex.Cursor, parent: Optional = None) -> Optional:
        if not cls.is_cursor_valid(cursor):
            return None
        return cls(cursor, parent)

    @classmethod
    def create_default(cls, parent: Optional = None) -> Any:
        return cls(None, parent)

    @property
    @lazy_invoke
    def content(self) -> List[Any]:
        """List of source code objects."""
        self._content = list(self._create_content())
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
    def parent(self) -> Optional[Any]:
        """Higher in the hierarchy scope, if any. In most cases another CodeContainer."""
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value

    @property
    def lexicon(self) -> Any:
        """Current lexicon storage of an object."""
        return None

    @property
    def allowed_namespaces(self) -> List:
        """List of all others allowed namespaces in container without Name:: prefix given by using namespace."""
        if self.lexicon is not None:
            return self.lexicon.allowed_namespaces # noqa
        from devana.syntax_abstraction.usingnamespace import UsingNamespace  # pylint: disable=import-outside-toplevel
        allowed = []
        for c in self.content:
            if isinstance(c, UsingNamespace):
                if c.namespace is not None:
                    allowed += c.namespace.allowed_namespaces # noqa
        if self.namespace is not None:
            allowed.append(self)
        return allowed

    @property
    @lazy_invoke
    def text_source(self) -> Optional[CodePiece]:
        self._text_source = CodePiece(self._cursor)
        return self._text_source

    @property
    @abstractmethod
    def _content_types(self) -> List:
        """Overwrite this method to feed _create_content with a list of types."""

    def _create_content(self) -> List[Any]:
        """Overwrite this method to filter witch content should be parsed inside class."""
        types = self._content_types
        content = []
        config = Configuration.get_configuration(self)
        is_abort_on_error = config.parsing.error_strategy == ParsingErrorPolicy.ABORT
        is_ignore_on_error = config.parsing.error_strategy == ParsingErrorPolicy.IGNORE
        for children in self._cursor.get_children():
            element: Optional = None
            for t in types:
                try:
                    element = t.from_cursor(children, self)
                    if element is None:
                        continue
                    break
                except ParserError:
                    if is_ignore_on_error:
                        continue
                    if is_abort_on_error:
                        raise
                    config.logger.warning("Parser error during create content of %s in type %s "
                                          "for cursor %s.", self, t, children.spelling)
                    continue
            if element is None:
                if is_ignore_on_error:
                    continue
                if is_abort_on_error:
                    raise ParserError(f"Cannot match any type for content of {self} n cursor {children.spelling}.")
                config.logger.warning("Cannot match any type for content of %s n cursor %s.",
                                      self, children.spelling)
                continue
            content.append(element)
        return content
