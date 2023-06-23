from enum import Enum, auto


class GenerationMode(Enum):
    """Controls the general style of code generation."""
    GENERATE_ALL = auto()
    """Recreates all the modified source code again. It can be sensitive to parsing errors and unknown syntax elements,
     but it ensures greater consistency of output files."""
    COPY_AND_PASTE = auto()
    """It makes a copy of the already existing code, the new code is simply added to it. More secure parsing mode at the
     expense of code generation errors. Especially recommended for code that must contain preprocessor directives
     (except header guard) - although generally we are discouraged from using them in devan-transformed code"""
