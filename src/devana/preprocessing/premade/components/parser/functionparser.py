from dataclasses import dataclass, field
from typing import List, Optional, Callable, NoReturn
from enum import Enum, auto


@dataclass
class FunctionEntity:
    """Parsing function information, argument are provided as string for another parser."""
    name: str
    namespaces: List[str]
    arguments: str


class FunctionParser:
    """Class realized parsing function."""

    class StateName(Enum):
        """Name of state."""
        SEARCH = auto()
        NAMESPACE = auto()
        NAMESPACE_SEPARATOR = auto()
        FUNCTION_SEPARATOR = auto()
        ARGS = auto()
        STRING = auto()
        STRING_ESCAPE = auto()
        END = auto()
        ERROR = auto()


    @classmethod
    def _transactions_search(cls, character: Optional[str]) -> StateName:
        if character.isspace():
            return cls.StateName.SEARCH
        if character.isalpha():
            return cls.StateName.NAMESPACE
        return cls.StateName.ERROR

    @classmethod
    def _transactions_namespace(cls, character: Optional[str]) -> StateName:
        if character is None:
            return cls.StateName.END
        if character == ":":
            return cls.StateName.NAMESPACE_SEPARATOR
        if character == "(":
            return cls.StateName.ARGS
        if character.isalnum() or character == "_":
            return cls.StateName.NAMESPACE
        if character.isspace():
            return cls.StateName.FUNCTION_SEPARATOR
        if character == ",":
            return cls.StateName.FUNCTION_SEPARATOR
        return cls.StateName.ERROR

    @classmethod
    def _transactions_namespace_separator(cls, character: Optional[str]) -> StateName:
        if character == ":":
            return cls.StateName.NAMESPACE
        return cls.StateName.ERROR

    @classmethod
    def _transactions_function_separator(cls, character: Optional[str]) -> StateName:
        if character is None:
            return cls.StateName.END
        if character == ",":
            return cls.StateName.SEARCH
        if character.isspace():
            return cls.StateName.FUNCTION_SEPARATOR
        return cls.StateName.ERROR

    @classmethod
    def _transactions_args(cls, character: Optional[str]) -> StateName:
        if character is None:
            return cls.StateName.ERROR
        if character == ")":
            return cls.StateName.FUNCTION_SEPARATOR
        else:
            return cls.StateName.ARGS

    @classmethod
    def _transactions_string(cls, character: Optional[str]) -> StateName:
        if character == '"':
            return cls.StateName.ARGS
        if character == '\\':
            return cls.StateName.STRING_ESCAPE
        return cls.StateName.STRING

    @classmethod
    def _transactions_string_escape(cls, _: Optional[str]) -> StateName:
        return cls.StateName.STRING

    @classmethod
    def _transactions_error(cls, _: Optional[str]) -> StateName:
        return cls.StateName.END

    @classmethod
    def _transactions_end(cls, _: Optional[str]) -> StateName:
        return cls.StateName.END

    @dataclass
    class State:
        """State information of parser. """
        transactions: Callable[[Optional[str]], "FunctionParser.StateName"]
        on_enter: Callable[[Optional[str]], NoReturn] = field(default=lambda _: None)
        on_exit: Callable[[], NoReturn] = field(default=lambda: None)
        on_self: Callable[[Optional[str]], NoReturn] = field(default=lambda _: None)

    def _accumulate(self, character: Optional[str]):
        self._current_name_string += character

    def _add_name(self):
        self._names.append(self._current_name_string)
        self._current_name_string = ""

    def _set_arguments(self, character: Optional[str]):
        self._arguments += character

    def _add_function(self):
        if not self._names:
            return
        self._functions.append(FunctionEntity(self._names[-1], self._names[:-1], self._arguments))
        self._names = []
        self._arguments = ""
        self._current_name_string = ""


    def _on_error(self, character: Optional[str]):
        raise ValueError("Unable to parse function.")

    def __init__(self):
        self._current_name_string = ""
        self._name = ""
        self._names = []
        self._arguments = ""
        self._functions: List[FunctionEntity] = []

        self._states = {
                  self.StateName.SEARCH: self.State(self._transactions_search),
                  self.StateName.NAMESPACE: self.State(self._transactions_namespace,
                                                       on_self= self._accumulate,
                                                       on_enter=lambda ch: self._accumulate(ch) if ch.isalpha() else None,
                                                       on_exit=self._add_name),
                  self.StateName.NAMESPACE_SEPARATOR: self.State(self._transactions_namespace_separator),
                  self.StateName.FUNCTION_SEPARATOR: self.State(self._transactions_function_separator, on_exit=self._add_function),
                  self.StateName.ARGS: self.State(self._transactions_args, on_self=self._set_arguments),
                  self.StateName.STRING: self.State(self._transactions_string,
                                                    on_self=self._accumulate,
                                                    on_enter=self._accumulate,
                                                    on_exit=self._add_function),
                  self.StateName.STRING_ESCAPE: self.State(self._transactions_string_escape),
                  self.StateName.END: self.State(self._transactions_end, on_exit=self._add_function),
                  self.StateName.ERROR: self.State(self._transactions_error, on_enter=self._on_error)
                  }

    def _process_state(self, character: Optional[str], next_state: StateName, current_state: StateName):
        if next_state == current_state:
            self._states[current_state].on_self(character)
        else:
            self._states[current_state].on_exit()
            self._states[next_state].on_enter(character)

    def parse(self, text: str) -> List[FunctionEntity]:
        """Parse line to find functions."""
        self._functions = []
        self._current_name_string = ""
        self._arguments = ""
        self._names = []

        current_state = self.StateName.SEARCH
        for character in text:
            next_state = self._states[current_state].transactions(character)
            self._process_state(character, next_state, current_state)
            current_state = next_state
        next_state = self._states[current_state].transactions(None)
        self._process_state(None, next_state, current_state)
        current_state = next_state
        self._states[current_state].on_exit()
        return self._functions
