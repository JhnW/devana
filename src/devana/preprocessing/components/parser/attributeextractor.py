from typing import Iterable, Type, Optional, Union
from dataclasses import dataclass
from devana.syntax_abstraction.organizers.sourcefile import SourceFile
from devana.syntax_abstraction.syntax import ISyntaxElement
from devana.syntax_abstraction.attribute import Attribute, DescriptiveByAttributes
from devana.syntax_abstraction.organizers.codecontainer import CodeContainer
from devana.preprocessing.preprocessor import IGenerator
from devana.preprocessing.components.parser.parsingcontext import ParsingContext


class AttributeExtractor(IGenerator):
    """Extract text data from C++ attributes."""

    @dataclass
    class AttributeData:
        """Extracted attribute"""
        text: str
        """Attribute value as text."""
        using: Optional[str]
        """For C++17 using attribute-namespace syntax text before attribute in using."""
        context: ParsingContext
        """Context of parsing."""

    def generate(self, data: Iterable[SourceFile]) -> Iterable[ParsingContext]:
        for file in data:
            for element in self._parse(file):
                yield element

    @classmethod
    def get_required_type(cls) -> Type:
        return SourceFile

    @classmethod
    def get_produced_type(cls) -> Type:
        return ParsingContext

    def _parse(self, container: Union[CodeContainer, Iterable]) -> Union[ParsingContext, Iterable]:
        for content in container.content:
            if isinstance(content, DescriptiveByAttributes):
                yield self._parse_context(content)
            # if issubclass(type(content), CodeContainer):
            #     for element in self._parse(content):
            #         yield element
            # else:
            #     yield ParsingContext("Lol", None)

    def _parse_context(self, element: DescriptiveByAttributes) -> Optional[AttributeData]:
        result = element







