from abc import ABC, abstractmethod
from clang import cindex
from typing import Optional
from devana.syntax_abstraction.organizers.lexicon import Lexicon


class IDefaultCreatable(ABC):

    @classmethod
    @abstractmethod
    def create_default(cls, parent: Optional = None) -> any:
        """Create a default, valid instance. Cls parameter allow to implemented this method once if
        init meets requirements in all derivative types."""
        pass


class ICursorValidate(ABC):

    @staticmethod
    @abstractmethod
    def is_cursor_valid(cursor: cindex.Cursor) -> bool:
        pass


class IFromCursorCreatable(ABC):

    @classmethod
    @abstractmethod
    def from_cursor(cls, cursor: cindex.Cursor, parent: Optional = None) -> Optional:
        """"Create a instance from parsed information from clang. Return None if creation is not possible. Cls parameter
        allow to implemented this method once if init meets requirements in all derivative types."""
        pass


class ICreatable(IDefaultCreatable, IFromCursorCreatable, ABC):
    """An interface that describes a set of constructors for a code element."""
    pass




# class ICodePrimitivePrimitive(ABC):
#     """Repeatable code element as a function parameter or field."""
#     pass
#
#
# class ILexiconElement(ABC):
#     """Code element that is in the lexicon. Applies to namespaces, types, functions, methods, etc."""
#     pass
#
#
# class ISyntaxElement(ABC):
#     """Basic syntax element."""
#
#     @staticmethod
#     @abstractmethod
#     def create_default(cls, parent=None) -> any:
#         """Create a default, valid instance."""
#         pass
#
#     @staticmethod
#     @abstractmethod
#     def from_cursor(cls, cursor: cindex.Cursor, parent=None) -> Optional[any]:
#         """"Create a instance from parsed information from clang. Return None if creation is not possible."""
#         pass
#
#
# class ISyntaxType(ABC):
#     """TODO: write doc"""
#
#     @abstractmethod
#     @property
#     def name(self) -> Optional[str]:
#         pass
#
#     @abstractmethod
#     @property
#     def is_definition(self) -> bool:
#         pass
#
#     @abstractmethod
#     @property
#     def is_declaration(self) -> bool:
#         pass
#
#     @abstractmethod
#     @property
#     def is_unnamed(self) -> bool:
#         pass
