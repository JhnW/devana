from dataclasses import dataclass, field
from typing import List, Type, Dict, Generic, TypeVar, Callable, Optional, Any
from abc import ABC, abstractmethod
import inspect
from devana.preprocessing.premade.components.executor.editor import IEditable


@dataclass
class Signature:
    """Invoking target identification data."""

    @dataclass
    class Arguments:
        """Description of the arguments accepted by executable."""
        positional: List[Type] = field(default_factory=list)
        """A list of types, in order of appearance of the positional arguments they take
        - those that cannot be accessed by name."""
        named: Dict[str, Type] = field(default_factory=dict)
        """A dictionary of named argument types - those that do not have a clearly defined order and the user can
        access them by name. In the current version, it is assumed that each positional argument must have
        a default value (not included in the signature)."""

    name: str
    """Name of function."""
    namespaces: List[str] = field(default_factory=list)
    """List of supported namespaces, in order from outermost. It is recommended to use at least one
    'devana' namespace (or the name of your preprocessor) to get better support for data sources
    such as c++ attributes."""
    arguments: Arguments = field(default_factory=Arguments)
    """Description of the arguments accepted by executable."""

    @classmethod
    def from_function(cls, function: Callable, name: Optional[str] = None, namespaces: Optional[List[str]] = None) -> "Signature":
        """Create a Signature from a function. Type hints for all function parameters are required."""
        function_name = function.__name__ if name is None else name
        signature = inspect.signature(function)
        positionals: List[Type] = []
        named: Dict[str, Type] = {}
        if not [a for a in signature.parameters.values() if a.name in ["context", "target"]]:
            raise ValueError("Function must have context and target argument.")
        for arg in signature.parameters.values():
            if arg.annotation is None:
                raise TypeError(f"Argument {arg} has no type annotation.")
            if arg.name in ["context", "target"]:
                continue
            if arg.default is inspect.Parameter.empty:
                positionals.append(arg.annotation)
            else:
                named[arg.name] = arg.annotation
        return Signature(function_name, [] if namespaces is None else namespaces, cls.Arguments(positionals, named))


T = TypeVar("T")
@dataclass
class CallFrame(Generic[T]):
    """Calling data."""

    class IContext(ABC):
        """A description of the current function call context. This is used to share common state between calls to
        multiple executables, for example, to allow multiple executables to work on the contents of a single file."""

        @property
        @abstractmethod
        def editors(self) -> List[IEditable]:
            """Returns list of all editors."""

        @abstractmethod
        def get_editor(self, name: str) -> IEditable:
            """Returns by name the identifier of the mutable object used as the output artifact of the executable.
            In the case of multiple executables sharing the same context (typical case), the object will be shared.
            It is allowed to throw an exception in case of non-existent editors or to create an editor. The first
            approach is recommended, leaving the creation of the contexts' content to the executable grouping class."""

        @abstractmethod
        def get_state(self, name: str) -> Any:
            """Returns by name, which is the identifier of an immutable object used as general configuration information
            for the given context. It is allowed and recommended to throw an exception when the object with the
            requested identifier does not exist."""

    @dataclass
    class Arguments:
        """Calling arguments."""

        @dataclass
        class Value:
            """The current value of the argument with which it will be called."""
            content: Any
            """Python value."""

            @property
            def type(self) -> Type:
                """Python type of content."""
                return type(self.content)

        positional: List[Value] = field(default_factory=list)
        """A list of types, in order of appearance of the positional arguments they take."""
        named: Dict[str, Value] = field(default_factory=dict)
        """A dictionary of named argument types - those that do not have a clearly defined order and the user can."""

    def __init__(self, arguments: Arguments, target: T, context: IContext):
        self._arguments = arguments
        self._target = target
        self._context = context

    @property
    def arguments(self) -> Arguments:
        return self._arguments

    @property
    def target(self) -> T:
        return self._target

    @property
    def context(self) -> IContext:
        return self._context


class Executable(Generic[T]):
    """Basic, executable fragment. The function should take all arguments listed in the signature, preserve
    names of non-positional parameters and the order of positional arguments, and take a context instance as the
    first argument."""

    @dataclass
    class TargetScope(Generic[T]):
        """Configuration of the current scope. The template specialization denotes what type the target's base type
        is in the inheritance ladder."""
        target: Optional[Type[T]] = None
        """The specific requested type supported by the scope. If none, the is more generic."""

    def __init__(self, signature: Signature, scope: TargetScope, function: Callable):
        self._signature = signature
        self._scope = scope
        self._function = function

    @property
    def signature(self) -> Signature:
        return self._signature

    @property
    def scope(self) -> TargetScope[T]:
        return self._scope



    def _validate_call_frame(self, frame: CallFrame[T]):
        possible_position_type_list = self._signature.arguments.positional.copy()
        possible_position_type_list += [v for _, v in self._signature.arguments.named.items()]

        if len(frame.arguments.positional) < len(self._signature.arguments.positional):
            raise ValueError(f"Too few positional arguments for the function. "
                             f"Expected minimum: {max(0, len(self._signature.arguments.positional))}. "
                             f"Given: {len(frame.arguments.positional)}")
        if len(frame.arguments.positional) > len(possible_position_type_list):
            raise ValueError(f"Too many positional arguments for the function. "
                             f"Expected maximum: {len(possible_position_type_list)}. "
                             f"Given: {len(frame.arguments.positional)}")

        from devana.preprocessing.premade.components.parser.typechecker import is_type_valid # pylint: disable=import-outside-toplevel
        for i, arg in enumerate(frame.arguments.positional):
            if not is_type_valid(arg.content, possible_position_type_list[i]):
                raise ValueError(f"The argument at position {i} was given the wrong type. "
                                 f"Expected: {possible_position_type_list[i]}. Received: {arg.type}.")

        signature_named_list = list(self._signature.arguments.named.items())
        positionally_passed_named_arguments_count = len(frame.arguments.positional) - len(frame.arguments.positional)
        remaining_positional_types = {}

        for i in range(len(signature_named_list) - positionally_passed_named_arguments_count):
            remaining_positional_types[signature_named_list[i][0]] = signature_named_list[i][1]

        for name, value in frame.arguments.named.items():
            if name not in remaining_positional_types:
                raise ValueError(f"Unexpected argument named: {name}.")
            if value.type != remaining_positional_types[name]:
                raise ValueError(f"Unexpected type for argument named {name}. "
                                 f"Expected: {remaining_positional_types[name]}. Given: {value.type}.")


    def call(self, frame: CallFrame[T]) -> None:
        self._validate_call_frame(frame)
        named_arguments = {}
        for name, value in frame.arguments.named.items():
            named_arguments[name] = value.content
        positional_arguments = [value.content for value in frame.arguments.positional]
        self._function(frame.context, frame.target, *positional_arguments, **named_arguments)
