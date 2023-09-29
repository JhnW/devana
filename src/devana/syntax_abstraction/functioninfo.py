from typing import Optional, Tuple, List, Any
from enum import auto, IntFlag
import re
from clang import cindex
from devana.syntax_abstraction.variable import Variable
from devana.syntax_abstraction.typeexpression import TypeExpression, BasicType
from devana.syntax_abstraction.organizers.lexicon import Lexicon
from devana.syntax_abstraction.organizers.codecontainer import CodeContainer
from devana.syntax_abstraction.comment import Comment
from devana.syntax_abstraction.codepiece import CodePiece
from devana.syntax_abstraction.templateinfo import TemplateInfo
from devana.syntax_abstraction.attribute import DescriptiveByAttributes, AttributeDeclaration
from devana.utility.lazy import LazyNotInit, lazy_invoke
from devana.utility.traits import IBasicCreatable, ICursorValidate
from devana.utility.errors import ParserError, CodeError
from devana.syntax_abstraction.syntax import ISyntaxElement


class FunctionModification(IntFlag):
    """Modification for functions and methods."""
    NONE = auto()
    CONST = auto()
    EXPLICIT = auto()
    STATIC = auto()
    VIRTUAL = auto()
    PURE_VIRTUAL = auto()
    INLINE = auto()
    FINAL = auto()
    OVERRIDE = auto()
    DELETE = auto()
    DEFAULT = auto()
    CONSTEXPR = auto()
    CONSTEVAL = auto()
    VOLATILE = auto()
    NOEXCEPT = auto()

    @property
    def is_const(self) -> bool:
        # noinspection PyTypeChecker
        return bool(self.value & self.CONST)

    @property
    def is_explicit(self) -> bool:
        # noinspection PyTypeChecker
        return self.value & self.EXPLICIT

    @property
    def is_static(self) -> bool:
        # noinspection PyTypeChecker
        return self.value & self.STATIC

    @property
    def is_virtual(self) -> bool:
        # noinspection PyTypeChecker
        return self.value & self.VIRTUAL

    @property
    def is_pure_virtual(self) -> bool:
        # noinspection PyTypeChecker
        return self.value & self.PURE_VIRTUAL

    @property
    def is_inline(self) -> bool:
        # noinspection PyTypeChecker
        return self.value & self.INLINE

    @property
    def is_final(self) -> bool:
        # noinspection PyTypeChecker
        return self.value & self.FINAL

    @property
    def is_override(self) -> bool:
        # noinspection PyTypeChecker
        return self.value & self.OVERRIDE

    @property
    def is_delete(self) -> bool:
        # noinspection PyTypeChecker
        return self.value & self.DELETE

    @property
    def is_default(self) -> bool:
        # noinspection PyTypeChecker
        return self.value & self.DEFAULT

    @property
    def is_constexpr(self) -> bool:
        # noinspection PyTypeChecker
        return self.value & self.CONSTEXPR

    @property
    def is_consteval(self) -> bool:
        # noinspection PyTypeChecker
        return self.value & self.CONSTEVAL

    @property
    def is_volatile(self) -> bool:
        # noinspection PyTypeChecker
        return self.value & self.VOLATILE

    @property
    def is_noexcept(self) -> bool:
        # noinspection PyTypeChecker
        return self.value & self.NOEXCEPT


class FunctionInfo(IBasicCreatable, ICursorValidate, DescriptiveByAttributes, ISyntaxElement):
    """Representative of function definition or declaration."""

    class Argument(Variable, ICursorValidate, DescriptiveByAttributes, ISyntaxElement):
        """Data of function or method argument."""

        def __init__(self, cursor: Optional[cindex.Cursor] = None, parent: Optional = None):
            super().__init__(cursor, parent)
            DescriptiveByAttributes.__init__(self, cursor, parent)
            if cursor is not None:
                self._attributes = LazyNotInit
                if not self.is_cursor_valid(cursor):
                    raise ParserError("It is not a valid type cursor.")
            else:
                self._attributes = []

        @staticmethod
        def is_cursor_valid(cursor: cindex.Cursor) -> bool:
            return cursor.kind == cindex.CursorKind.PARM_DECL

        @property
        @lazy_invoke
        def attributes(self) -> List[AttributeDeclaration]:
            """C++11/C23 attributes associated with the syntax."""
            self._attributes = AttributeDeclaration.create_from_element(self, self._parent.arguments)
            return self._attributes

        @attributes.setter
        def attributes(self, value: List[AttributeDeclaration]):
            self._attributes = value

    def __init__(self, cursor: Optional[cindex.Cursor] = None, parent: Optional[CodeContainer] = None):
        DescriptiveByAttributes.__init__(self, cursor, parent)
        self._cursor = cursor
        self._parent = parent
        self._prefix = ""

        if cursor is None:
            self._arguments = []
            self._name = "foo"
            self._return_type = TypeExpression.create_default(parent)
            self._return_type.details = BasicType.VOID
            self._modification = FunctionModification.NONE
            self._body = None
            self._template = None
            self._text_source = None
            self._template = None
            self._namespaces = None
            self._associated_comment = None
        else:
            if not self.is_cursor_valid(cursor):
                msg = f"It is not a valid type cursor: {cursor.kind}."
                raise ParserError(msg)
            self._arguments = LazyNotInit
            self._name = LazyNotInit
            self._return_type = LazyNotInit
            self._modification = LazyNotInit
            self._body = LazyNotInit
            self._template = LazyNotInit
            self._text_source = LazyNotInit
            self._template = LazyNotInit
            self._namespaces = LazyNotInit
            self._associated_comment = LazyNotInit
        self._lexicon = Lexicon.create(self)

    @classmethod
    def create_default(cls, parent: Optional = None) -> "FunctionInfo":
        result = cls(None, parent)
        return result

    @staticmethod
    def is_cursor_valid(cursor: cindex.Cursor) -> bool:
        return cursor.kind in (cindex.CursorKind.FUNCTION_DECL, cindex.CursorKind.FUNCTION_TEMPLATE)

    @classmethod
    def from_cursor(cls, cursor: cindex.Cursor, parent: Optional = None) -> Optional["FunctionInfo"]:
        if cls.is_cursor_valid(cursor):
            return cls(cursor, parent)
        return None

    @property
    @lazy_invoke
    def arguments(self) -> List[Argument]:
        """List of function input arguments."""
        self._arguments = []
        for children in self._cursor.get_children():
            if children.kind == cindex.CursorKind.PARM_DECL:
                self._arguments.append(self.Argument(children, self))
        return self._arguments

    @arguments.setter
    def arguments(self, value):
        self._arguments = value

    @property
    @lazy_invoke
    def name(self) -> str:
        """Name of function, without namespace."""
        self._name = self._cursor.spelling
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def complex_name(self) -> str:
        """Name of function, without namespace, with return typ name and arguments types (but no variable names)."""
        name = self.name
        if self.return_type is not None:
            name = self.return_type.name + " " + name
        name += "("
        name += ",".join(a.type.name for a in self.arguments)
        name += ")"
        return name

    @property
    @lazy_invoke
    def return_type(self) -> TypeExpression:
        """Function return type. None of class functions like constructor."""
        self._return_type = TypeExpression(self._cursor.result_type, self)
        return self._return_type

    @return_type.setter
    def return_type(self, value):
        self._return_type = value

    @property
    def overloading(self) -> Tuple:
        """List of another function overloading this name."""
        family = list(self.overloading_family)
        if family:
            args = [arg.type for arg in self.arguments]
            family = [f for f in family if args != [arg.type for arg in f.arguments]]
        return tuple(family)

    @property
    def overloading_family(self) -> Tuple:
        """List of all functions overloading this name including this one."""
        if self._lexicon is None:
            return ()

        functions: List[FunctionInfo] = self._lexicon.find_content(self.name)
        if functions is None:
            return ()

        def check_eq(a: FunctionInfo, b: FunctionInfo) -> bool:
            if [arg.type for arg in a.arguments] == [arg.type for arg in b.arguments]:
                if b.lexicon is not None:
                    a_namespaces = a.lexicon.namespaces_chain + a.namespaces
                    b_namespaces = b.lexicon.namespaces_chain + b.namespaces
                    if a_namespaces != b_namespaces:
                        return False
                if a.is_definition and b.is_definition:
                    raise CodeError("Ambiguous functions definitions.")
                if a.return_type != b.return_type:
                    raise CodeError("Ambiguous functions return arguments.")
                return True
            else:
                return False

        result = []
        duplicated_idx = []
        for i in range(len(functions)):
            for j in range(len(functions)):
                if i == j:
                    continue
                if check_eq(functions[i], functions[j]):
                    duplicated_idx.append(j)
            if i in duplicated_idx:
                continue
            if functions[i].template is not None:
                if functions[i].template.specialisation_values:
                    continue
            result.append(functions[i])

        for i in range(len(result)):
            definition = result[i].definition
            if definition is not None:
                result[i] = definition

        # remove an element from other namespaces
        base_namespace = self.lexicon.namespaces_chain + self.namespaces
        result = filter(lambda f: f.lexicon is None or f.lexicon.namespaces_chain + f.namespaces == base_namespace,
                        result)

        return tuple(result)

    @property
    @lazy_invoke
    def modification(self) -> FunctionModification:
        """Function modification enum flag."""
        self._modification = FunctionModification.NONE
        tokens = list(self._cursor.get_tokens())
        for i in range(len(tokens)):
            token = tokens[i]
            if token.spelling == "constexpr":
                self._modification |= FunctionModification.CONSTEXPR
            if token.spelling == "consteval":
                try:
                    opening_bracket_index = list(map(lambda t: t.spelling, tokens)).index("{")
                    if i < opening_bracket_index:
                        self._modification |= FunctionModification.CONSTEVAL
                except ValueError:
                    self._modification |= FunctionModification.CONSTEVAL
            elif token.spelling == "static":
                self._modification |= FunctionModification.STATIC
            elif token.spelling == "inline":
                self._modification |= FunctionModification.INLINE
            elif token.spelling == "explicit":
                self._modification |= FunctionModification.EXPLICIT
            elif token.spelling == "final":
                self._modification |= FunctionModification.FINAL
            elif token.spelling == "delete":
                self._modification |= FunctionModification.DELETE
            elif token.spelling == "override":
                self._modification |= FunctionModification.OVERRIDE
            elif token.spelling == "volatile":
                self._modification |= FunctionModification.VOLATILE
            elif token.spelling == "noexcept":
                self._modification |= FunctionModification.NOEXCEPT
        if self._cursor.is_static_method():
            self._modification |= FunctionModification.STATIC
        if self._cursor.is_const_method():
            self._modification |= FunctionModification.CONST
        if self._cursor.is_pure_virtual_method():
            self._modification |= FunctionModification.PURE_VIRTUAL
        if self._cursor.is_virtual_method():
            self._modification |= FunctionModification.VIRTUAL
        if self._cursor.is_default_method():
            self._modification |= FunctionModification.DEFAULT
        return self._modification

    @modification.setter
    def modification(self, value):
        self._modification = value

    @property
    @lazy_invoke
    def body(self) -> Optional[str]:
        """Body of function - source code. None if it is a declaration."""
        self._body = None
        for children in self._cursor.get_children():
            if children.kind == cindex.CursorKind.COMPOUND_STMT:
                self._body = CodePiece(children).text
                break
        return self._body

    @body.setter
    def body(self, value):
        self._body = value

    @property
    def is_declaration(self) -> bool:
        """Determine function kind, definition or declaration."""
        return self.body is None

    @property
    def is_definition(self) -> bool:
        """Determine function kind, definition or declaration."""
        return not self.is_declaration

    @property
    def definition(self) -> Any:
        """Definition of function."""
        if self.lexicon is None:
            return None
        cursor = self._cursor.get_definition()
        if cursor is None:
            return None
        return self.lexicon.find_cursor(cursor)

    @property
    @lazy_invoke
    def namespaces(self) -> List[str]:
        """Explicitly declared namespaces.
        For example: double namespace1::namespace2::functionName()."""
        self._namespaces = []
        text_without_function_name = CodePiece(self._cursor).text
        text = text_without_function_name[:text_without_function_name.find(f"{self._cursor.spelling}(")]
        if text[-1].isspace():
            return self._namespaces
        namespace_tokens = text.split()[-1].split("::")
        namespace_tokens = list(filter(lambda element: element, namespace_tokens))
        self._namespaces = namespace_tokens
        return self._namespaces

    @namespaces.setter
    def namespaces(self, value):
        self._namespaces = value

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
        """Current lexicon storage of an object."""
        return self._lexicon

    @lexicon.setter
    def lexicon(self, value):
        self._lexicon = value

    @property
    @lazy_invoke
    def template(self) -> Optional[TemplateInfo]:
        """Template information if declaration is template."""
        if self._cursor.kind == cindex.CursorKind.FUNCTION_TEMPLATE \
                or re.search(self.name + r"<.*>", self._cursor.displayname):
            self._template = TemplateInfo(self._cursor, self)
        elif re.compile(r"template\s*<\s*>").search(self.text_source.text):
            self._template = TemplateInfo(parent=self)
        else:
            self._template = None
        return self._template

    @template.setter
    def template(self, value):
        self._template = value

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
    def associated_comment(self, value):
        self._associated_comment = value

    @property
    def prefix(self) -> str:
        """The text that precedes the function. Only applicable for code generation, allowing
        you to inject compiler attributes e.g. dllexport."""
        return self._prefix

    @prefix.setter
    def prefix(self, value: str):
        self._prefix = value

    def __repr__(self):
        return f"{type(self).__name__}:{self.name} ({super().__repr__()})"
