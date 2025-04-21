from __future__ import annotations
from typing import Optional, List
from clang import cindex

from devana.syntax_abstraction.organizers.codecontainer import CodeContainer
from devana.syntax_abstraction.typeexpression import TypeExpression
from devana.utility.traits import IBasicCreatable, ICursorValidate
from devana.syntax_abstraction.organizers.lexicon import Lexicon
from devana.syntax_abstraction.syntax import ISyntaxElement
from devana.syntax_abstraction.codepiece import CodePiece
from devana.utility.lazy import LazyNotInit, lazy_invoke
from devana.syntax_abstraction.comment import Comment
from devana.utility.init_params import init_params
from devana.utility.errors import ParserError


class ConceptInfo(IBasicCreatable, ICursorValidate, ISyntaxElement):
    """Represents a C++ concept as a full definition."""

    def __init__(self, cursor: Optional[cindex.Cursor] = None, parent: Optional[CodeContainer] = None):
        self._cursor = cursor
        self._parent = parent
        if cursor is None:
            from devana.syntax_abstraction.templateinfo import TemplateInfo # pylint: disable=import-outside-toplevel
            self._name = "DefaultConcept"
            self._body = "true"
            self._template = TemplateInfo.from_params(parameters=[
                TemplateInfo.TemplateParameter.create_default()
            ])
            self._associated_comment = None
            self._text_source = None
        else:
            if not self.is_cursor_valid(cursor):
                raise ParserError(f"It is not a valid type cursor: {cursor.kind}.")
            self._name = LazyNotInit
            self._body = LazyNotInit
            self._template = LazyNotInit
            self._associated_comment = LazyNotInit
            self._text_source = LazyNotInit
        self._lexicon = Lexicon.create(self)

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
    def from_params( # pylint: disable=unused-argument, too-many-positional-arguments
            cls,
            parent: Optional[ISyntaxElement] = None,
            name: Optional[str] = None,
            body: Optional[str] = None,
            template: Optional[ISyntaxElement] = None,
            associated_comment: Optional[Comment] = None,
            lexicon: Optional[Lexicon] = None
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
    def template(self) -> ISyntaxElement:
        """Template associated with this concept."""
        from devana.syntax_abstraction.templateinfo import TemplateInfo # pylint: disable=import-outside-toplevel
        self._template = TemplateInfo.from_cursor(self._cursor)
        return self._template

    @template.setter
    def template(self, value: ISyntaxElement) -> None:
        self._template = value

    @property
    @lazy_invoke
    def body(self) -> str:
        """The body of the concept, which defines its constraint expression."""
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
    def associated_comment(self) -> Optional[Comment]:
        parent = self.parent
        while parent is not None:
            if hasattr(parent, "bind_comment"):
                self._associated_comment = parent.bind_comment(self)
                return self._associated_comment
            parent = parent.parent
        return None

    @associated_comment.setter
    def associated_comment(self, value: Optional[Comment]) -> None:
        self._associated_comment = value

    @property
    @lazy_invoke
    def text_source(self) -> CodePiece:
        """Source of this element."""
        self._text_source = CodePiece(self._cursor)
        return self._text_source

    @property
    def lexicon(self) -> CodeContainer:
        """Current lexicon storage of an object."""
        return self._lexicon

    @lexicon.setter
    def lexicon(self, value):
        self._lexicon = value

    @property
    def parent(self):
        return self._parent

class ConceptUsage(IBasicCreatable, ICursorValidate, ISyntaxElement):
    """Represents a usage of a C++ concept."""

    def __init__(self, cursor: Optional[cindex.Cursor] = None, parent: Optional[ISyntaxElement] = None):
        self._cursor = cursor
        self._parent = parent
        if cursor is None:
            self._concept = ConceptInfo.create_default()
            self._namespaces = []
            self._parameters = []
        else:
            if not self.is_cursor_valid(cursor):
                raise ParserError(f"It is not a valid type cursor: {cursor.kind}.")
            self._concept = LazyNotInit
            self._namespaces = LazyNotInit
            self._parameters = LazyNotInit
        self._lexicon = Lexicon.create(self)

    @classmethod
    def create_default(cls, parent: Optional = None) -> "ConceptUsage":
        return cls(None, parent)

    @classmethod
    def from_cursor(cls, cursor: cindex.Cursor, parent: Optional = None) -> Optional["ConceptUsage"]:
        if cls.is_cursor_valid(cursor):
            return cls(cursor, parent)
        return None

    @classmethod
    @init_params(skip={"parent"})
    def from_params(  # pylint: disable=unused-argument
            cls,
            parent: Optional[ISyntaxElement] = None,
            concept: Optional[ConceptInfo] = None,
            namespaces: Optional[List[str]] = None,
            parameters: Optional[List[TypeExpression]] = None
    ) -> "ConceptUsage":
        return cls(None, parent)

    @staticmethod
    def is_cursor_valid(cursor: cindex.Cursor) -> bool:
        for child in cursor.get_children():
            if child.referenced and child.referenced.kind == cindex.CursorKind.CONCEPT_DECL:
                return True
        return False

    @property
    @lazy_invoke
    def concept(self) -> ConceptInfo:
        concept_cursors = list(filter(
            lambda c: c.referenced and c.referenced.kind == cindex.CursorKind.CONCEPT_DECL,
            self._cursor.get_children())
        )
        self._concept = self._lexicon.find_type(concept_cursors[0].referenced)
        if self._concept is None: # case for std and other headers outside module
            self._concept = ConceptInfo.from_cursor(concept_cursors[0].referenced)
        return self._concept

    @concept.setter
    def concept(self, value: ConceptInfo) -> None:
        self._concept = value

    @property
    @lazy_invoke
    def namespaces(self) -> List[str]:
        self._namespaces = []
        for child in self._cursor.get_children():
            if child.kind == cindex.CursorKind.NAMESPACE_REF:
                self._namespaces.append(child.spelling)
        return self._namespaces

    @namespaces.setter
    def namespaces(self, value: List[str]) -> None:
        self._namespaces = value

    @property
    @lazy_invoke
    def parameters(self) -> List[str]:
        """Retrieves the concept parameters '<...>'."""
        self._parameters = []
        for c in self._cursor.get_children():
            if c.kind == cindex.CursorKind.TYPE_REF:
                self._parameters.append(c.spelling)
        return self._parameters


        #self._parameters = []
        #return self._parameters

    @parameters.setter
    def parameters(self, value: List[str]):
        self._parameters = value

    @property
    def name(self) -> str:
        return self.concept.name

    @property
    def parent(self):
        return self._parent

    def __repr__(self):
        return f"{type(self).__name__}:{self.name} ({super().__repr__()})"
