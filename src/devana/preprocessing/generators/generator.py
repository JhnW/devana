from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Optional
from devana.syntax_abstraction.codelocation import CodeLocation
from devana.preprocessing.sources.source import ISource


class IGenerator(ABC):
    """Interface for code generator."""

    @dataclass
    class Result:
        """Generation result."""
        text: str
        location: Optional[CodeLocation]

    @abstractmethod
    def generate(self, source: ISource, *args) -> Result:
        pass
