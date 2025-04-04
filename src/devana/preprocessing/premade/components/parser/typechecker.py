import typing
from typing import Any, Optional, List, Union
from devana.preprocessing.premade.components.executor.executable import CallFrame, Signature

def is_type_valid(value, maybe_hint) -> bool:
    # check typing without parameters and tread is as Any
    hint = maybe_hint
    if isinstance(maybe_hint, tuple):
        hint = maybe_hint[1]
    if hint is Any:
        return True
    if hint is List:
        if isinstance(value, list):
            return True
        return False
    elif hint is Union:
        return True
    elif hint is Optional:
        return True
    # check basic type
    hint_origin = typing.get_origin(hint)
    if hint_origin is None: # its str, int etc
        if hint is float:
            return isinstance(value, (float, int))
        if hint is int and isinstance(value, bool):
            return False
        return isinstance(value, hint)
    else:
        args = typing.get_args(hint)
        if hint_origin is list:
            result = False
            if not isinstance(value, list):
                return False
            for v in value:
                for arg in args:
                    result = False
                    if is_type_valid(v, arg):
                        result = True
                        break
                if not result:
                    return False
            return True
        for arg in args:
            if is_type_valid(value, arg):
                return True
        return False


def is_arguments_valid(given: CallFrame.Arguments, expected: Signature.Arguments) -> bool:
    if len(given.positional) < len(expected.positional):
        return False

    unified_expected = expected.positional + list(expected.named.items())
    unified_given = given.positional + list(given.named.items())

    for i, value in enumerate(unified_given):
        if i > len(expected.positional): # its positional match
            if not is_type_valid(value, expected.positional[i]):
                return False
        else:
            if isinstance(value, tuple):
                if not value[0] in expected.named:
                    return False
                if not is_type_valid(value[1].content, expected.named[value[0]]):
                    return False
            else:
                if not is_type_valid(value.content, unified_expected[i]):
                    return False
    return True
