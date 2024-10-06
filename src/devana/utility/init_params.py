from typing import Callable, Any, Optional, Set
from inspect import signature, BoundArguments
from functools import wraps


def init_params(skip: Optional[Set[str]] = None) -> Callable:
    """A decorator that automatically assigns classmethod parameters to instance attributes,
    if the attribute has a setter or exists as an instance variable.

    Parameters in the `skip` set will be ignored, "cls" is ignored by default.
    If parameter is not settable or doesn't exist in the instance, an AttributeError will be raised.

    Example usage::

        class Person:
            name: str = ""
            age: int = 0

            @classmethod
            @init_params()
            def create(cls, name: str, age: int):
                return cls()

        jerry = Person.create("Jerry", 20)
        print(jerry.name, jerry.age)  # Outputs: Jerry 20
    """
    def decorator(_classmethod: Callable) -> Callable:
        def has_setter(instance: object, name: str) -> bool:
            """Checks if the class attribute is a property with a defined setter."""
            try:
                maybe_property = getattr(instance.__class__, name)
            except AttributeError:
                return False
            return isinstance(maybe_property, property) and maybe_property.fset is not None

        def has_attr(instance: object, name: str) -> bool:
            """Checks if the attribute is directly in the instance or if it's a class attribute,
            excluding properties."""
            if not isinstance(getattr(instance.__class__, name, property()), property):
                return True
            return name in instance.__dict__

        @wraps(_classmethod)
        def wrapper(*args: Any, **kwargs: Any) -> object:
            instance: object = _classmethod(*args, **kwargs)
            bound_args: BoundArguments = signature(_classmethod).bind(*args, **kwargs)
            bound_args.apply_defaults()
            ignore: Set[str] = skip or set()
            ignore.add("cls")

            for name, value in bound_args.arguments.items():
                if name in ignore:
                    continue
                if not any((has_setter(instance, name), has_attr(instance, name))):
                    raise AttributeError(
                        f"'{name}' is not a settable attribute on instance {instance}."
                    )
                if value is not None:
                    setattr(instance, name, value)
            return instance
        return wrapper
    return decorator
