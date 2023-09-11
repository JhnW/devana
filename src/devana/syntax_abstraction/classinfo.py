from enum import Enum, auto
import re
from typing import Optional, List, Tuple, cast, Any
from clang import cindex
from devana.syntax_abstraction.functioninfo import FunctionInfo
from devana.syntax_abstraction.organizers.codecontainer import CodeContainer
from devana.syntax_abstraction.codepiece import CodePiece
from devana.syntax_abstraction.variable import Variable
from devana.syntax_abstraction.organizers.lexicon import Lexicon
from devana.syntax_abstraction.templateinfo import TemplateInfo
from devana.syntax_abstraction.typeexpression import TypeExpression
from devana.syntax_abstraction.comment import Comment
from devana.syntax_abstraction.attribute import DescriptiveByAttributes
from devana.syntax_abstraction._external_source import create_external
from devana.utility.lazy import LazyNotInit, lazy_invoke
from devana.utility.traits import IBasicCreatable, ICursorValidate, IFromCursorCreatable
from devana.configuration import Configuration, ParsingErrorPolicy
from devana.utility.errors import ParserError
from devana.syntax_abstraction.syntax import ISyntaxElement


class AccessSpecifier(Enum):
    """C++ class access specifier to members."""
    PUBLIC = "public"
    PRIVATE = "private"
    PROTECTED = "protected"

    @staticmethod
    def from_cursor(cursor: cindex.Cursor):
        if cursor.access_specifier == cindex.AccessSpecifier.PUBLIC:
            return AccessSpecifier.PUBLIC
        elif cursor.access_specifier == cindex.AccessSpecifier.PRIVATE:
            return AccessSpecifier.PRIVATE
        elif cursor.access_specifier == cindex.AccessSpecifier.PROTECTED:
            return AccessSpecifier.PROTECTED
        else:
            raise ParserError("Cursor is not class/struct component.")


class ClassMember(IBasicCreatable, ISyntaxElement):
    """Base class for all class members."""

    def __init__(self, cursor: Optional[cindex.Cursor] = None):
        if cursor is None:
            self._access_specifier = AccessSpecifier.PUBLIC
        else:
            self._access_specifier = AccessSpecifier.from_cursor(cursor)

    @classmethod
    def create_default(cls, _: Optional = None) -> "ClassMember":
        result = cls(None)
        return result

    @classmethod
    def from_cursor(cls, cursor: cindex.Cursor, _: Optional = None) -> Optional["ClassMember"]:
        result = cls(cursor)
        return result

    @property
    def access_specifier(self) -> AccessSpecifier:
        """Access scope of member."""
        return self._access_specifier

    @access_specifier.setter
    def access_specifier(self, value):
        self._access_specifier = value


class MethodType(Enum):
    """Information about a type of described method."""
    STANDARD = auto()
    OPERATOR = auto()
    CONSTRUCTOR = auto()
    COPY_CONSTRUCTOR = auto()
    MOVE_CONSTRUCTOR = auto()
    COPY_ASSIGNMENT = auto()
    MOVE_ASSIGNMENT = auto()
    DESTRUCTOR = auto()

    @property
    def is_standard(self) -> bool:
        return self == MethodType.STANDARD

    @property
    def is_operator(self) -> bool:
        return self == MethodType.OPERATOR

    @property
    def is_constructor(self) -> bool:
        return self == MethodType.CONSTRUCTOR

    @property
    def is_copy_constructor(self) -> bool:
        return self == MethodType.COPY_CONSTRUCTOR

    @property
    def is_move_constructor(self) -> bool:
        return self == MethodType.MOVE_CONSTRUCTOR

    @property
    def is_copy_assignment(self) -> bool:
        return self == MethodType.COPY_ASSIGNMENT

    @property
    def is_move_assignment(self) -> bool:
        return self == MethodType.MOVE_ASSIGNMENT

    @property
    def is_destructor(self) -> bool:
        return self == MethodType.DESTRUCTOR

    @staticmethod
    def check_assignment(name: str) -> bool:
        if name == "operator=":
            return True
        return False

    @staticmethod
    def check_operator(name: str) -> bool:
        op_names = [
            "operator()",
            "operator[]",
            "operator->",
            "operator==",
            "operator!=",
            "operator>=",
            "operator<=",
            "operator<",
            "operator>",
            "operator+",
            "operator-",
            "operator*",
            "operator/",
            "operator&&",
            "operator||",
            "operator%",
            "operator&",
            "operator|",
            "operator^",
            "operator<<",
            "operator>>",
            "operator+=",
            "operator-=",
            "operator/=",
            "operator*=",
            "operator%=",
            "operator&=",
            "operator|=",
            "operator^=",
            "operator>>=",
            "operator<<=",
            "operator++",
            "operator++",
            "operator--",
            "operator--",
            "operator bool",
            "operator!",
            "operator~",
            "operator*",
            "operator&",
            "operator->",
            "operator,",
            "operator new",
            "operator delete",
            "operator new[]",
            "operator delete[]"
        ]
        if name in op_names:
            return True
        return False


class MethodInfo(FunctionInfo, ClassMember):
    """Information abut class member function - methods."""

    def __init__(self, cursor: Optional[cindex.Cursor] = None, parent: Optional[CodeContainer] = None):
        FunctionInfo.__init__(self, cursor, parent)
        ClassMember.__init__(self, cursor)
        if cursor is None:
            self._type = MethodType.STANDARD
        else:
            self._type = LazyNotInit

    @property
    @lazy_invoke
    def type(self) -> MethodType:
        """Type kind of function method."""
        self._type = MethodType.STANDARD
        if MethodType.check_operator(self.name):
            self._type = MethodType.OPERATOR
        elif MethodType.check_assignment(self.name):
            self._type = MethodType.COPY_ASSIGNMENT
            if any(a.type.modification.is_rvalue_ref for a in self.arguments):
                self._type = MethodType.MOVE_ASSIGNMENT
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @staticmethod
    def is_cursor_valid(cursor: cindex.Cursor) -> bool:
        return cursor.kind in (cindex.CursorKind.CXX_METHOD, cindex.CursorKind.FUNCTION_TEMPLATE,
                               cindex.CursorKind.CONVERSION_FUNCTION)

    @property
    @lazy_invoke
    def template(self) -> Optional[TemplateInfo]:
        """Template information if declaration is template."""
        if self._cursor.kind == cindex.CursorKind.FUNCTION_TEMPLATE:
            self._template = TemplateInfo(self._cursor, parent=self)
        elif re.compile(r"template\s*<\s*>").search(self.text_source.text):
            if self._cursor.kind == cindex.CursorKind.CXX_METHOD and not isinstance(self.parent, ClassInfo):
                self._template = TemplateInfo(self._cursor, parent=self)
            else:
                self._template = TemplateInfo(parent=self)
        else:
            self._template = None
        return self._template

    @template.setter
    def template(self, value):
        self._template = value


class ConstructorInfo(MethodInfo):
    """Constructor method information."""

    class InitializerInfo:
        """Information about one of initializer lists."""

        def __init__(self, name, value):
            self._name: str = name
            self._value: str = value

        @property
        def name(self) -> str:
            """Name of an initialized element."""
            return self._name

        @name.setter
        def name(self, value):
            self._name = value

        @property
        def value(self) -> str:
            """Value of initialization."""
            return self._value

        @value.setter
        def value(self, v):
            self._value = v

    def __init__(self, cursor: Optional[cindex.Cursor] = None, parent: Optional[CodeContainer] = None):
        super().__init__(cursor, parent)
        if cursor is None:
            self._initializer_list = []
            self._name = ""
        else:
            self._initializer_list = LazyNotInit
            self._name = LazyNotInit

    @property
    @lazy_invoke
    def initializer_list(self) -> List[InitializerInfo]:
        """Initializer list paired with constructor."""
        self._initializer_list = []
        it = self._cursor.get_children()
        c = next(it, None)
        if c is not None:
            try:
                while True:
                    if c.kind in (cindex.CursorKind.MEMBER_REF, cindex.CursorKind.TYPE_REF):
                        name = c.spelling
                        name = name.replace("class ", "").replace("struct ", "")
                        c = next(it)
                        if c.kind == cindex.CursorKind.MEMBER_REF:
                            continue
                        text = CodePiece(c).text
                        if c.kind in (cindex.CursorKind.UNEXPOSED_EXPR, cindex.CursorKind.CALL_EXPR):
                            if c.kind == cindex.CursorKind.CALL_EXPR:
                                pattern = re.compile(
                                    name + r"\((.*)\)")  # parse args for function like Base(5)or Base()
                                value = pattern.match(text)[1]
                            else:
                                pattern = re.compile(name + r"\(\)")  # find empty init like Base()
                                if pattern.match(text):
                                    value = ""
                                else:
                                    value = text
                        else:
                            value = text
                        data = self.InitializerInfo(name, value)
                        self._initializer_list.append(data)
                        c = next(it)
                    else:
                        c = next(it)
            except StopIteration:
                pass
        return self._initializer_list

    @initializer_list.setter
    def initializer_list(self, value):
        self._initializer_list = value

    @property
    @lazy_invoke
    def type(self) -> MethodType:
        """Type kind of function method."""
        self._type = MethodType.CONSTRUCTOR
        if self._cursor.is_copy_constructor():
            self._type = MethodType.COPY_CONSTRUCTOR
        elif self._cursor.is_move_constructor():
            self._type = MethodType.MOVE_CONSTRUCTOR
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    @lazy_invoke
    def name(self) -> str:
        self._name = re.sub(r"(.*)(<.+>)", r"\g<1>", super().name)
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @staticmethod
    def is_cursor_valid(cursor: cindex.Cursor) -> bool:
        return cursor.kind == cindex.CursorKind.CONSTRUCTOR

    @property
    def return_type(self) -> None:
        return None

    @return_type.setter
    def return_type(self, value):
        raise ValueError("Constructor do not have return value.")


class DestructorInfo(MethodInfo):
    """Destructor information."""

    def __init__(self, cursor: Optional[cindex.Cursor] = None, parent: Optional[CodeContainer] = None):
        super().__init__(cursor, parent)
        if cursor is None:
            self._name = ""
        else:
            self._name = LazyNotInit

    @property
    @lazy_invoke
    def name(self) -> str:
        self._name = re.sub(r"(.*)(<.+>)", r"\g<1>", super().name)
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def return_type(self) -> None:
        return None

    @return_type.setter
    def return_type(self, value):
        raise ValueError("Destructor do not have return value.")

    @property
    def type(self) -> MethodType:
        return MethodType.DESTRUCTOR

    @staticmethod
    def is_cursor_valid(cursor: cindex.Cursor) -> bool:
        return cursor.kind == cindex.CursorKind.DESTRUCTOR


class FieldInfo(Variable, ClassMember, ICursorValidate, DescriptiveByAttributes):
    """Field of class/struct."""

    def __init__(self, cursor: Optional[cindex.Cursor] = None, parent: Optional[CodeContainer] = None):
        Variable.__init__(self, cursor, parent)
        ClassMember.__init__(self, cursor)
        DescriptiveByAttributes.__init__(self, cursor, parent)
        if cursor is not None:
            if not self.is_cursor_valid(cursor):
                raise ParserError("Bad cursor kind.")
        if cursor is None:
            self._associated_comment = None
        else:
            self._associated_comment = LazyNotInit

    @staticmethod
    def is_cursor_valid(cursor: cindex.Cursor) -> bool:
        return cursor.kind in (cindex.CursorKind.FIELD_DECL, cindex.CursorKind.VAR_DECL)

    @classmethod
    def create_default(cls, parent: Optional = None) -> "FieldInfo":
        return cls(None, parent)

    @classmethod
    def from_cursor(cls, cursor: cindex.Cursor, parent: Optional = None) -> Optional["FieldInfo"]:
        if cls.is_cursor_valid(cursor):
            return cls(cursor, parent)
        return None

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


class SectionInfo(IBasicCreatable, ICursorValidate, ISyntaxElement):
    """Representation of class sections like private, public and protected."""

    def __init__(self, cursor: Optional[cindex.Cursor] = None, parent: Optional[CodeContainer] = None):
        if parent is None:
            raise ValueError()
        self._cursor = cursor
        self._parent = parent
        if parent is None:
            self._content = []
        else:
            self._content = None
        if cursor is None:
            self._type = AccessSpecifier.PUBLIC
            self._is_unnamed = True
        else:
            self._type = LazyNotInit
            self._text_source = LazyNotInit
            self._is_unnamed = LazyNotInit
            if self._cursor is not None:
                if not self.is_cursor_valid(cursor):
                    raise ParserError("Expected CursorKind.CXX_ACCESS_SPEC_DECL.")

    @classmethod
    def create_default(cls, parent: Optional = None) -> "SectionInfo":
        result = cls(None, parent)
        result.is_unnamed = False
        return result

    @classmethod
    def from_cursor(cls, cursor: cindex.Cursor, parent: Optional = None) -> Optional["SectionInfo"]:
        if not cls.is_cursor_valid(cursor):
            return None
        return cls(cursor, parent)

    @staticmethod
    def is_cursor_valid(cursor: cindex.Cursor) -> bool:
        return cursor.kind == cindex.CursorKind.CXX_ACCESS_SPEC_DECL

    @property
    @lazy_invoke
    def type(self) -> AccessSpecifier:
        """Section type, for example public."""
        if self._cursor is None:
            self._type = AccessSpecifier.PUBLIC
            return self._type
        if self._cursor.access_specifier == cindex.AccessSpecifier.PUBLIC:
            self._type = AccessSpecifier.PUBLIC
        elif self._cursor.access_specifier == cindex.AccessSpecifier.PRIVATE:
            self._type = AccessSpecifier.PRIVATE
        elif self._cursor.access_specifier == cindex.AccessSpecifier.PROTECTED:
            self._type = AccessSpecifier.PROTECTED
        else:
            raise ParserError("Invalid access specifier")
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    @lazy_invoke
    def is_unnamed(self) -> bool:
        """Return a flag about section source if code line or standard access in class body."""
        self._is_unnamed = self._cursor is None
        return self._is_unnamed

    @is_unnamed.setter
    def is_unnamed(self, value):
        self._is_unnamed = value

    @property
    @lazy_invoke
    def text_source(self) -> Optional[CodePiece]:
        """Source of this element."""
        self._text_source = CodePiece(self._cursor)
        return self._text_source

    @property
    def parent(self) -> CodeContainer:
        """Structural parent element like file, namespace or class."""
        return self._parent

    @property
    def content(self) -> List[Any]:
        if self._content is not None:
            return self._content
        content = []
        start = False
        for c in self.parent.content:
            if start:
                if isinstance(c, SectionInfo):
                    break
                content.append(c)
            else:
                if c is self:
                    start = True
        return content

    @content.setter
    def content(self, value):
        self._content = value

    def __repr__(self):
        return f"{type(self).__name__}:{self.type} ({super().__repr__()})"


class InheritanceInfo(IFromCursorCreatable, ISyntaxElement):
    """Information about class/structure inheritance."""

    class InheritanceValue(IBasicCreatable, ISyntaxElement):
        """One of parent (in C++ mean) information."""

        def __init__(self, cursor: Optional[cindex.Cursor] = None, parent: Optional = None):
            self._cursor = cursor
            self._parent = parent
            if cursor is None:
                self._access_specifier = AccessSpecifier.PUBLIC
                self._is_virtual = False
                self._type = None
                self._template_arguments = []
                self._namespaces = []
            else:
                self._access_specifier = LazyNotInit
                self._is_virtual = LazyNotInit
                self._type = LazyNotInit
                self._template_arguments = LazyNotInit
                self._namespaces = LazyNotInit

        @classmethod
        def create_default(cls, parent: Optional = None) -> "InheritanceInfo.InheritanceValue":
            return cls(None, parent)

        @classmethod
        def from_cursor(cls, cursor: cindex.Cursor, parent: Optional = None) -> Optional[("InheritanceInfo"
                                                                                          ".InheritanceValue")]:
            return cls(cursor, parent)

        @property
        def parent(self) -> CodeContainer:
            """Class parent."""
            return self._parent

        @parent.setter
        def parent(self, value):
            self._parent = value

        @property
        @lazy_invoke
        def access_specifier(self) -> AccessSpecifier:
            """Inheritance mode like public."""
            self._access_specifier = AccessSpecifier.from_cursor(self._cursor)
            return self._access_specifier

        @access_specifier.setter
        def access_specifier(self, value):
            self._access_specifier = value

        @property
        @lazy_invoke
        def type(self) -> Optional:
            """Type of inheritance provided by lexicon."""
            if self.parent is None:
                return None
            if self.parent.lexicon is None:
                return None
            result = self.parent.lexicon.find_type(self._cursor.get_definition())
            if result is None: # create an external type like std lib
                result = create_external(self._cursor.get_definition())
            if result is None:
                name: str = self._cursor.spelling
                if name.startswith("class "):
                    name = name[len("class "):]
                elif name.startswith("struct "):
                    name = name[len("struct "):]
                namespaces_and_type = name.split("::")
                name = namespaces_and_type[-1]
                namespaces = namespaces_and_type[:-1]
                result = self.parent.lexicon.find_type(name, namespaces)
            return result

        @type.setter
        def type(self, value):
            self._type = value

        @property
        @lazy_invoke
        def is_virtual(self) -> bool:
            """Defines is virtual inheritance"""
            self._is_virtual = False
            text = CodePiece(self._cursor).text
            if " virtual " in text or "virtual " in text:
                self._is_virtual = True
            return self._is_virtual

        @is_virtual.setter
        def is_virtual(self, value):
            self._is_virtual = value

        @property
        @lazy_invoke
        def template_arguments(self) -> List[TypeExpression]:
            self._template_arguments = []
            if self._cursor.type.get_num_template_arguments() != -1:
                for i in range(self._cursor.type.get_num_template_arguments()):
                    self._template_arguments.append(TypeExpression(self._cursor.type.get_template_argument_type(i),
                                                                   self.parent))
            return self._template_arguments

        @template_arguments.setter
        def template_arguments(self, value):
            self._template_arguments = value

        @property
        @lazy_invoke
        def namespaces(self) -> List[str]:
            """Provide information about used namespaces in parent type."""
            self._namespaces = []
            type_name: str = self._cursor.get_definition().spelling
            namespaces: List[str] = self._cursor.spelling.split("::")[:-1]
            for namespace in namespaces:
                if namespace.find(f"{type_name}<") == -1:
                    self._namespaces.append(namespace)
            return self._namespaces

        @namespaces.setter
        def namespaces(self, value: List[str]):
            self._namespaces = value

    def __init__(self, cursor: Optional[cindex.Cursor] = None, parent: Optional = None):
        self._cursor = cursor
        self._parent = parent
        self._lexicon = Lexicon.create(self)
        if cursor is None:
            self._type_parents = []
        else:
            self._type_parents = LazyNotInit

    @classmethod
    def from_cursor(cls, cursor: cindex.Cursor, parent: Optional = None) -> Optional["InheritanceInfo"]:
        return cls(cursor, parent)

    @property
    @lazy_invoke
    def type_parents(self) -> List[InheritanceValue]:
        """List of parents in code meaning."""
        parents = []
        for children in self._cursor.get_children():
            if children.kind == cindex.CursorKind.CXX_BASE_SPECIFIER:
                parents.append(self.InheritanceValue(children, self))
        self._type_parents = parents
        return self._type_parents

    @type_parents.setter
    def type_parents(self, value):
        self._type_parents = value

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value

    @property
    def lexicon(self):
        return self._lexicon


class ClassInfo(CodeContainer, DescriptiveByAttributes):
    """Data of a class type."""

    def __init__(self, cursor: Optional[cindex.Cursor] = None, parent: Optional[CodeContainer] = None):
        super().__init__(cursor, parent)
        DescriptiveByAttributes.__init__(self, cursor, parent)
        self._prefix = ""
        if cursor is None:
            self._name = "TestClass"
            self._text_source = None
            self._is_final = False
            self._template = None
            self._is_class = False
            self._inheritance = None
            self._is_declaration = False
            self._namespaces = []
            self._associated_comment = None
        else:
            self._name = LazyNotInit
            self._text_source = LazyNotInit
            self._is_final = LazyNotInit
            self._template = LazyNotInit
            self._is_class = False
            self._inheritance = LazyNotInit
            self._is_declaration = LazyNotInit
            self._namespaces = LazyNotInit
            self._associated_comment = LazyNotInit
            if cursor.kind == cindex.CursorKind.STRUCT_DECL:
                self._is_class = False
            elif cursor.kind == cindex.CursorKind.CLASS_DECL:
                self._is_class = True
            elif cursor.kind in (cindex.CursorKind.CLASS_TEMPLATE,
                                 cindex.CursorKind.CLASS_TEMPLATE_PARTIAL_SPECIALIZATION):
                # we need handle clang internal _LIBCPP_TEMPLATE_VIS macro
                if re.search(rf"class\s+(_LIBCPP_TEMPLATE_VIS)?\s*{self.name}", self.text_source.text):
                    self._is_class = True
                elif re.search(rf"struct\s+(_LIBCPP_TEMPLATE_VIS)?\s*{self.name}", self.text_source.text):
                    self._is_class = False
                else:
                    raise ParserError("It is not a valid type cursor.")
            else:
                raise ParserError("It is not a valid type cursor.")

            if self.is_definition:  # prevent for class definition like class A::B::C {}
                #  its overcomplicated because semantic parent contains standard namespaces, not only A::B
                # and children will contain namespace reference if template parameter is written with namespace,
                # so we need to make intersection both list
                semantic_parents = []
                parent = self._cursor.semantic_parent
                while True:
                    if parent is None:
                        break
                    if len(semantic_parents) >= 1:
                        if semantic_parents[-1] == parent:
                            break
                    semantic_parents.append(parent)
                    parent = parent.semantic_parent
                semantic_parents = semantic_parents[:-1]  # remove last element - file path
                semantic_parents = [p.spelling for p in semantic_parents]
                namespaces_parents = [n.spelling for n in self._cursor.get_children()
                                      if n.kind == cindex.CursorKind.NAMESPACE_REF]
                namespaces = list(set(semantic_parents) & set(namespaces_parents))

                if namespaces:
                    raise NotImplementedError("Class definition with namespaces is not allowed.")

        self._lexicon = Lexicon.create(self)

    @classmethod
    def create_default(cls, parent: Optional = None) -> "ClassInfo":
        return cls(None, parent)

    @classmethod
    def from_cursor(cls, cursor: cindex.Cursor, parent: Optional = None) -> Optional["ClassInfo"]:
        if not cls.is_cursor_valid(cursor):
            return None
        try:
            return cls(cursor, parent)
        except ParserError:
            return None

    @staticmethod
    def is_cursor_valid(cursor: cindex.Cursor) -> bool:
        if cursor.kind == cindex.CursorKind.STRUCT_DECL:
            return True
        elif cursor.kind == cindex.CursorKind.CLASS_DECL:
            return True
        elif cursor.kind in (cindex.CursorKind.CLASS_TEMPLATE,
                             cindex.CursorKind.CLASS_TEMPLATE_PARTIAL_SPECIALIZATION):
            return True
        else:
            return False

    @property
    def constructors(self) -> Tuple[ConstructorInfo]:
        """Constructors associated with class."""
        return cast(Tuple[ConstructorInfo], tuple(filter(lambda e: isinstance(e, ConstructorInfo), self.content)))

    @property
    def destructor(self) -> Optional[DestructorInfo]:
        """Destructor associated with class."""
        destructor = list(filter(lambda e: isinstance(e, DestructorInfo), self.content))
        if len(destructor) == 0:
            return None
        return destructor[0]

    @property
    def operators(self) -> Tuple[MethodInfo]:
        """Operators of class."""
        return cast(Tuple[MethodInfo], tuple(filter(lambda e: e.type.is_operator, self.methods)))

    @property
    def fields(self) -> Tuple[FieldInfo]:
        """Class fields."""
        return cast(Tuple[FieldInfo], tuple(filter(lambda e: isinstance(e, FieldInfo), self.content)))

    @property
    def methods(self) -> Tuple[MethodInfo]:
        return cast(Tuple[MethodInfo], tuple(filter(lambda e: isinstance(e, MethodInfo), self.content)))

    @property
    def private(self) -> Tuple[ISyntaxElement]:
        private = []
        for s in self.sections:
            if s.type == AccessSpecifier.PRIVATE:
                private.extend(s.content)
        return tuple(private)

    @property
    def public(self) -> Tuple[ISyntaxElement]:
        public = []
        for s in self.sections:
            if s.type == AccessSpecifier.PUBLIC:
                public.extend(s.content)
        return tuple(public)

    @property
    def protected(self) -> Tuple[ISyntaxElement]:
        protected = []
        for s in self.sections:
            if s.type == AccessSpecifier.PROTECTED:
                protected.extend(s.content)
        return tuple(protected)

    @property
    def is_class(self) -> bool:
        """Flag abut is class."""
        return self._is_class

    @is_class.setter
    def is_class(self, value):
        self._is_class = value

    @property
    def is_struct(self) -> bool:
        """Flag abut is struct."""
        return not self.is_class

    @is_struct.setter
    def is_struct(self, value):
        self._is_class = not value

    @property
    @lazy_invoke
    def is_final(self) -> bool:
        """Flag about final key-world in class."""
        self._is_final = False
        for c in self._cursor.get_children():
            if c.kind == cindex.CursorKind.CXX_FINAL_ATTR:
                self._is_final = True
        return self._is_final

    @is_final.setter
    def is_final(self, value):
        self._is_final = value

    @property
    def sections(self) -> Tuple[SectionInfo]:
        """List of sections present in an object."""
        sections = []
        if len(self.content) == 0:
            return cast(Tuple[SectionInfo], ())

        section = None
        if not isinstance(self.content[0], SectionInfo):
            section = SectionInfo(parent=self)
            section.content = []
            if self.is_class:
                section.type = AccessSpecifier.PRIVATE
            else:
                section.type = AccessSpecifier.PUBLIC
            sections.append(section)

        for content in self.content:
            if isinstance(content, SectionInfo):
                section = None
                sections.append(content)
            else:
                if section is not None:
                    section.content.append(content)
        return cast(Tuple[SectionInfo], tuple(sections))

    @property
    @lazy_invoke
    def name(self) -> str:
        """Name of class."""
        self._name = self._cursor.spelling
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    @lazy_invoke
    def inheritance(self) -> Optional[InheritanceInfo]:
        """Inheritance, if any."""
        self._inheritance = InheritanceInfo(self._cursor, self)
        if len(self._inheritance.type_parents) == 0:
            self._inheritance = None
        return self._inheritance

    @inheritance.setter
    def inheritance(self, value):
        self._inheritance = value

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
    def definition(self) -> Any:
        """Definition of class."""
        if self.is_definition:
            return self
        if self._cursor is None:
            return self._lexicon.find_type(self.name)
        return self._lexicon.find_type(self._cursor)

    @property
    @lazy_invoke
    def namespaces(self) -> List[str]:
        """Explicitly declared namespaces.
        For example: class namespace1::namespace2::ClassName; or class namespace1::ClassName {};"""
        if self.is_definition:
            return []
        self._namespaces = [n.spelling for n in self._cursor.get_children()
                            if n.kind == cindex.CursorKind.NAMESPACE_REF]
        return self._namespaces

    @namespaces.setter
    def namespaces(self, value):
        self._namespaces = value

    @property
    def lexicon(self) -> Lexicon:
        return self._lexicon

    @lexicon.setter
    def lexicon(self, value):
        self._lexicon = value

    @property
    @lazy_invoke
    def text_source(self) -> Optional[CodePiece]:
        """Source of this element."""
        self._text_source = CodePiece(self._cursor)
        return self._text_source

    @property
    @lazy_invoke
    def template(self) -> Optional[TemplateInfo]:
        """Template information if declaration is template."""
        if self._cursor.kind == cindex.CursorKind.CLASS_TEMPLATE \
                or self._cursor.kind == cindex.CursorKind.CLASS_TEMPLATE_PARTIAL_SPECIALIZATION \
                or re.search(self.name + r"<.*>", self._cursor.displayname):
            self._template = TemplateInfo(self._cursor, self)
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

    @property
    def _content_types(self) -> List:
        # pylint: disable=import-outside-toplevel
        from devana.syntax_abstraction.unioninfo import UnionInfo
        from devana.syntax_abstraction.enuminfo import EnumInfo
        from devana.syntax_abstraction.using import Using
        types = [SectionInfo, ClassInfo, FieldInfo, ConstructorInfo, DestructorInfo, MethodInfo, EnumInfo, UnionInfo,
                 Using]
        return types

    def _create_content(self) -> List[Any]:
        types = self._content_types
        content = []
        config = Configuration.get_configuration(self)
        is_abort_on_error = config.parsing.error_strategy == ParsingErrorPolicy.ABORT
        is_ignore_on_error = config.parsing.error_strategy == ParsingErrorPolicy.IGNORE
        for children in self._cursor.get_children():
            if children.kind in (cindex.CursorKind.CXX_FINAL_ATTR,
                                 cindex.CursorKind.TEMPLATE_TYPE_PARAMETER,
                                 cindex.CursorKind.CXX_BASE_SPECIFIER,
                                 cindex.CursorKind.NAMESPACE_REF,
                                 cindex.CursorKind.TYPE_REF):
                continue  # to avoid parsing keywords in class declaration - final and templates params
            element: Optional = None
            for t in types:
                try:
                    element = t.from_cursor(children, self)
                    if element is None:
                        continue
                    break
                except ParserError:
                    if is_ignore_on_error:
                        continue
                    if is_abort_on_error:
                        raise
                    config.logger.warning(f"Parser error during create content of {self} in type {t} "
                                          f"for cursor {children.spelling}.")
                    continue
            if element is None:
                if is_ignore_on_error:
                    continue
                if is_abort_on_error:
                    raise ParserError(f"Cannot match any type for content of {self} n cursor {children.spelling}.")
                config.logger.warning('Cannot match any type for content of %s n cursor %s.',
                                      self, children.spelling)
                continue
            content.append(element)
        return content

    def __repr__(self):
        return f"{type(self).__name__}:{self.name} ({super().__repr__()})"
