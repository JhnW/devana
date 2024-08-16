from abc import ABC, abstractmethod
from typing import Optional, List, Any


class IDescribedType(ABC):
    """An interface containing a basic description of the type assumed by the property for unambiguous identification.
    Types can be (and often should be) created dynamically along with the creation of properties to provide support
    for example enums."""

    @property
    @abstractmethod
    def name(self) -> str:
        """The full name of the type, including the names of the generic specialization types"""


class IDescribedValue(ABC):
    """Interface describing the possible value taken by property. Its use is to describe property definitions in the
    context of default values, making the parser's work easier and ensuring diagnostic messages of appropriate quality.
    This interface does not apply to actual property values."""

    @property
    @abstractmethod
    def type(self) -> IDescribedType:
        """The type of the current value."""

    @property
    @abstractmethod
    def content_as_string(self) -> str:
        """Test representation of a stored value - without a type, object data, etc. For example, holding the number
        7.5, the text representation will be the string 7.5.
        If no content value is provided, the string should be paired to obtain the correct value."""

    @property
    @abstractmethod
    def content(self) -> Optional[Any]:
        """Provides a value if you need to provide a more reliable or non-standard way to provide values instead of
        relying on the parser when providing default values."""


class IDescribedArgument(ABC):
    """Interface describing the arguments accepted by property."""

    @property
    @abstractmethod
    def type(self) -> IDescribedType:
        """Type of argument."""

    @property
    @abstractmethod
    def default_value(self) -> Optional[IDescribedValue]:
        """Default value of argument, if any."""


class IDescribedProperty(ABC):
    """Description property for parsing and diagnostic messages."""

    @property
    @abstractmethod
    def namespace(self) -> Optional[str]:
        """Namespace in which the property is located (if it is located in any)."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of property."""

    @property
    @abstractmethod
    def arguments(self) -> List[IDescribedArgument]:
        """List of arguments for this property."""
