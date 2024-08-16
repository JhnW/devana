from typing import Optional, Any, Union, Type
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ParsableElementError:
    """Possible parsing errors"""
    what: Optional[str] = None
    """Error description. In most cases it will be empty allowing fallback to other types."""

    @property
    def is_meaningless(self) -> bool:
        """Indicates when an error is used for fallback - it is not an actual user syntax error."""
        return self.what is None


class IParsableElement(ABC):
    """A class that performs basic data parsing - the smallest component, for example, a type."""

    @abstractmethod
    def parse(self, text: str) -> Union[ParsableElementError, Any]:
        """Extraxt python data from text."""

    @property
    @abstractmethod
    def result_type(self) -> Type:
        """Python type of result."""
