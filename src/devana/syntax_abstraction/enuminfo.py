import re
from typing import Optional, List, Literal, Any
from clang import cindex
from devana.syntax_abstraction.codepiece import CodePiece
from devana.syntax_abstraction.organizers.codecontainer import CodeContainer
from devana.syntax_abstraction.comment import Comment
from devana.syntax_abstraction.typeexpression import BasicType
from devana.syntax_abstraction.organizers.lexicon import Lexicon
from devana.syntax_abstraction.attribute import DescriptiveByAttributes
from devana.utility.errors import ParserError
from devana.utility.lazy import LazyNotInit, lazy_invoke
from devana.utility.traits import IBasicCreatable, ICursorValidate
from devana.syntax_abstraction.syntax import ISyntaxElement


class EnumInfo(CodeContainer, DescriptiveByAttributes):
    """Enum declaration."""

    class EnumValue(IBasicCreatable, ICursorValidate, ISyntaxElement):
        """Enum value stored in EnumInfo."""

        def __init__(self, cursor: Optional[cindex.Cursor] = None, parent: Optional[CodeContainer] = None):
            self._cursor = cursor
            self._parent = parent
            if cursor is None:
                self._text_source = None
                self._name = "TestValue"
                self._value = 0
                self._is_default = False
                self._associated_comment = False
            else:
                self._text_source = LazyNotInit
                self._name = LazyNotInit
                self._value = LazyNotInit
                self._associated_comment = LazyNotInit
                if not self.is_cursor_valid(cursor):
                    raise ParserError("It is not a valid type cursor.")
                self._is_default = True
                for _ in cursor.get_children():
                    self._is_default = False

        @classmethod
        def create_default(cls, parent: Optional = None) -> "EnumInfo.EnumValue":
            result = cls(None, parent)
            return result

        @classmethod
        def from_cursor(cls, cursor: cindex.Cursor, parent: Optional = None) -> Optional["EnumInfo.EnumValue"]:
            if not cls.is_cursor_valid(cursor):
                return None
            return cls(cursor, parent)

        @staticmethod
        def is_cursor_valid(cursor: cindex.Cursor) -> bool:
            return cursor.kind == cindex.CursorKind.ENUM_CONSTANT_DECL

        @property
        @lazy_invoke
        def name(self) -> str:
            """Enumeration name."""
            self._name = self._cursor.displayname
            return self._name

        @name.setter
        def name(self, value):
            self._name = value

        @property
        @lazy_invoke
        def value(self) -> int:
            """Enumeration value, automatic or standard."""
            self._value = self._cursor.enum_value
            return self._value

        @value.setter
        def value(self, v):
            self._value = v

        @property
        def is_default(self) -> bool:
            """Flag inform about value is default generated."""
            return self._is_default

        @is_default.setter
        def is_default(self, value):
            self._is_default = value

        @property
        @lazy_invoke
        def text_source(self) -> Optional[CodePiece]:
            """Source of this element."""
            self._text_source = CodePiece(self._cursor)
            return self._text_source

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
        def parent(self) -> CodeContainer:
            """Structural parent element like file, namespace or class."""
            return self._parent

        def __repr__(self):
            return f"{type(self).__name__}:{self.name} ({super().__repr__()})"

    def __init__(self, cursor: Optional[cindex.Cursor] = None, parent: Optional[CodeContainer] = None):
        super().__init__(cursor, parent)

        if cursor is None:
            self._name = "TestEnum"
            self._values = []
            self._is_scoped = False
            self._prefix = None
            self._numeric_type = BasicType.INT
            self._text_source = None
            self._is_declaration = False
            self._associated_comment = None
        else:
            if not self.is_cursor_valid(cursor):
                raise ParserError("It is not a valid type cursor.")
            self._name = LazyNotInit
            self._values = LazyNotInit
            self._is_scoped = LazyNotInit
            self._prefix = LazyNotInit
            self._numeric_type = LazyNotInit
            self._text_source = LazyNotInit
            self._is_declaration = LazyNotInit
            self._associated_comment = LazyNotInit
        self._lexicon = Lexicon.create(self)

    @staticmethod
    def is_cursor_valid(cursor: cindex.Cursor) -> bool:
        return cursor.kind == cindex.CursorKind.ENUM_DECL

    @property
    @lazy_invoke
    def name(self) -> str:
        """Enum name."""
        self._name = self._cursor.spelling
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    @lazy_invoke
    def values(self) -> List[EnumValue]:
        """List of possible values of enum."""
        self._values = []
        for children in self._cursor.get_children():
            self._values.append(self.EnumValue(children, self))
        return self._values

    @values.setter
    def values(self, value):
        self._values = value

    @property
    @lazy_invoke
    def is_scoped(self) -> bool:
        """Flag that is scoped enum - enum class or enum struct"""
        self._is_scoped = self._cursor.is_scoped_enum()
        return self._is_scoped

    @is_scoped.setter
    def is_scoped(self, value):
        self._is_scoped = value
        if self.prefix is None:
            self.prefix = "class"

    @property
    @lazy_invoke
    def prefix(self) -> Optional[Literal["class", "struct"]]:
        """Scoped enum prefix, class or struct."""
        self._prefix = None
        if self.is_scoped:
            self._prefix = "class" if re.search(r"class\s+" + self.name, self.text_source.text) else "struct"
        return self._prefix

    @prefix.setter
    def prefix(self, value):
        if not self.is_scoped and value is not None:
            raise ValueError("Only scoped enum has prefix.")
        if self.is_scoped and value is None:
            raise ValueError("Scoped enum do not allow None prefix.")
        if value is None:
            self._prefix = None
        if value in ("class", "struct"):
            raise ValueError("Only None or sting class or struct are allowed.")
        self._prefix = value

    @property
    @lazy_invoke
    def numeric_type(self) -> BasicType:
        """Used numeric type."""
        self._numeric_type = BasicType.from_cursor(self._cursor.enum_type)
        assert self._numeric_type is not None
        return self._numeric_type

    @numeric_type.setter
    def numeric_type(self, value):
        self._numeric_type = value

    @property
    @lazy_invoke
    def text_source(self) -> Optional[CodePiece]:
        """Source of this element."""
        self._text_source = CodePiece(self._cursor)
        return self._text_source

    @property
    @lazy_invoke
    def is_declaration(self) -> bool:
        """Determine kind, definition or declaration."""
        self._is_declaration = True
        for token in self._cursor.get_tokens():
            if "{" == token.spelling:
                self._is_declaration = False
                break
        return self._is_declaration

    @is_declaration.setter
    def is_declaration(self, value):
        self._is_declaration = value

    @property
    def is_definition(self) -> bool:
        """Determine kind, definition or declaration."""
        return not self.is_declaration

    @is_definition.setter
    def is_definition(self, value):
        self._is_declaration = not value

    @property
    def definition(self) -> Optional[Any]:
        """Definition of enum."""
        if self.is_definition:
            return self
        return self._lexicon.find_type(self.name)

    @property
    def parent(self):
        """Structural parent element like file, namespace or class."""
        return self._parent

    @property
    def lexicon(self):
        return self._lexicon

    @lexicon.setter
    def lexicon(self, value):
        self._lexicon = value

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
    def _content_types(self) -> List:
        return [self.EnumValue]

    def __repr__(self):
        return f"{type(self).__name__}:{self.name} ({super().__repr__()})"
