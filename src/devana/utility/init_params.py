from typing import Callable, Any, Optional, Set
import functools
import inspect


def init_params(skip: Optional[Set[str]] = None) -> Callable:
    """A decorator that assigns method parameters as instance attributes.
    The attribute must have a setter or exist as an instance or class variable."""

    def decorator(_classmethod: Callable) -> Callable:

        def has_setter(cls: type, name: str) -> bool:
            """Checks if the class attribute is a property with a defined setter method."""
            try:
                maybe_property = getattr(cls, name)
            except AttributeError:
                return False
            return isinstance(maybe_property, property) and maybe_property.fset is not None

        def has_attr(instance: object, name: str) -> bool:
            """Checks if the attribute is directly in the instance or if it's a class attribute,
            excluding properties."""
            if hasattr(instance.__class__, name):
                if not isinstance(getattr(instance.__class__, name, property()), property):
                    return True
            return name in instance.__dict__

        @functools.wraps(_classmethod)
        def wrapper(*args: Any, **kwargs: Any) -> object:
            instance: object = _classmethod(*args, **kwargs)
            bound_args: inspect.BoundArguments = inspect.signature(_classmethod).bind(*args, **kwargs)
            bound_args.apply_defaults()
            ignore = skip or set()

            for name, value in bound_args.arguments.items():
                if name in ignore:
                    continue
                if not any((has_setter(instance.__class__, name), has_attr(instance, name))):
                    raise AttributeError(f"'{name}' is not a settable attribute on instance {instance}.")
                if value is not None:
                    setattr(instance, name, value)
            return instance
        return wrapper
    return decorator
