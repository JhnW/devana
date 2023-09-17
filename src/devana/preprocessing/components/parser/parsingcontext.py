from dataclasses import dataclass
from typing import Optional
from devana.syntax_abstraction.syntax import ISyntaxElement
from devana.syntax_abstraction.codepiece import CodePiece


@dataclass
class ParsingContext:
    """Context of parsed description."""
    target: ISyntaxElement
    """The source code element associated with a specific source inclusion. It can be, for example, a class when the
     source is comments describing a class or attributes, a function when an attribute referred to it,
      or even a representation of an external parsing configuration."""
    code: Optional[CodePiece]
    """The location and text of the source when found in the code. Especially important for macros inside
    function bodies."""
