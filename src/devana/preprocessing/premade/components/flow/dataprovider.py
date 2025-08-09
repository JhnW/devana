from typing import List, Type, Optional, Callable, Iterable

from devana.preprocessing.premade.components.executor.environment import Environment
from devana.syntax_abstraction.organizers.sourcemodule import SourceModule
from devana.syntax_abstraction.organizers.codecontainer import CodeContainer
from devana.syntax_abstraction.syntax import ISyntaxElement
from devana.preprocessing.preprocessor import ISource

class SyntaxElementDataProvider(ISource):
    """
    Scans syntax elements across provided source modules and produces a list of
    Environment.CallingData instances using custom factory functions.

    If `deep_search` is True, method `feed()` will also look inside nested containers
    (e.g. namespaces, classes) to find elements. If False, it only
    checks the top-level elements that are directly inside each file.
    """

    def __init__(
            self,
            modules: List[SourceModule],
            data_factories: List[Callable[[ISyntaxElement], Optional[Environment.CallingData]]],
            deep_search: bool = True
    ):
        self._modules = modules
        self._data_factories = data_factories
        self._deep_search = deep_search

    @classmethod
    def get_produced_type(cls) -> Type:
        return Environment.CallingData

    def feed(self) -> List[Environment.CallingData]:
        def get_syntax_elements(container: CodeContainer) -> Iterable[ISyntaxElement]:
            """Yield all ISyntaxElement instances from container recursively."""
            for content in container.content:
                yield content
                if isinstance(content, CodeContainer) and self._deep_search:
                    yield from get_syntax_elements(content)

        result = []
        files = (file for module in self._modules for file in module.files)
        elements = (element for file in files for element in get_syntax_elements(file))

        for element in elements:
            # call every factory with the current element
            for factory in self._data_factories:
                if data := factory(element):
                    assert isinstance(data, Environment.CallingData), "Data is not an instance of Environment.CallingData"
                    result.append(data)
        return result
