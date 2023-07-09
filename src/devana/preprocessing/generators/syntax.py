import typing
from enum import Enum, auto, EnumMeta
from typing import Callable, List, Optional
from dataclasses import dataclass
import re
from devana.preprocessing.sources.source import ISource


class AttributeSyntaxError(ValueError):
    """Error from attributes syntax."""


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
            raise AttributeSyntaxError(f"{type_data} is not vail type")

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

    def __init__(self, fnc: Callable, name: str, arguments: List[Argument], namespace: Optional[str] = None,
                 is_marker: bool = False):
        self._name = name
        self._arguments = arguments
        self._function = fnc
        self._namespace = namespace
        self._is_marker = is_marker

    @staticmethod
    def _is_optional(type_data: type) -> bool:
        if typing.get_origin(type_data) is typing.Union and type(None) in typing.get_args(type_data):
            return True
        return False

    @classmethod
    def from_callable(cls, fnc: Callable, namespace: Optional[str] = None, is_marker: Optional[bool] = None):
        fnc_name: str = fnc.__name__
        arguments_names = []
        if hasattr(fnc, "__code__"):
            arguments_names = fnc.__code__.co_varnames
        arguments_values_size = 0
        if hasattr(fnc, "__defaults__"):
            arguments_values_size = 0 if fnc.__defaults__ is None else len(fnc.__defaults__)
        hints = typing.get_type_hints(fnc)

        if len(arguments_names) < 1:
            raise AttributeSyntaxError("Expected minimum one argument taken by callable.")
        source_type = hints[arguments_names[0]]
        if source_type is not ISource:
            raise AttributeSyntaxError("First argument must be ISource")

        arguments_names = arguments_names[1:]
        arguments = []

        for i, name in enumerate(arguments_names):
            type_data = hints[name]
            has_default_value = False
            argument_type = TypeInformation.from_type(type_data)
            if i > (len(arguments_names) - arguments_values_size) - 1:
                has_default_value = True
            arguments.append(Argument(name, argument_type, has_default_value))

        if is_marker is None:
            if len(arguments) == 0:
                return cls(fnc, fnc_name, arguments, namespace, True)
            else:
                return cls(fnc, fnc_name, arguments, namespace, False)
        else:
            return cls(fnc, fnc_name, arguments, namespace, is_marker)

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

    @property
    def namespace(self) -> Optional[str]:
        """Namespace for function call. All function using devana:: namespace implicitly, so it is second namespace.
        Namespaces only to C++ attributes, not for comments."""
        return self._namespace

    @property
    def is_marker(self) -> bool:
        """Marker function do not have arguments expect source and its name is written capital letters.
        Addition it does not need brackets."""
        return self._is_marker


class PreprocessorAttribute:
    """Parser and invoker of the given function on the basis of test-specified attributes."""

    _implicitly_namespace: str = "devana"

    def __init__(self, signature: DataSignature):
        self._signature = signature

    def invoke(self, context: ISource, text: str, skip_namespace: bool = False) -> any:
        arguments = self._parse(text, skip_namespace)
        return self._signature.function(context, *arguments)

    def _parse(self, text: str, skip_namespace: bool = False) -> List[any]:
        namespace = ""
        if not skip_namespace:
            namespace = self._implicitly_namespace + "::"
            if self._signature.namespace:
                namespace += self._signature.namespace + "::"

        # its very simple so we can parse it manually
        pattern = namespace + self._signature.name
        if not self._signature.is_marker:
            pattern += r"\((.+)\)"
        pattern = "^" + pattern + "$"

        match = re.match(pattern, text)
        text_arguments = []
        if match and not self._signature.is_marker:
            if len(match.groups()) < 1:
                raise AttributeSyntaxError("General parsing error, its nort a function.")
            text_arguments = self._split_arguments(match.group(1))

        # pylint: disable=consider-using-generator
        mandatory_arguments_count = sum([1 for arg in self._signature.arguments if not arg.has_default])
        if mandatory_arguments_count < len(text_arguments):
            raise AttributeSyntaxError("Not enough arguments.")

        arguments = []
        # check arguments types and parse it
        for i, arg in enumerate(text_arguments):
            try:
                arguments.append(self._parse_argument(arg, self._signature.arguments[i].type))
            except Exception as e:
                raise AttributeSyntaxError(f"Unable to parsing argument of index {i} because of: {e}") from e
        return arguments

    @staticmethod
    def _split_arguments(text: str) -> List[str]:
        arguments = []
        quote_count = 0
        argument = ""
        for character in text:
            if quote_count == 1:
                argument += character
                if character == "\"":
                    arguments.append(argument)
                    argument = ""
                    quote_count = 0
            else:
                if character == ",":
                    arguments.append(argument)
                    argument = ""
                    quote_count = 0
                elif character == "\"":
                    quote_count = 1
                    argument += character
                else:
                    argument += character
        if argument:
            arguments.append(argument)
        return arguments

    @staticmethod
    def _parse_argument(argument_value: str, argument_type_signature: TypeInformation) -> any:
        argument_type = argument_type_signature.kind
        value = argument_value.strip()
        if argument_type is TypeKind.INT:
            return int(value)
        elif argument_type is TypeKind.REAL:
            return float(value)
        elif argument_type is TypeKind.BOOL:
            if value == "True":
                return True
            elif value == "False":
                return False
            else:
                raise AttributeSyntaxError(f"Expected bool (True/False), given: {argument_value}")
        elif argument_type is TypeKind.STRING:
            if len(value) < 2:
                raise AttributeSyntaxError(f"Expected string, given: {argument_value}")
            if value[0] == "\"" and value[-1] == "\"":
                return value[1:-1]
            else:
                raise AttributeSyntaxError(f"Expected string, given: {argument_value}")
        elif argument_type is TypeKind.ENUM:
            try:
                return argument_type_signature.details[argument_value]
            except Exception as e:
                raise AttributeSyntaxError(f"Wrong argument type. Expected {argument_type_signature.details}.") from e
        elif argument_type is TypeKind.OPTIONAL:
            if value == "None":
                return None
            else:
                return PreprocessorAttribute._parse_argument(value, argument_type_signature.details)
        else:
            raise AttributeSyntaxError("Unhandled argument type argument type.")
