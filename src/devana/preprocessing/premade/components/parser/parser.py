from typing import List, Dict, Type
import typing
from enum import Enum
from devana.preprocessing.premade.components.parser.extractor import IExtractor
from devana.preprocessing.premade.components.parser.argumentsparser import (ArgumentsParser, IParsable,
                                                                            ArgumentGenericTypeParser)
from devana.preprocessing.premade.components.parser.functionparser import FunctionParser
from devana.preprocessing.premade.components.parser.typechecker import is_arguments_valid
from devana.preprocessing.premade.components.executor.executable import CallFrame, Signature
from devana.preprocessing.preprocessor import ISource
from devana.syntax_abstraction.syntax import ISyntaxElement
from devana.preprocessing.premade.components.executor.environment import Environment


class Parser(ISource):
    """Parser of preprocessor functions given as string. Extractor must provide string of function, or example,
    from source code."""

    def __init__(self, extractor: IExtractor, signatures: List[Signature]):
        self._extractor = extractor
        self._signatures = signatures

        enum_types: List[IParsable] = []
        for signature in signatures:
            for arg in signature.arguments.positional:
                enum_types += self._find_enum(arg)
            for value in signature.arguments.named.values():
                enum_types += self._find_enum(value)

        self._arguments_parser = ArgumentsParser([ArgumentGenericTypeParser.create_from_enum(e) for e in enum_types])

    @classmethod
    def _find_enum(cls, hint) -> List[Type[Enum]]:
        try:
            if issubclass(hint, Enum):
                return [hint]
        except TypeError:
            pass
        hint_origin = typing.get_origin(hint)
        if hint_origin is None:
            return []
        args = typing.get_args(hint)
        result = []
        for arg in args:
            result += cls._find_enum(arg)
        return result

    @classmethod
    def get_produced_type(cls) -> Type:
        return Environment.CallingData


    def feed(self) -> List[Environment.CallingData[ISyntaxElement]]:
        result = []
        text_datas = self._extractor.extract()
        for data in text_datas:
            function_parsr = FunctionParser()
            functions = function_parsr.parse(data.text)
            for function in functions:
                arguments = self._arguments_parser.tokenize(function.arguments)
                positional_arguments: List[CallFrame.Arguments.Value] = []
                named_arguments: Dict[str, CallFrame.Arguments.Value] = {}

                # we need to search named arguments and unnamed to create the right arguments entry
                for argument in arguments:
                    if isinstance(argument, dict):
                        if len(argument.keys()) != 0:
                            raise ValueError("Internal error. Argument parser provide too many keys in dictionary.")
                        key = list(argument.keys())[0]
                        if not isinstance(key, str):
                            raise ValueError("Internal error. Argument parser provide wrong dictionary key type.")
                        named_arguments[key] = CallFrame.Arguments.Value(argument[key])
                    else:
                        positional_arguments.append(CallFrame.Arguments.Value(argument))

                # now find match signature
                match_signatures: List[Signature] = [signature for signature in self._signatures
                                    if signature.name == function.name and signature.namespaces == function.namespaces]
                if len(match_signatures) > 1:
                    raise ValueError(f"Duplicated signatures found for function: "
                                       f"{function.namespaces}::{function.name}")
                if len(match_signatures) == 0:
                    raise ValueError(f"Cannot find signature for function: {function.namespaces}::{function.name}")

                arguments_fame = CallFrame.Arguments(positional_arguments, named_arguments)
                if not is_arguments_valid(arguments_fame, match_signatures[0].arguments):
                    raise ValueError(f"Cannot match arguments for signature: {function.namespaces}::{function.name}")
                call_frame = Environment.CallingData(arguments_fame, data.parent, match_signatures[0])
                result.append(call_frame)
        return result
