from typing import List, Type, Optional, Callable

from devana.preprocessing.premade.components.executor.environment import Environment
from devana.syntax_abstraction.organizers.sourcemodule import SourceModule
from devana.syntax_abstraction.syntax import ISyntaxElement
from devana.preprocessing.preprocessor import ISource

class SyntaxElementDataProvider(ISource):
    """Scans syntax elements across provided source modules and produces a list of
    Environment.CallingData instances via a custom factory function."""

    def __init__(
            self,
            modules: List[SourceModule],
            data_factory: Callable[[ISyntaxElement], Optional[Environment.CallingData]]
    ):
        self._modules = modules
        self._data_factory = data_factory

    @classmethod
    def get_produced_type(cls) -> Type:
        return Environment.CallingData

    def feed(self) -> List[Environment.CallingData]:
        result = []
        elements = (content for module in self._modules for file in module.files for content in file.content)
        for element in elements:
            if data := self._data_factory(element):
                assert isinstance(data, Environment.CallingData), "Data is not an instance of Environment.CallingData"
                result.append(data)
        return result
