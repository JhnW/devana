from dataclasses import dataclass, field
from enum import Enum, auto
from sys import platform
from typing import List, Optional
from devana.syntax_abstraction.attribute import AttributeDeclaration, Attribute


class LineEndings(Enum):
    """Kind of used line endings."""
    LF = auto()
    CR_LF = auto()
    CR = auto()

    LINUX = LF
    WINDOWS = CR_LF
    MAC_OS = CR

    @property
    def character(self) -> str:
        if self == self.LF:
            return "\n"
        elif self == self.CR_LF:
            return "\r\n"
        elif self == self.CR:
            return "\r"
        raise ValueError("Unknown enum value.")

    @staticmethod
    def detect():
        if platform in ("linux", "linux2"):
            return LineEndings.LINUX
        elif platform == "darwin":
            return LineEndings.MAC_OS
        elif platform == "win32":
            return LineEndings.WINDOWS
        raise EnvironmentError("Unknown system.")

    @staticmethod
    def default():
        return LineEndings.LINUX

    def print(self):
        return self.character


class IndentCharacter(Enum):
    """Indent character to configure."""
    SPACE = auto()
    TAB = auto()

    @property
    def character(self) -> str:
        if self == IndentCharacter.SPACE:
            return r" "
        elif self == IndentCharacter.TAB:
            return r"\t"
        raise NotImplementedError("Out of range enum.")

    def print(self):
        return self.character


@dataclass
class Indent:
    """Indent configuration. Value is the indent sign (space or tab) multiplier. For example value 2 mean indent
    2 spaces. Count mean how many separated indent we have, for example count 3 mean 3 * value * character."""

    character: IndentCharacter = IndentCharacter.SPACE
    value: int = 4
    count: int = 0

    def print(self):
        assert self.value > 0
        result = r""
        for _ in range(self.count):
            for _ in range(self.value):
                result += self.character.print()
        return result

    def increase(self):
        self.count += 1

    def decrease(self):
        self.count -= 1
        if self.count < 0:
            self.count = 0

    def __add__(self, other):
        if not isinstance(other, int):
            raise NotImplementedError()
        result = Indent(self.character, self.value, self.count + other)
        if result.count < 0:
            result.count = 0
        return result

    def __sub__(self, other):
        if not isinstance(other, int):
            raise NotImplementedError()
        result = Indent(self.character, self.value, self.count - other)
        if result.count < 0:
            result.count = 0
        return result

    def reset(self):
        self.count = 0


@dataclass
class AttributeFilter:
    """Filter for possible and forbidden attributes."""
    values: List[str]
    is_forbidden: bool = False


@dataclass
class AttributesCriteria:
    """More specific attribute admissibility criteria."""
    names: Optional[AttributeFilter] = field(default_factory=lambda: AttributeFilter(["noreturn",
                                                                                      "carries_dependency",
                                                                                      "deprecated",
                                                                                      "fallthrough",
                                                                                      "nodiscard",
                                                                                      "maybe_unused",
                                                                                      "likely",
                                                                                      "unlikely",
                                                                                      "no_unique_address",
                                                                                      "assume",
                                                                                      "optimize_for_synchronized"]
                                                                                     ))
    """List of allowed or forbidden attribute names."""
    namespaces: Optional[AttributeFilter] = field(default_factory=lambda: AttributeFilter(["gnu", "gsl"]))
    """List of allowed or forbidden attribute namespaces."""

    def filter(self, attributes: List[AttributeDeclaration]) -> List[AttributeDeclaration]:
        results = [attr.clone() for attr in attributes]

        def filter_using_namespaces(decl: AttributeDeclaration) -> bool:
            return ((decl.using_namespace in self.namespaces.values) ^ self.namespaces.is_forbidden) \
                | (decl.using_namespace is None)

        if self.namespaces is not None:
            results = list(filter(filter_using_namespaces, results))

            for attr in results:
                if attr.using_namespace is not None:
                    continue

                def filter_namespaces(a: Attribute) -> bool:
                    if a.namespace is None:
                        return True
                    return (a.namespace in self.namespaces.values) ^ self.namespaces.is_forbidden

                attr.attributes = list(filter(filter_namespaces, attr.attributes))

        if self.names is not None:
            for attr in results:
                if attr.using_namespace is not None:
                    continue
                attr.attributes = list(filter(
                    lambda a: ((a.name in self.names.values) ^ self.names.is_forbidden) or (a.namespace is not None),
                    attr.attributes))
        return list(filter(lambda a: len(a.attributes) > 0, results))


@dataclass
class PrinterConfiguration:
    """Data structure that stores standard code printing settings e.g. newline format."""

    line_ending: LineEndings = LineEndings.default()
    indent: Indent = field(default_factory=lambda: Indent())
    attributes: AttributesCriteria = field(default_factory=lambda: AttributesCriteria())

    def format_line(self, text: str) -> str:
        return f"{self.indent.print()}{text}{self.line_ending.print()}"
