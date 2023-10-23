from typing import Iterable, Type, List
from devana.syntax_abstraction.organizers.sourcefile import SourceFile
from devana.syntax_abstraction.functioninfo import FunctionInfo
from devana.syntax_abstraction.attribute import Attribute, DescriptiveByAttributes
from devana.syntax_abstraction.organizers.codecontainer import CodeContainer
from devana.preprocessing.preprocessor import IGenerator


class AttributeExtractor(IGenerator):
    """Extract text data from C++ attributes."""

    def generate(self, data: Iterable[SourceFile]) -> List[Attribute]:
        result = []
        for file in data:
            result += self._parse(file)
        return result

    @classmethod
    def get_required_type(cls) -> Type:
        return SourceFile

    @classmethod
    def get_produced_type(cls) -> Type:
        return Attribute

    def _parse(self, container) -> List[Attribute]:
        result = []
        if isinstance(container, DescriptiveByAttributes):
            result += container.flatten_attributes
        if isinstance(container, FunctionInfo):
            for argument in container.arguments:
                result += argument.flatten_attributes
        if isinstance(container, CodeContainer):
            for content in container.content:
                result += self._parse(content)
        return result
