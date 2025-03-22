from typing import List, Type, Generic, TypeVar
from devana.preprocessing.preprocessor import IGenerator
from devana.preprocessing.premade.components.executor.environment import Environment, EnvironmentCreator
from devana.preprocessing.premade.components.executor.executable import Executable
from devana.preprocessing.premade.components.savers.filesaver import IDestiny


T = TypeVar("T")
class Executor(Generic[T], IGenerator):
    """An object that executes all user function commands within the processing framework in its own context."""

    def __init__(self, creator: EnvironmentCreator, executables: List[Executable[T]]):
        self._executables = executables
        self._creator = creator

    @classmethod
    def get_required_type(cls) -> Type:
        return Environment.CallingData

    @classmethod
    def get_produced_type(cls) -> Type:
        """Specifies a result type, typically as an interface."""
        return IDestiny

    def generate(self, data: List[Environment[T].CallingData[T]]) -> List[IDestiny]:
        environments = self._creator.create(data)
        result = []
        for environment in environments:
            environment.call()
            result += [editor.destiny for editor in environment.context.editors]
        return result
