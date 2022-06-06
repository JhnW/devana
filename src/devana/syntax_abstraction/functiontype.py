from devana.utility.errors import ParserError
from devana.syntax_abstraction.typeexpression import TypeExpression
from devana.syntax_abstraction.organizers.lexicon import Lexicon
from devana.syntax_abstraction.organizers.codecontainer import CodeContainer
from devana.syntax_abstraction.codepiece import CodePiece
from devana.utility.lazy import LazyNotInit, lazy_invoke
from clang import cindex
from typing import Optional, List


class FunctionType:
    """Class representing the type of a function (function pointer) that can
    appear as a variable or in a typedef etc."""

    def __init__(self, cursor: Optional[cindex.Cursor] = None, parent: Optional[CodeContainer] = None):
        if cursor.kind is not cindex.TypeKind.FUNCTIONPROTO:
            raise ParserError(f"It is not a valid type cursor: {cursor.kind}.")
        self._cursor = cursor
        self._parent = parent
        if cursor is None:
            self._arguments = []
            self._return_type = TypeExpression()
            self._text_source = None
        else:
            self._arguments = LazyNotInit
            self._return_type = LazyNotInit
            self._text_source = LazyNotInit
        self._name = LazyNotInit
        self._lexicon = Lexicon.create(self)

    @property
    @lazy_invoke
    def arguments(self) -> List[TypeExpression]:
        """List of function input arguments types."""
        self._arguments = [TypeExpression(arg, self) for arg in self._cursor.argument_types()]
        return self._arguments

    @arguments.setter
    def arguments(self, value):
        self._arguments = value

    @property
    @lazy_invoke
    def return_type(self) -> TypeExpression:
        """Function return type."""
        self._return_type = TypeExpression(self._cursor.get_result(), self)
        return self._return_type

    @return_type.setter
    def return_type(self, value):
        self._return_type = value

    @property
    @lazy_invoke
    def name(self) -> str:
        return_name = self.return_type.name
        args_names = ", ".join([arg.name for arg in self.arguments])
        self._name = f"{return_name} ()({args_names})"
        return self._name

    @property
    @lazy_invoke
    def text_source(self) -> CodePiece:
        """Source of this element."""
        self._text_source = CodePiece(self._cursor)
        return self._text_source

    @property
    def parent(self) -> CodeContainer:
        """Structural parent element like file, namespace or class."""
        return self._parent

    @property
    def lexicon(self) -> Lexicon:
        """Current lexicon storage of object."""
        return self._lexicon

    @lexicon.setter
    def lexicon(self, value):
        self._lexicon = value
