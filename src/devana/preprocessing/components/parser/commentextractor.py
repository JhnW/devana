from typing import Iterable, Type, List
from devana.syntax_abstraction.organizers.sourcefile import SourceFile
from devana.syntax_abstraction.organizers.codecontainer import CodeContainer
from devana.syntax_abstraction.comment import Comment
from devana.preprocessing.preprocessor import IGenerator


class CommentExtractor(IGenerator):
    """Extract text data from comments."""

    def generate(self, data: Iterable[SourceFile]) -> List[Comment]:
        result = []
        for file in data:
            result += self._parse(file)
        return result

    @classmethod
    def get_required_type(cls) -> Type[SourceFile]:
        return SourceFile

    @classmethod
    def get_produced_type(cls) -> Type[Comment]:
        return Comment

    def _parse(self, container) -> List[Comment]:
        result = []

        if isinstance(container, CodeContainer):
            for element in container.content:
                result += self._parse(element)

        elif comment := getattr(container, "associated_comment", None):
            result.append(comment)

        return result
