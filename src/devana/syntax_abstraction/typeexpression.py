from typing import List, Optional, Union
from enum import Enum, auto, IntFlag
import re
from clang import cindex
from devana.syntax_abstraction.codepiece import CodePiece
from devana.syntax_abstraction.organizers.lexicon import Lexicon
from devana.syntax_abstraction._external_source import create_external
from devana.utility.lazy import lazy_invoke, LazyNotInit
from devana.utility.fakeenum import FakeEnum
from devana.utility.traits import IBasicCreatable
from devana.utility.errors import ParserError
from devana.syntax_abstraction.syntax import ISyntaxElement


class BasicType(Enum):
    """Provides information about common types like integer of floating point. It should be implemented as Enum
    subclass."""

    class BasicTypeValue:
        """Internal value od a basic type."""

        def __init__(self, name: str, value, unsigned: bool = False):
            self._name = name
            self._value = value
            self._unsigned = unsigned

        @property
        def name(self) -> str:
            """Name of type."""
            return self._name

        @property
        def unsigned(self) -> bool:
            """It is unsigned type or not."""
            return self._unsigned

    INT = BasicTypeValue("int", auto())
    U_INT = BasicTypeValue("unsigned int", auto(), True)
    SHORT = BasicTypeValue("short", auto())
    U_SHORT = BasicTypeValue("unsigned short", auto(), True)
    CHAR = BasicTypeValue("char", auto())
    U_CHAR = BasicTypeValue("unsigned char", auto(), True)
    BOOL = BasicTypeValue("bool", auto())
    LONG = BasicTypeValue("long", auto())
    U_LONG = BasicTypeValue("unsigned long", auto(), True)
    LONG_LONG = BasicTypeValue("long long", auto(), True)
    U_LONG_LONG = BasicTypeValue("unsigned long long", auto(), True)
    FLOAT = BasicTypeValue("float", auto())
    DOUBLE = BasicTypeValue("double", auto())
    LONG_DOUBLE = BasicTypeValue("long double", auto())
    VOID = BasicTypeValue("void", auto())

    @property
    def unsigned(self) -> bool:
        return self.value.unsigned

    @property
    def name(self) -> str:  # pylint: disable=function-redefined disable=invalid-overridden-method
        return self.value.name  # pylint: disable=invalid-overridden-method

    @staticmethod
    def from_cursor(cursor: Union[cindex.Cursor, cindex.Type]):
        try:
            type_c = cursor.type
        except AttributeError:
            type_c = cursor
        result = None
        if type_c.kind == cindex.TypeKind.INT:
            result = BasicType.INT
        elif type_c.kind == cindex.TypeKind.UINT:
            result = BasicType.U_INT
        elif type_c.kind == cindex.TypeKind.SHORT:
            result = BasicType.SHORT
        elif type_c.kind == cindex.TypeKind.USHORT:
            result = BasicType.U_SHORT
        elif type_c.kind == cindex.TypeKind.CHAR_S:
            result = BasicType.CHAR
        elif type_c.kind == cindex.TypeKind.UCHAR:
            result = BasicType.U_CHAR
        elif type_c.kind == cindex.TypeKind.FLOAT:
            result = BasicType.FLOAT
        elif type_c.kind == cindex.TypeKind.DOUBLE:
            result = BasicType.DOUBLE
        elif type_c.kind == cindex.TypeKind.LONGDOUBLE:
            result = BasicType.LONG_DOUBLE
        elif type_c.kind == cindex.TypeKind.LONG:
            result = BasicType.LONG
        elif type_c.kind == cindex.TypeKind.ULONG:
            result = BasicType.U_LONG
        elif type_c.kind == cindex.TypeKind.LONGLONG:
            result = BasicType.LONG_LONG
        elif type_c.kind == cindex.TypeKind.ULONGLONG:
            result = BasicType.U_LONG_LONG
        elif type_c.kind == cindex.TypeKind.BOOL:
            result = BasicType.BOOL
        elif type_c.kind == cindex.TypeKind.VOID:
            result = BasicType.VOID
        return result


class TypeModification(metaclass=FakeEnum):
    """Possible type modifications like const or being a pointer type."""

    class ModificationKind(IntFlag):
        """Internal enum list."""
        NONE = auto()
        REFERENCE = auto()
        POINTER = auto()
        CONST = auto()
        VOLATILE = auto()
        TEMPLATE = auto()
        STATIC = auto()
        ARRAY = auto()
        RVALUE_REF = auto()
        RESTRICT = auto()
        CONSTEXPR = auto()
        CONSTINIT = auto()
        MUTABLE = auto()
        INLINE = auto()

    enum_source = ModificationKind

    def __call__(self, order):
        if self.value is TypeModification.ModificationKind.POINTER:
            return TypeModification(self.value, order)
        elif self.value is TypeModification.ModificationKind.ARRAY:
            return TypeModification(self.value, order)
        else:
            raise NotImplementedError()

    NONE = ModificationKind.NONE
    REFERENCE = ModificationKind.REFERENCE
    POINTER = ModificationKind.POINTER
    CONST = ModificationKind.CONST
    VOLATILE = ModificationKind.VOLATILE
    TEMPLATE = ModificationKind.TEMPLATE
    STATIC = ModificationKind.STATIC
    ARRAY = ModificationKind.ARRAY
    RVALUE_REF = ModificationKind.RVALUE_REF
    RESTRICT = ModificationKind.RESTRICT
    CONSTEXPR = ModificationKind.CONSTEXPR
    CONSTINIT = ModificationKind.CONSTINIT
    MUTABLE = ModificationKind.MUTABLE
    INLINE = ModificationKind.INLINE

    def __init__(self, value: Optional[int] = None, order: Optional[List[str]] = None):
        self._pointer_order = None
        self._array_order = None
        if value is not None:
            self._value = TypeModification.ModificationKind(value)
            if value & TypeModification.ModificationKind.POINTER:
                if order is None:
                    self._pointer_order = 1
                else:
                    self._pointer_order = order
            elif value & TypeModification.ModificationKind.ARRAY:
                if order is None:
                    self._array_order = [""]
                else:
                    self._array_order = order
        else:
            self._value = TypeModification.ModificationKind.NONE

    @classmethod
    def create_array(cls, order):
        return TypeModification.ARRAY(order) # noqa pylint: disable=not-callable

    @classmethod
    def create_pointer(cls, order):
        return TypeModification.POINTER(order) # noqa pylint: disable=not-callable

    @property
    def value(self) -> ModificationKind:
        return self._value

    def __and__(self, other):
        if isinstance(other, type(self)):
            result = TypeModification(self.value & other.value)
            if result.is_pointer:
                if other.pointer_order is not None:
                    if self.pointer_order is None:
                        result.pointer_order = other.pointer_order
                    else:
                        if self.pointer_order != other.pointer_order:
                            result.pointer_order = None
                else:
                    result.pointer_order = self.pointer_order
            if result.is_array:
                if other.array_order is not None:
                    if self.array_order is None:
                        result.array_order = other.array_order
                    else:
                        if self.array_order != other.array_order:
                            result.array_order = None
                else:
                    result.array_order = self.array_order
            return result
        elif isinstance(other, TypeModification.ModificationKind):
            result = TypeModification(self.value & other)
            if result.is_pointer:
                if self.is_pointer and other == TypeModification.ModificationKind.POINTER and self.pointer_order > 1:
                    result.pointer_order = None
            if result.is_array:
                if self.is_array and other == TypeModification.ModificationKind.ARRAY and self.array_order != []:
                    result.array_order = None
                return result
        raise NotImplementedError()

    def __or__(self, other):
        if isinstance(other, type(self)):
            result = TypeModification(self.value | other.value)
            if result.is_pointer:
                if other.pointer_order is not None:
                    if self.pointer_order is None:
                        result.pointer_order = other.pointer_order
                    else:
                        result.pointer_order = max(self.pointer_order, other.pointer_order)
                else:
                    result.pointer_order = self.pointer_order
            if result.is_array:
                if other.array_order is not None:
                    if self.array_order is None:
                        result.array_order = other.array_order
                    else:
                        result.array_order = other.array_order if len(self.array_order) <= len(
                            other.array_order) else self.array_order
                else:
                    result.array_order = self.array_order
            return result
        elif isinstance(other, TypeModification.ModificationKind):
            result = TypeModification(self.value | other)
            if self.is_pointer:
                result.pointer_order = self.pointer_order
            if self.array_order:
                result.array_order = self.array_order
            return result
        raise NotImplementedError()

    def __xor__(self, other):
        if isinstance(other, type(self)):
            result = TypeModification(self.value.__or__(self.value, other.value)) # noqa
            if result.is_pointer:
                if self.is_pointer:
                    result.pointer_order = self.pointer_order
                else:
                    result.pointer_order = other.pointer_order
            if result.is_array:
                if self.is_array:
                    result.array_order = self.array_order
                else:
                    result.array_order = other.array_order
            return result
        elif isinstance(other, TypeModification.ModificationKind):
            result = TypeModification(self.value.__or__(self.value, other)) # noqa
            if result.is_pointer:
                if self.is_pointer:
                    result.pointer_order = self.pointer_order
            if result.is_array:
                if self.is_array:
                    result.array_order = self.array_order
            return result
        raise NotImplementedError()

    def __eq__(self, other):
        if isinstance(other, TypeModification):
            return self.value == other.value and self.pointer_order == other.pointer_order \
                and self.array_order == other.array_order
        elif isinstance(other, TypeModification.ModificationKind):
            if self.pointer_order is not None:
                if self.pointer_order > 1:
                    return False
            if self.array_order is not None:
                if len(self.array_order) > 0:
                    return False
            return self.value == other.value
        return False

    def __invert__(self):
        result = TypeModification(~self.value)
        return result

    def __bool__(self):
        return bool(self.value)

    __ror__ = __or__
    __rand__ = __and__
    __rxor__ = __xor__

    def __str__(self):
        result = f"{str(self.value)}"
        if self.value & TypeModification.ModificationKind.POINTER:
            result += f" (Pointer order: {self.pointer_order})"
        if self.value & TypeModification.ModificationKind.ARRAY:
            result += f" (Array order: {self._array_order})"
        return result

    @property
    def pointer_order(self) -> Optional[int]:
        return self._pointer_order # noqa

    @pointer_order.setter
    def pointer_order(self, value):
        if not self.value & TypeModification.ModificationKind.POINTER:
            if value is not None:
                if value <= 0:
                    raise ValueError("Pointer order must be greater than zero.")
                self.value |= TypeModification.ModificationKind.POINTER # noqa
        if value is None:
            self.value &= ~TypeModification.ModificationKind.POINTER # noqa
        self._pointer_order = value

    @property
    def array_order(self) -> Optional[List[str]]:
        return self._array_order

    @array_order.setter
    def array_order(self, value):
        if not self.value & TypeModification.ModificationKind.ARRAY:
            if value is not None:
                self.value |= TypeModification.ModificationKind.ARRAY # noqa
        if value is None:
            self.value &= ~TypeModification.ModificationKind.ARRAY # noqa
        self._array_order = value

    @property
    def is_reference(self) -> bool:
        return bool(self.value & TypeModification.ModificationKind.REFERENCE)

    @property
    def is_pointer(self) -> bool:
        return bool(self.value & TypeModification.ModificationKind.POINTER)

    @property
    def is_const(self) -> bool:
        return bool(self.value & TypeModification.ModificationKind.CONST)

    @property
    def is_template(self) -> bool:
        return bool(self.value & TypeModification.ModificationKind.TEMPLATE)

    @property
    def is_static(self) -> bool:
        return bool(self.value & TypeModification.ModificationKind.STATIC)

    @property
    def is_array(self) -> bool:
        return bool(self.value & TypeModification.ModificationKind.ARRAY)

    @property
    def is_rvalue_ref(self) -> bool:
        return bool(self.value & TypeModification.ModificationKind.RVALUE_REF)

    @property
    def is_volatile(self) -> bool:
        return bool(self.value & TypeModification.ModificationKind.VOLATILE)

    @property
    def is_restrict(self) -> bool:
        return bool(self.value & TypeModification.ModificationKind.RESTRICT)

    @property
    def is_constexpr(self) -> bool:
        return bool(self.value & TypeModification.ModificationKind.CONSTEXPR)

    @property
    def is_constinit(self) -> bool:
        return bool(self.value & TypeModification.ModificationKind.CONSTINIT)

    @property
    def is_mutable(self) -> bool:
        return bool(self.value & TypeModification.ModificationKind.MUTABLE)

    @property
    def is_inline(self) -> bool:
        return bool(self.value & TypeModification.ModificationKind.INLINE)

    @property
    def is_no_modification(self) -> bool:
        return self.value == TypeModification.ModificationKind.NONE


class TypeExpression(IBasicCreatable, ISyntaxElement):
    """Hold information about C++ type usage in common expression, for example, function argument declaration,
    class field, function return value or part of typedef declaration."""

    def __init__(self, cursor: Optional[Union[cindex.Cursor, cindex.Type]] = None, parent: Optional = None):
        self._cursor = cursor
        self._parent = parent
        self._is_input_type = False
        if cursor is None:
            self._name = ""
            self._modification = TypeModification.NONE
            self._details = BasicType.INT
            self._text_source = None
            self._namespaces = []
            self._template_arguments = None
        else:
            self._name = LazyNotInit
            self._modification = LazyNotInit
            self._details = LazyNotInit
            self._text_source = LazyNotInit
            self._text_source = LazyNotInit
            self._namespaces = LazyNotInit
            self._template_arguments = LazyNotInit
            try:
                self._base_type_c = cursor.type
            except AttributeError:
                self._base_type_c = cursor
                self._is_input_type = True

            if not self._is_input_type:
                if self._cursor.kind == cindex.CursorKind.TYPEDEF_DECL:
                    if self._cursor.type == cindex.TypeKind.ELABORATED:
                        for children in self._cursor.get_children():
                            self._base_type_c = children.underlying_typedef_type
                    else:
                        self._base_type_c = self._cursor.underlying_typedef_type
                elif self._cursor.kind == cindex.CursorKind.TYPE_ALIAS_DECL:
                    self._base_type_c = self._cursor.type.get_canonical()
        self._lexicon = Lexicon.create(self)

    @classmethod
    def create_default(cls, parent: Optional = None) -> "TypeExpression":
        result = cls(None, parent)
        return result

    @classmethod
    def from_cursor(cls, cursor: cindex.Cursor, parent: Optional = None) -> Optional["TypeExpression"]:
        result = cls(cursor, parent)
        return result

    @property
    @lazy_invoke
    def name(self) -> str:
        """Used name of a type in the current context.

        Name of a type is exactly the same name as used in expression, with all type modifications, namespace,
        template arguments and use or not type aliases."""
        name = ""
        from devana.syntax_abstraction.functiontype import FunctionType  # pylint: disable=import-outside-toplevel
        if not isinstance(self.details, FunctionType):
            if self.modification.is_static:
                name += "static "
            if self.modification.is_inline:
                name += "inline "
            if self.modification.is_const:
                name += "const "
            elif self.modification.is_volatile:
                name += "volatile "
            elif self.modification.is_restrict:
                name += "restrict "
            elif self.modification.is_constexpr:
                name += "constexpr "
            elif self.modification.is_constinit:
                name += "constinit "
            elif self.modification.is_mutable:
                name += "mutable "

            name += self.details.name
            if self.template_arguments:
                name += "<"
                for i in range(len(self.template_arguments)):
                    name += self.template_arguments[i].name
                    if i != len(self.template_arguments) - 1:
                        name += ","
                name += ">"

            if self.modification.is_pointer:
                for i in range(self.modification.pointer_order):
                    name += r"*"
            elif self.modification.is_reference:
                name += r"&"
            elif self.modification.is_array:
                if self.modification.array_order is None:
                    name += r"[]"
                else:
                    name += "[" + "][".join(self.modification.array_order) + "]"
            elif self.modification.is_rvalue_ref:
                name += r"&&"
        else:  # for function pointers
            fnc: FunctionType = self.details
            return_name = fnc.return_type.name
            args_names = ", ".join([arg.name for arg in fnc.arguments])
            prefix = "static " if self.modification.is_static else ""
            prefix += "inline " if self.modification.is_inline else ""

            mods = ""
            if self.modification.is_const:
                mods += "const "
            elif self.modification.is_volatile:
                mods += "volatile "
            elif self.modification.is_restrict:
                mods += "restrict "
            elif self.modification.is_constexpr:
                mods += "constexpr "
            elif self.modification.is_mutable:
                mods += "mutable "

            if self.modification.is_pointer:
                for i in range(self.modification.pointer_order):
                    mods = r"*" + mods
            elif self.modification.is_reference:
                mods = r"&" + mods
            elif self.modification.is_array:
                if self.modification.array_order is None:
                    mods += r"[]"
                else:
                    mods += "[" + "][".join(self.modification.array_order) + "]"
            elif self.modification.is_rvalue_ref:
                mods = r"&&" + mods
            name = f"{prefix}{return_name} ({mods})({args_names})"
        self._name = name
        return self._name

    @property
    @lazy_invoke
    def modification(self) -> TypeModification:
        """Usages modifications."""
        self._modification = TypeModification.NONE

        if hasattr(self._cursor, "is_mutable_field"):
            if self._cursor.is_mutable_field():
                self._modification |= TypeModification.MUTABLE

        if self.text_source is not None and self.text_source.text.find("inline ") != -1:
            self._modification |= TypeModification.INLINE

        if self._cursor.kind == cindex.CursorKind.VAR_DECL:
            self._modification |= TypeModification.STATIC
            if self.text_source is not None and self.text_source.text.find("static ") == -1:
                self._modification &= ~TypeModification.STATIC
        tmp_modification = TypeModification.NONE
        type_c = self._base_type_c

        if type_c.kind in (cindex.TypeKind.CONSTANTARRAY, cindex.TypeKind.INCOMPLETEARRAY):
            if type_c.kind == cindex.TypeKind.INCOMPLETEARRAY:
                self._modification |= TypeModification.ARRAY
            else:
                order = re.findall(r"\[(.*?)\]", CodePiece(self._cursor).text) # noqa pylint: disable=not-callable
                self._modification |= TypeModification.ARRAY(order) # noqa pylint: disable=not-callable
            while True:
                type_c = type_c.get_array_element_type()
                if type_c.kind not in (cindex.TypeKind.CONSTANTARRAY, cindex.TypeKind.INCOMPLETEARRAY):
                    break

        if type_c.kind == cindex.TypeKind.LVALUEREFERENCE:
            tmp_modification |= TypeModification.REFERENCE
        if type_c.kind == cindex.TypeKind.POINTER:
            order = 0
            tmp_type = type_c
            while True:
                if tmp_type.kind != cindex.TypeKind.POINTER:
                    break
                if tmp_type.is_const_qualified() or tmp_type.is_volatile_qualified():
                    raise NotImplementedError("Pointer to modified types are not supported (e.g. int * const ptr, but "
                                              "const int *ptr is valid.")
                tmp_type = tmp_type.get_pointee()
                order += 1
            tmp_modification |= TypeModification.POINTER(order) # noqa pylint: disable=not-callable
        if type_c.kind == cindex.TypeKind.RVALUEREFERENCE:
            tmp_modification |= TypeModification.RVALUE_REF
        type_source = type_c
        if tmp_modification.is_pointer or tmp_modification.is_reference or tmp_modification.is_rvalue_ref: # noqa
            if tmp_modification.is_pointer: # noqa
                type_source = TypeExpression.cursor_parse_from_pointer(type_c)
            else:
                type_source = type_c.get_pointee()

        if isinstance(self._cursor, cindex.Cursor):
            is_constinit = list(filter(lambda token: token.spelling == "constinit", self._cursor.get_tokens()))
            if is_constinit:
                tmp_modification |= TypeModification.CONSTINIT

        if type_source.is_const_qualified():
            if self.text_source is not None and self.text_source.text.find("constexpr ") != -1:
                tmp_modification |= TypeModification.CONSTEXPR
            else:
                tmp_modification |= TypeModification.CONST

        if type_source.is_volatile_qualified():
            tmp_modification |= TypeModification.VOLATILE

        self._modification |= tmp_modification
        return self._modification # noqa

    @modification.setter
    def modification(self, value):
        self._modification = value
        self._name = LazyNotInit

    @property
    @lazy_invoke
    def namespaces(self) -> List[str]:
        """List of namespaces used in name."""
        self._namespaces = []
        if not hasattr(self._cursor, "get_children"):
            # for function return types we need to complete this list by regular expression
            # it would be nice to find another way to do it by clang tools

            # we need to prevent namespaces to catch self type name with template
            # in case like std::vector<std::vector<double>> we get std and vector<std
            if hasattr(self._cursor, "get_declaration"):
                type_name = self._cursor.get_declaration().spelling
                base_spelling = self._cursor.spelling

                # filter prefix like const in, for example const std::string
                names = re.findall(r"\s*(\S+::\S+)\s*", self._cursor.spelling)
                if names:
                    base_spelling = names[0]

                namespaces: List[str] = base_spelling.split("::")[:-1]
                for namespace in namespaces:
                    if namespace.find(f"{type_name}<") == -1:
                        self._namespaces.append(namespace)
            else:
                self._namespaces = self._cursor.spelling.split("::")[:-1]
            return self._namespaces
        for children in self._cursor.get_children():
            if children.kind == cindex.CursorKind.NAMESPACE_REF:
                self._namespaces.append(children.spelling)
            else:
                break
        self._namespaces = self._namespaces
        return self._namespaces

    @namespaces.setter
    def namespaces(self, value):
        self._namespaces = value

    @property
    @lazy_invoke
    def template_arguments(self) -> Optional[List["TypeExpression"]]:
        """Arguments list of template concretization. None if type is not template."""
        self._template_arguments = []
        type_c = self._base_type_c
        if self.modification.is_pointer or self.modification.is_reference or self.modification.is_rvalue_ref:
            if self.modification.is_pointer:
                type_c = TypeExpression.cursor_parse_from_pointer(type_c)
            else:
                type_c = type_c.get_pointee()

        match = re.match(r"^.+<.+>", type_c.spelling)
        # disable to get template patterns from typedef parent type
        if type_c.kind is cindex.TypeKind.TYPEDEF or (
                type_c.kind is cindex.TypeKind.ELABORATED and match is None):
            self._template_arguments = None
            return self._template_arguments
        for i in range(type_c.get_num_template_arguments()):
            el = type_c.get_template_argument_type(i)
            self._template_arguments.append(TypeExpression(el, self))

        if not self._template_arguments:
            self._template_arguments = None
        return self._template_arguments

    @template_arguments.setter
    def template_arguments(self, value):
        self._template_arguments = value

    @property
    def is_generic(self) -> bool:
        """Flag informed type is generic or not."""
        # pylint: disable=import-outside-toplevel
        from devana.syntax_abstraction.templateinfo import GenericTypeParameter
        return isinstance(self.details, GenericTypeParameter)

    @property
    @lazy_invoke
    def details(self) -> ISyntaxElement:
        """Object linked to all type information.

        This field linked to first type information. If TypeExpression is used by alias, details contain typedef
        information, so jump to root of typedef declaration may be needed."""
        # pylint: disable=import-outside-toplevel
        type_c = self._base_type_c
        if self.modification.is_array:
            type_c = TypeExpression.cursor_parse_from_array(type_c)
        if self.modification.is_pointer or self.modification.is_reference or self.modification.is_rvalue_ref:
            if self.modification.is_pointer:
                type_c = TypeExpression.cursor_parse_from_pointer(type_c)
            else:
                type_c = type_c.get_pointee()

        if type_c.kind == cindex.TypeKind.FUNCTIONPROTO:
            from devana.syntax_abstraction.functiontype import FunctionType
            self._details = FunctionType(type_c, self.parent)
            return self._details

        self._details = BasicType.from_cursor(type_c)

        # check template
        if self._details is None:
            from devana.syntax_abstraction.templateinfo import GenericTypeParameter
            self._details = GenericTypeParameter.from_cursor(type_c, self._cursor, self._lexicon)

        if self._details is None:
            type_c = type_c.get_declaration()
            # check internal types
            if self.parent is not None:
                if self.parent.lexicon is not None:  # check current lexicon scope
                    self._details = self.parent.lexicon.find_type(type_c)
                if self._details is None:
                    self._details = self.parent.lexicon.find_type(type_c.spelling, self.namespaces)
            # check external types
            if self._details is None:
                self._details = create_external(type_c)
            if self._details is None:
                raise ParserError("Unable to parse type.")

        return self._details

    @details.setter
    def details(self, value):
        self._details = value
        self._name = LazyNotInit

    @property
    @lazy_invoke
    def text_source(self) -> Optional[CodePiece]:
        """Source of this element."""
        if self._is_input_type:
            self._text_source = None
        else:
            self._text_source = CodePiece(self._cursor)
        return self._text_source

    @property
    def parent(self) -> ISyntaxElement:
        """Object scope of usage this data."""
        return self._parent

    @property
    def lexicon(self):
        return self._lexicon

    @lexicon.setter
    def lexicon(self, value):
        self._lexicon = value

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.modification == other.modification and self.details == other.details
        return False

    @staticmethod
    def cursor_parse_from_pointer(cursor):
        result = cursor
        while True:
            if result.kind != cindex.TypeKind.POINTER:
                return result
            result = result.get_pointee()

    @staticmethod
    def cursor_parse_from_array(cursor):
        result = cursor
        while True:
            if result.kind not in (cindex.TypeKind.CONSTANTARRAY, cindex.TypeKind.INCOMPLETEARRAY):
                return result
            result = result.get_array_element_type()

    def __repr__(self):
        return f"{type(self).__name__}:{self.name} ({super().__repr__()})"
