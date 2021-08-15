class FakeEnum(type):
    """Helper metaclass for provide emus with variable values in instance-level (standard enum do it in class-level).
    You must provide enum_source argument."""

    def __new__(mcs, name, bases, args):
        mcs.__enum_source__ = args["enum_source"]
        return type.__new__(mcs, name, bases, args)

    def __getattribute__(cls, item):
        enum_source = type.__getattribute__(cls, "__enum_source__")
        available_enums = [e.name for e in list(enum_source)]
        if item in available_enums:
            enum = getattr(enum_source, item)
            return cls(enum.value)
        return type.__getattribute__(cls, item)

    def __iter__(cls):
        enum_source = type.__getattribute__(cls, "__enum_source__")
        return enum_source.__iter__()
