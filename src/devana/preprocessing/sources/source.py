from abc import ABC, abstractmethod
from typing import Optional
from devana.syntax_abstraction.codepiece import CodePiece


class ISource(ABC):
    """Description of the source of the code to be transformed for the purposes of the appropriate generators."""

    @property
    @abstractmethod
    def invoker(self) -> any:
        """The source code element associated with a specific source inclusion. It can be, for example, a class when the
         source is comments describing a class or attributes, a function when an attribute referred to it,
          or even a representation of an external parsing configuration."""

    @property
    @abstractmethod
    def target(self) -> any:
        """The element in the context of which the code generation is to take place. Typically, a code element that
        will be transformed or extended within itself, but it is not required - the target can be a class when the
         generator should reasonably create an external function that makes sense for this class, for example by
          generating JSON from it."""

    @property
    @abstractmethod
    def code(self) -> Optional[CodePiece]:
        """The location and text of the source when found in the code. Especially important for macros inside
        function bodies."""
