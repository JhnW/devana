from typing import List, Union, Type
import re
from devana.preprocessing.components.property.parsers.descriptions import IDescribedType
from devana.preprocessing.components.property.parsers.parser import IParsableElement, ParsableElementError


class IntegerType(IDescribedType, IParsableElement):
    """Representation of integer number."""

    @property
    def name(self) -> str:
        return "Integer"

    __pattern = re.compile(r"^\s*([-+]?\d+)\s*$")

    def parse(self, text: str) -> Union[ParsableElementError, int]:
        match = self.__pattern.match(text)
        if match:
            return int(match.group(1))
        return ParsableElementError()

    @property
    def result_type(self) -> Type:
        return int


class FloatType(IDescribedType, IParsableElement):
    """Representation of floating point number."""

    @property
    def name(self) -> str:
        return "Float"

    __pattern = re.compile(r"^\s*([+-]?\d+\.?\d*)\s*$")

    def parse(self, text: str) -> Union[ParsableElementError, float]:
        match = self.__pattern.match(text)
        if match:
            return float(match.group(1))
        return ParsableElementError()

    @property
    def result_type(self) -> Type:
        return float


class StringType(IDescribedType, IParsableElement):
    """Representation of text."""

    @property
    def name(self) -> str:
        return "String"

    __pattern = re.compile(r'^\s*\"(.*)\"\s*$')

    def parse(self, text: str) -> Union[ParsableElementError, str]:
        match = self.__pattern.match(text)
        if match:
            return match.group(1)
        return ParsableElementError()

    @property
    def result_type(self) -> Type:
        return str


class BooleanType(IDescribedType, IParsableElement):
    """Representation of true/false."""

    @property
    def name(self) -> str:
        return "Boolean"

    __pattern = re.compile(r"^\s*(true|false)\s*$")

    def parse(self, text: str) -> Union[ParsableElementError, bool]:
        match = self.__pattern.match(text)
        if match:
            if match.group(1) == "true":
                return True
            elif match.group(1) == "false":
                return False
            else:
                return ParsableElementError()
        return ParsableElementError()

    @property
    def result_type(self) -> Type:
        return bool


class EnumType(IDescribedType):
    """Representation of enum."""
    def __init__(self, name: str, values: List[str]):
        self._name = name
        self._values = values

    @property
    def values(self) -> List[str]:
        return self._values

    @property
    def name(self) -> str:
        return f"Enum {self.name}"


class _GenericType(IDescribedType):
    """internal mixin for generic implementation."""
    def __init__(self, name: str, specialization: IDescribedType):
        self._name = name
        self._specialization = specialization

    @property
    def specialization(self) -> IDescribedType:
        return self._specialization

    @property
    def name(self) -> str:
        return f"{self.name}<{self.specialization.name}>"


class ListType(_GenericType):
    """internal of list like []"""
    def __init__(self, specialization: IDescribedType):
        super().__init__("List", specialization)


class OptionalType(_GenericType):
    """internal of optional can be value of specialization type or none."""
    def __init__(self, specialization: IDescribedType):
        super().__init__("Optional", specialization)


class UnionType(IDescribedType):
    """internal of union type can be value of many types."""
    def __init__(self, types: List[IDescribedType]):
        self._types = types

    @property
    def types(self) -> List[IDescribedType]:
        return self._types

    @property
    def name(self) -> str:
        return f"Union<{'|'.join([s.name for s in self._types])}>"
