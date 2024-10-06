import re
from typing import Optional, Any, Union, Type, Dict
from abc import ABC, abstractmethod
from dataclasses import dataclass
from devana.preprocessing.components.property.parsers.descriptions import IDescribedType

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


class IParsableType(IParsableElement, IDescribedType, ABC):
    """Mix of two interfaces needed by parser."""


class ParsingBackend:
    """Core backend for all parser."""

    @dataclass
    class Argument:
        """Class holding result arguments."""
        value: Any
        type: IDescribedType
        name: Optional[str] = None


    def __init__(self):
        self._types: Dict[str, IParsableElement] = {}

    @property
    def types(self) -> Dict[str, IParsableElement]:
        return self._types

    def add_type(self, element: IParsableType):
        """Add a new type to parser. May raise exceptions for duplicate types."""
        if element.name not in self._types:
            self._types[element.name] = element
        if element != self._types[element.name]:
            raise ValueError("Duplicate type name.")

    #__argument_pattern = re.compile(r'(^\s*(?P<name>(\w|")+)\s*=\s*(?P<named_value>\w+)\s*$)|^\s*(?P<value>(\w|")+)\s*$')

    __argument_pattern = re.compile(
        r'(^\s*(?P<name>\w+)\s*=\s*(?P<named_value>.+)\s*$)|^\s*(?P<value>.+)\s*$')


    @dataclass
    class ParsedValue:
        """Internal value parsing result."""
        text: str
        type: IDescribedType


    def _parse_value(self, text: str) -> ParsedValue:
        for t in self._types.values():
            result = t.parse(text)
            if isinstance(result, ParsableElementError):
                if result.is_meaningless:
                    continue
                raise ValueError(f"Parsing error: {result.what}")
            return ParsingBackend.ParsedValue(result, t)
        raise ValueError("Unable to find matching type.")

    def parse_argument(self, text: str) -> Argument:
        match = self.__argument_pattern.match(text)
        if match is None:
            raise ValueError("Cannot parse argument.")
        matches = match.groupdict()
        if matches["value"] is not None:
            parsing_result = self._parse_value(matches["value"])
            return self.Argument(parsing_result.text, parsing_result.type)
        elif matches["named_value"] is not None and matches["name"] is not None:
            parsing_result = self._parse_value(matches["named_value"])
            return self.Argument(parsing_result.text, parsing_result.type, matches["name"])
        else:
            raise ValueError("Cannot parse argument.")
