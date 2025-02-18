from typing import Optional, List, Any
from clang import cindex

from devana.syntax_abstraction.organizers.codecontainer import CodeContainer
from devana.syntax_abstraction.typeexpression import TypeExpression
from devana.syntax_abstraction.templateinfo import TemplateInfo
from devana.syntax_abstraction.codepiece import CodePiece
from devana.syntax_abstraction.syntax import ISyntaxElement
from devana.utility.lazy import LazyNotInit, lazy_invoke
from devana.utility.init_params import init_params
from devana.utility.errors import ParserError


class ConceptInfo(CodeContainer):
    """Represents a C++ concept, either as a full definition or as a template requirement (e.g. in `template<Concept T>`)."""

    def __init__(self, cursor: Optional[cindex.Cursor] = None, parent: Optional[CodeContainer] = None):
        super().__init__(cursor, parent)
        if cursor is None:
            self._name = "DefaultConcept"
            self._body = "true"
            self._template = TemplateInfo.from_params(parameters=[
                TemplateInfo.TemplateParameter.create_default()
            ])
            self._parameters = []
        else:
            if not self.is_cursor_valid(cursor):
                raise ParserError(f"It is not a valid type cursor: {cursor.kind}.")
            self._name = LazyNotInit
            self._body = LazyNotInit
            self._template = LazyNotInit
            self._parameters = LazyNotInit

    def __repr__(self):
        return f"{type(self).__name__}:{self.name} ({super().__repr__()})"

    @classmethod
    def create_default(cls, parent: Optional = None) -> "ConceptInfo":
        return cls(None, parent)

    @classmethod
    def from_cursor(cls, cursor: cindex.Cursor, parent: Optional = None) -> Optional["ConceptInfo"]:
        if cls.is_cursor_valid(cursor):
            return cls(cursor, parent)
        return None

    @classmethod
    @init_params(skip={"parent"})
    def from_params( # pylint: disable=unused-argument
            cls,
            parent: Optional[ISyntaxElement] = None,
            content: Optional[List[Any]] = None,
            namespace: Optional[str] = None,
            name: Optional[str] = None,
            body: Optional[str] = None,
            template: Optional[TemplateInfo] = None,
            parameters: Optional[List["TypeExpression"]] = None
    ) -> "ConceptInfo":
        return cls(None, parent)

    @staticmethod
    def is_cursor_valid(cursor: cindex.Cursor) -> bool:
        return cursor.kind == cindex.CursorKind.CONCEPT_DECL

    @property
    @lazy_invoke
    def name(self) -> str:
        self._name = self._cursor.spelling
        return self._name

    @name.setter
    def name(self, value) -> None:
        self._name = value

    @property
    @lazy_invoke
    def template(self) -> TemplateInfo:
        self._template = TemplateInfo.from_cursor(self._cursor)
        return self._template

    @template.setter
    def template(self, value: TemplateInfo) -> None:
        self._template = value

    @property
    @lazy_invoke
    def body(self) -> str:
        self._body = ""
        for child in self._cursor.get_children():
            if child.kind != cindex.CursorKind.TEMPLATE_TYPE_PARAMETER:
                self._body = CodePiece(child).text
                break
        return self._body

    @body.setter
    def body(self, value: str) -> None:
        self._body = value

    @property
    @lazy_invoke
    def parameters(self) -> List["TypeExpression"]:
        """Retrieves the concept parameters '<...>'."""
        if not isinstance(self.parent, TemplateInfo.TemplateParameter):
            return []
        # Probably without a cursor from the parent it will not be possible to extract it.
        # I get a mental breakdown every time I see the number -1, when i want to extract parameters in the normal way.
        # Fuck it for now.
        return []

    @parameters.setter
    def parameters(self, value: List["TypeExpression"]) -> None:
        self._parameters = value

    @property
    def is_specifier(self) -> bool:
        """Determines whether this ConceptInfo instance is acting as a template specifier."""
        return isinstance(self.parent, TemplateInfo.TemplateParameter)

    @property
    def _content_types(self) -> List:
        return [ConceptInfo]
