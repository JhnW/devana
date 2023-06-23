from sources.source import ISource
from generators.generator import IGenerator
from typing import List, Type


class Action:

    def __int__(self, name: str, allowed_sources: List[Type[ISource]], generators: List[IGenerator]):
        self._name = name
        self._allowed_sources = allowed_sources

    @property
    def name(self) -> str:
        return self._name

    @property
    def allowed_sources(self) -> List[Type[ISource]]:
        return self._allowed_sources

    def process(self, source: ISource) -> IGenerator.Result:
        pass
