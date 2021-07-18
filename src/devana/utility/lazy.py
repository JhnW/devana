import functools


class LazyNotInit:
    """Value used by lazy_invoke to determine property are initialized or not. Set this type to value of property
    in init function to inform that value must be initialized. For example: self._name = LazyNotInit"""
    def __new__(cls, *args, **kwargs):
        return cls


def lazy_invoke(func):
    name = f"_{func.__name__}"

    @functools.wraps(func)
    def wrapper(self):
        if hasattr(self, name):
            atr = getattr(self, name)
            if atr is not LazyNotInit:
                return atr
        return func(self)

    return wrapper
