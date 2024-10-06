from typing import List, Type

def register(current_register: List[Type]):
    """Registers a type in the given variable - usually a global module variable.
    Useful for automatically creating lists of default supported classes, etc."""

    def wrapper(cls: Type):
        current_register.append(cls())
        return cls
    return wrapper
