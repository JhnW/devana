from abc import ABC, abstractmethod
from clang import cindex
from typing import Optional


class ICursorValidate(ABC):

    @staticmethod
    @abstractmethod
    def is_cursor_valid(cursor: cindex.Cursor) -> bool:
        """It checks if it is possible to create a valid object on the basis of the rate."""
        pass


class IDefaultCreatable(ABC):

    @classmethod
    @abstractmethod
    def create_default(cls, parent: Optional = None) -> any:
        """Create a default, valid instance. Cls parameter allow to implemented this method once if
        init meets requirements in all derivative types."""
        pass


class IFromCursorCreatable(ABC):

    @classmethod
    @abstractmethod
    def from_cursor(cls, cursor: cindex.Cursor, parent: Optional = None) -> Optional:
        """"Create a instance from parsed information from clang. Return None if creation is not possible. Cls parameter
        allow to implemented this method once if init meets requirements in all derivative types."""
        pass


class IBasicCreatable(IDefaultCreatable, IFromCursorCreatable, ABC):
    """An interface that describes a set of constructors for a code element."""
    pass


class IFromParamsCreatable(ABC):

    @classmethod
    @abstractmethod
    def from_params(cls, *argv):
        """Multi-parameter constructor. Similar to the default value, except that it allows
        you to set some basic properties."""
        pass
