import typing
from enum import Enum, auto, EnumMeta
from typing import Callable, List, Optional
from dataclasses import dataclass
from devana.preprocessing.sources.source import ISource


class TypeKind(Enum):
    """The type of token used in live tool configuration - as function data."""
    REAL = auto()
    INT = auto()
    STRING = auto()
    BOOL = auto()
    ENUM = auto()
    OPTIONAL = auto()


@dataclass
class TypeInformation:
    """Details about used type of argument."""
    kind: TypeKind
    details: Optional[any] = None

    @classmethod
    def from_type(cls, type_data: type) -> "TypeInformation":
        if type_data is str:
            return TypeInformation(TypeKind.STRING)
        elif type_data is bool:
            return TypeInformation(TypeKind.BOOL)
        elif type_data is float:
            return TypeInformation(TypeKind.REAL)
        elif type_data is int:
            return TypeInformation(TypeKind.INT)
        elif isinstance(type_data, EnumMeta):
            return TypeInformation(TypeKind.ENUM, type_data)
        elif cls._is_optional(type_data):
            internal_type = list(typing.get_args(type_data))
            internal_type.remove(type(None))
            return TypeInformation(TypeKind.OPTIONAL, cls.from_type(internal_type[0]))
        else:
            raise ValueError(f"{type_data} is not vail type")

    @staticmethod
    def _is_optional(type_data: type) -> bool:
        if typing.get_origin(type_data) is typing.Union and type(None) in typing.get_args(type_data):
            return True
        return False


@dataclass
class Argument:
    """Argument from data parsing"""
    name: str
    type: TypeInformation
    has_default: bool = False


class DataSignature:
    """Signature of parsing input data, in most of the cases from source file, but it can be used to generate
    foreign file schema reader."""

    def __init__(self, fnc: Callable, name: str, arguments: List[Argument]):
        self._name = name
        self._arguments = arguments
        self._function = fnc

    @staticmethod
    def _is_optional(type_data: type) -> bool:
        if typing.get_origin(type_data) is typing.Union and type(None) in typing.get_args(type_data):
            return True
        return False

    @classmethod
    def from_callable(cls, fnc: Callable):
        fnc_name: str = fnc.__name__
        arguments_names = []
        if hasattr(fnc, "__code__"):
            arguments_names = fnc.__code__.co_varnames
        arguments_values_size = 0
        if hasattr(fnc, "__defaults__"):
            arguments_values_size = 0 if fnc.__defaults__ is None else len(fnc.__defaults__)
        hints = typing.get_type_hints(fnc)

        if len(arguments_names) < 1:
            raise ValueError("Expected minimum one argument taken by callable.")
        source_type = hints[arguments_names[0]]
        if source_type is not ISource:
            raise ValueError("First argument must be ISource")

        arguments_names = arguments_names[1:]
        arguments = []

        for i, name in enumerate(arguments_names):

            type_data = hints[name]
            has_default_value = False
            argument_type = TypeInformation.from_type(type_data)
            if i > (len(arguments_names) - arguments_values_size) -1:
                has_default_value = True
            arguments.append(Argument(name, argument_type, has_default_value))

        result = cls(fnc, fnc_name, arguments)
        return result

    @property
    def name(self) -> str:
        """Name of option"""
        return self._name

    @property
    def arguments(self) -> List[Argument]:
        """List of acceptable arguments."""
        return self._arguments

    @property
    def function(self) -> Callable:
        """Assigned function."""
        return self._function
