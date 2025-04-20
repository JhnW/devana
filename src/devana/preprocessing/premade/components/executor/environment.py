from dataclasses import dataclass
from typing import List, Generic, TypeVar, Callable, Any, Dict, Type, Optional
from devana.preprocessing.premade.components.executor.executable import Executable, CallFrame, Signature
from devana.preprocessing.premade.components.executor.editor import IEditable


T = TypeVar("T")
class Environment(Generic[T]):
    """An environment is a set of multiple Executables into one group that share the same context during execution.
    It is used to group calls to allow working on a common output."""

    class Context(CallFrame.IContext):
        """Internal implementation of IContext."""

        def __init__(self, editors: Dict[str, IEditable], states: Dict[str, Any]):
            self._editors = editors
            self._states = states

        @property
        def editors(self) -> List[IEditable]:
            return [v for _, v in self._editors.items()]

        def get_editor(self, name: str) -> IEditable:
            if not name in self._editors:
                raise ValueError(f"No editor for {name}.")
            return self._editors[name]

        def get_state(self, name: str) -> Any:
            if not name in self._states:
                raise ValueError(f"No state for {name}.")
            return self._states[name]

    @dataclass
    class CallingData(Generic[T]):
        """Data for a single Executable call based on which the CallFrame will be created."""
        arguments: CallFrame[T].Arguments
        target: T
        signature: Signature

    def __init__(self, executables: List[Executable[T]], context: CallFrame[T].IContext, calling_data: List[CallingData[T]]):
        self._executables = executables
        self._context: CallFrame.IContext = context
        self._calling_data = calling_data

    @property
    def context(self) -> CallFrame.IContext:
        return self._context

    @staticmethod
    def _compare_signatures(base: Signature, given:Signature)  -> bool:
        if base.name != given.name:
            return False
        if base.namespaces != given.namespaces:
            return False
        if base.arguments.positional != given.arguments.positional:
            return False
        for a_name, a_value in base.arguments.named.items():
            if isinstance(a_value, CallFrame.IContext):
                continue
            if a_name == "target":
                continue
            is_find = False
            for b_name, b_value in given.arguments.named.items():
                if b_name == a_name and a_value == b_value:
                    is_find = True
                    break
            if not is_find:
                return False
        return True

    def call(self):

        def measure_inheritance_distance(t: Optional[Type], goal: Type) -> int:
            if t is None:
                return 0
            if t is goal:
                return 0
            bases = t.__bases__
            base = [b for b in bases if issubclass(b, goal)]
            if len(base) > 1:
                raise RuntimeError(f"Multiple bases found for {t}. Multiple base targets are not supported.")
            if len(base) == 0:
                raise RuntimeError(f"No base found for {t}.")
            base = base[0]
            if base is goal:
                return 0
            return 1 + measure_inheritance_distance(base, goal)

        for data in self._calling_data:
            if "context" in data.arguments.named:
                raise RuntimeError("Context named argument is not allowed.")
            matches = [e for e in self._executables if self._compare_signatures(e.signature, data.signature)]

            # now we need to find executable for specific target
            matches = [m for m in matches if m.scope.target is None or issubclass(m.scope.target, type(data.target))]
            if not matches:
                raise RuntimeError(f"No executable found for {data} call.")

            # now we have a list of all possible executables that meet the target requirements,
            # so now we need to find the executable which is closest to the target call data.
            # for this purpose, unfortunately, we need to build an inheritance tree
            distances = [measure_inheritance_distance(m.scope.target, type(data.target)) for m in matches]
            min_value = min(distances)
            min_indexes = [i for i, d in enumerate(distances) if d == min_value]
            matches = [matches[i] for i in min_indexes]

            if len(matches) > 1:
                raise RuntimeError(f"Multiple executable found for {data} call.")
            executable = matches[0]
            call_frame = CallFrame(data.arguments,data.target, self._context)
            executable.call(call_frame)


class EnvironmentCreator(Generic[T]):
    """Helper class to take care an environment creation process."""

    def __init__(self, creator: Callable[[List[Environment.CallingData]], List[Environment]]):
        self._creator = creator

    def create(self, data: List[Environment[T].CallingData[T]]) -> List[Environment[T]]:
        return self._creator(data)
