from dataclasses import dataclass, field
from enum import Enum, auto
from sys import platform


class LineEndings(Enum):
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
        if platform == "linux" or platform == "linux2":
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
    2 spaces. Count mean how many separated indent we have, for example count count 3 mean 3 * value * character."""

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

    def __add__(self, other):
        if not type(other) is int:
            raise NotImplementedError()
        result = Indent(count=self.count + other)
        if result.count <= 0:
            result.count = 1
        return result

    def __sub__(self, other):
        if not type(other) is int:
            raise NotImplementedError()
        result = Indent(count=self.count - other)
        if result.count < 0:
            result.count = 0
        return result

    def reset(self):
        self.count = 0


@dataclass
class PrinterConfiguration:
    """Data structure that stores standard code printing settings e.g. newline format."""

    line_ending: LineEndings = LineEndings.default()
    indent: Indent = field(default_factory=lambda: Indent())

    def format_line(self, text: str) -> str:
        return f"{self.indent.print()}{text}{self.line_ending.print()}"
