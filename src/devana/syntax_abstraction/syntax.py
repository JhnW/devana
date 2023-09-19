from abc import ABC


class ISyntaxElement(ABC):
    """Empty interface for C++ elements other than types to clarify what actually return devan functions that can return
    any element - to avoid the Any type."""
