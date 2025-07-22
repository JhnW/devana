from typing import List, Type, Any, TypeVar
from devana.preprocessing.preprocessor import ISource
from devana.preprocessing.premade.components.executor.environment import Environment
T = TypeVar('T')


class SourceMergeCallingData(ISource):
    """Merges multiple sources into one."""
    def __init__(self, sources: List[ISource]):
        if len(sources) == 0:
            raise ValueError("No sources provided.")
        self._sources = sources

        for source in sources:
            if source.get_produced_type() != Environment.CallingData:
                raise TypeError(f"All sources must produce the same type. Expected Environment.CallingData, "
                                f"but got {source.get_produced_type()}")

    @property
    def sources(self) -> List[ISource]:
        return self._sources

    def feed(self) -> List[Any]:
        result = []
        for source in self._sources:
            result += source.feed()
        return result

    @classmethod
    def get_produced_type(cls) -> Type:
        return Environment.CallingData
