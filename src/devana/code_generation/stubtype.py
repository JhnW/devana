class StubType:
    """This class serves to create outside type representation without sourcing this to lexicon as right type or
    parse source file. StubType is just free string.

    Good example are std types ile std::string or size_t. Parsing stdlib is definitely what you don't want to do, so you
    are able to write this type as raw string for code generation. StubType is fast and easy way to stub type. For more
    complex features ypu should think about create yur own ClassInfo etc."""

    def __init__(self, name: str):
        self._name = name

    @property
    def name(self):
        return self._name
