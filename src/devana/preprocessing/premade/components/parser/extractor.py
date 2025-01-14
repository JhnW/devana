from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Callable
from devana.syntax_abstraction.organizers.codecontainer import CodeContainer
from devana.syntax_abstraction.organizers.sourcemodule import SourceModule
from devana.syntax_abstraction.organizers.sourcefile import SourceFile
from devana.syntax_abstraction.syntax import ISyntaxElement
from devana.syntax_abstraction.comment import Comment

@dataclass
class ExtractedFunction:
    """One line (can contain none, one or more functions) of text and parent of this line."""
    text: str
    parent: ISyntaxElement


class IExtractor(ABC):
    """Interface for extract functions strings to parser."""
    @abstractmethod
    def extract(self) -> List[ExtractedFunction]:
        """Extract from source - managed by this class - to specifics data."""


class CommentExtractor(IExtractor):
    """This function extracts function parsable data from comments in C++ source files."""
    def __init__(self, modules: List[SourceModule], file_filter: Optional[Callable[[SourceFile], bool]] = None):
        self._modules = modules
        self._file_filter = file_filter


    @classmethod
    def _dispatch(cls, container) -> List[ExtractedFunction]:
        result = []
        if hasattr(container, "associated_comment"):
            comment: Comment = getattr(container, "associated_comment")
            if comment is not None:
                for line in comment.text:
                    result.append(ExtractedFunction(line, container))
        if isinstance(container, CodeContainer):
            for element in container.content:
                result += cls._dispatch(element)
        return result

    def extract(self) -> List[ExtractedFunction]:
        result: List[ExtractedFunction] = []
        for module in self._modules:
            for file in module.files:
                if self._file_filter and not self._file_filter(file):
                    continue
                result += self._dispatch(file)
        return result
