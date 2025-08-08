from typing import List, Type, Optional, Callable

from devana.preprocessing.premade.components.executor.environment import Environment
from devana.syntax_abstraction.organizers.sourcemodule import SourceModule
from devana.syntax_abstraction.syntax import ISyntaxElement
from devana.preprocessing.preprocessor import ISource

class SyntaxElementDataProvider(ISource):
    """Scans syntax elements across provided source modules and produces a list of
    Environment.CallingData instances using custom factory functions."""

    def __init__(
            self,
            modules: List[SourceModule],
            data_factories: List[Callable[[ISyntaxElement], Optional[Environment.CallingData]]]
    ):
        self._modules = modules
        self._data_factories = data_factories

    @classmethod
    def get_produced_type(cls) -> Type:
        return Environment.CallingData

    def feed(self) -> List[Environment.CallingData]:
        result = []
        elements = (content for module in self._modules for file in module.files for content in file.content)
        for element in elements:
            for factory in self._data_factories:
                if data := factory(element):
                    assert isinstance(data, Environment.CallingData), "Data is not an instance of Environment.CallingData"
                    result.append(data)
        return result
