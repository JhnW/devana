class CodeError(ValueError):
    """Expressions in the code as C/C++ standard."""


class ParserError(CodeError):
    """Parsing error, most commonly due to backend errors or the use of unsupported syntax."""
