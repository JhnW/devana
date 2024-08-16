from dataclasses import dataclass, field
from typing import List, Type, Dict, Any
from devana.syntax_abstraction.syntax import ISyntaxElement


@dataclass
class Value:
    """The current value of the property argument with which it will be called."""
    content: Any
    """Python value."""

    @property
    def type(self) -> Type:
        """Python type of content."""
        return type(self.content)


@dataclass
class PropertySignature:
    """Invoking target property identification data."""
    name: str
    namespaces: List[str] = field(default_factory=lambda: [])
    arguments: List[Type] = field(default_factory=lambda: [])


@dataclass
class Arguments:
    """Calling arguments."""
    positional: List[Value]
    named: Dict[str, Value]


@dataclass
class Result:
    """Call frame - target function, arguments and current context"""
    property: PropertySignature
    arguments: Arguments
    target: ISyntaxElement
