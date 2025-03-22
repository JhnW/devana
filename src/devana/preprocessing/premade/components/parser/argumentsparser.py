import re
from abc import ABC, abstractmethod
from typing import Optional, List, Any, Union, Callable, Type
from enum import Enum


class NoValue:
    """Stub class to not-find argument token. We can't use None because None is a valid value."""
    def __new__(cls):
        return cls

class IParsable(ABC):
    """Interface for parsable token element."""
    end_pattern = r"\s*((?P<comma>,.*)|(?P<empty>\s*))$"

    @abstractmethod
    def parse(self, text: str, dispatcher: Callable[[str], List[Any]]) -> Union[List[Any], Type[NoValue]]:
        """Should get text and return parsed token as python value (except named argument - it is a dictionary).
        This method should call dispatcher argument with the rest of the text string to allow to parse
        the whole text with recursion. For example [value, *dispatcher(test_text)] is a typical return value."""


class ListArgumentParser(IParsable):
    """Implementation of a parsing list type."""

    def parse(self, text: str, dispatcher: Callable[[str], List[Any]]) -> Union[List[Any], Type[NoValue]]:
        count = 0
        ignore_mode = False
        prev = None

        for i, ch in enumerate(text):
            if ch.isspace():
                prev = ch
                continue
            if ch == '"':
                if ignore_mode:
                    if prev == r"\\":
                        prev = ch
                        continue
                ignore_mode = not ignore_mode
            if ignore_mode:
                prev = ch
                continue
            if ch == "[":
                count += 1
                prev = ch
                continue
            if ch == "]":
                count -= 1
                if count == 0:
                    pattern = self.end_pattern
                    find_rest = re.match(pattern, text[i+1:])
                    if not find_rest:
                        return NoValue()
                    rest = find_rest.groupdict()["comma"][1:] if find_rest.groupdict()["comma"] else find_rest.groupdict()["empty"]
                    value = re.match(r"\s*\[(?P<value>.*)]", text[0:i+1]).group("value")
                    return [dispatcher(value), *dispatcher(rest)]
            if count > 0:
                prev = ch
                continue
            return NoValue()
        return NoValue()



class NameArgumentParser(IParsable):
    """Implementation of parsing named argument like name=value."""

    def parse(self, text: str, dispatcher: Callable[[str], List[Any]]) -> Union[List[Any], Type[NoValue]]:
        pattern = r"((?P<label>\S+)\s*=\s*(?P<value>.+))"
        pattern = r"^\s*"+pattern+self.end_pattern
        match = re.match(pattern, text)
        if not match:
            return NoValue()
        parsed_value = dispatcher(match.groupdict()["value"])
        if parsed_value is NoValue:
            return parsed_value
        return [{match.groupdict()["label"]: parsed_value[0]}, *parsed_value[1:]]



class ArgumentGenericTypeParser(IParsable):
    """Universal type parser created based on regex and callback function or based on enum to create enum parser."""

    @classmethod
    def create_from_enum(cls, enum: Type[Enum]):
        value_map = {v.name: v for v in enum}
        pattern = "|".join([v.name for v in enum])
        pattern = r"(?P<value>"+pattern+")"
        def value_creator(v, _):
            return value_map[v]
        return cls(pattern, value_creator)

    def __init__(self, pattern: str, value_creator: Callable[[str, Callable], Any]):
        self._pattern = re.compile(r"^\s*"+pattern+self.end_pattern)
        self._value_creator = value_creator

    def parse(self, text: str, dispatcher: Callable[[str], List[Any]]) -> Union[List[Any], Type[NoValue]]:
        match = self._pattern.match(text)
        if not match:
            return NoValue()
        value = self._value_creator(match.groupdict()["value"], dispatcher)
        rest = match.groupdict()["comma"][1:] if match.groupdict()["comma"] is not None else match.groupdict()["empty"]
        return [value, *dispatcher(rest)]


class ArgumentsParser:
    """Helper class to parse function arguments (provided as text) and return list of python values."""

    def _dispatch(self, text: str) -> List[Any]:
        result = self._name_parser.parse(text, self._dispatch)
        if result is not NoValue:
            return result # noqa
        for parser in self._parsers:
            result = parser.parse(text, self._dispatch)
            if result is not NoValue:
                return result
        result = self._terminate_parser(text)
        if result is not NoValue:
            return result
        raise ValueError("Unable to parse arguments.")


    @staticmethod
    def _terminate_parser(text):
        pattern = r"^\s*$"
        result = re.match(pattern, text)
        if result is None:
            return NoValue()
        return []

    @staticmethod
    def _named_parser_creator(v: str, f: Callable):
        d = v.split("=")
        value = f(d[1:0])
        return [{d[0]: value[:1]}, value[1:]]

    def __init__(self, extra_parsers: Optional[List[IParsable]] = None):

        self._name_parser = NameArgumentParser()
        self._parsers = []
        self._parsers.append(ArgumentGenericTypeParser(r"(?P<value>[+-]?\d+)", lambda v, _: int(v)))
        self._parsers.append(ArgumentGenericTypeParser(r"(?P<value>[+-]?(?:\.\d+|\d+\.?\d*))", lambda v, _: float(v)))
        self._parsers.append(ListArgumentParser())
        self._parsers.append(ArgumentGenericTypeParser(r'(\"(?P<value>.*)\")', lambda v, _: v))
        self._parsers.append(ArgumentGenericTypeParser( r'(?P<value>true)', lambda v, _: True))
        self._parsers.append(ArgumentGenericTypeParser(r'(?P<value>false)',lambda v, _: False))
        self._parsers.append(ArgumentGenericTypeParser(r'(?P<value>None)',lambda v, _: None))
        if extra_parsers:
            self._parsers += extra_parsers


    def tokenize(self, text: str) -> List[Any]:
        return self._dispatch(text)
