from abc import ABC, abstractmethod
from typing import Optional
from clang import cindex



class ICursorValidate(ABC):
    """An interface that specifies that an object can only work with certain types of clang cursors."""

    @staticmethod
    @abstractmethod
    def is_cursor_valid(cursor: cindex.Cursor) -> bool:
        """It checks if it is possible to create a valid object on the basis of the rate."""


class IDefaultCreatable(ABC):
    """The interface of an object that can be created with default sets of values."""

    @classmethod
    @abstractmethod
    def create_default(cls, parent: Optional = None) -> any:
        """Create a default, valid instance. Cls parameter allow to implement this method once if
        init meets requirements in all derivative types."""


class IFromCursorCreatable(ABC):
    """The interface of an object that can be created from many clang cursor."""

    @classmethod
    @abstractmethod
    def from_cursor(cls, cursor: cindex.Cursor, parent: Optional = None) -> Optional:
        """Create an instance from parsed information from clang. Return None if creation is not possible.
        Cls parameter allow to implement this method once if init meets requirements in all derivative types."""


class IBasicCreatable(IDefaultCreatable, IFromCursorCreatable, ABC):
    """An interface that describes a set of constructors for a code element."""


class IFromParamsCreatable(ABC):
    """The interface of an object that can be created from many parameters."""

    @classmethod
    @abstractmethod
    def from_params(cls, *argv):
        """Multi-parameter constructor. Similar to the default value, except that it allows
        you to set some basic properties."""
