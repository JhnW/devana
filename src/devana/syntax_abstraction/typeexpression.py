from clang import cindex
from typing import List, Optional, Union
from enum import Enum, auto, IntFlag
from copy import copy
from devana.syntax_abstraction.codepiece import CodePiece
from devana.utility.lazy import lazy_invoke, LazyNotInit
from devana.syntax_abstraction.organizers.lexicon import Lexicon


class BasicType(Enum):
    """Provides information about common types like integer of floating point. It should be implemented as Enum
    subclass."""

    class BasicTypeValue:

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
    def name(self) -> str:
        return self.value.name

    @property
    def unknown(self) -> bool:
        return self.value.unknown

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


class TypeModification(IntFlag):
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

    def __init__(self, _):
        super().__init__()
        self._pointer_order = None

    def __call__(self, pointer_order: int):
        result = copy(self)
        result._pointer_order = pointer_order
        return result

    @property
    def pointer_order(self) -> Optional[int]:
        if not hasattr(self, "_pointer_order"):
            self._pointer_order = None
        if self._pointer_order is None:
            if self.value & TypeModification.POINTER.value:
                self._pointer_order = 1
        return self._pointer_order

    @pointer_order.setter
    def pointer_order(self, value):
        self._pointer_order = value

    def __and__(self, other):
        result = super().__and__(other)
        if not hasattr(self, "pointer_order") or not hasattr(other, "pointer_order"):
            return result
        if self.pointer_order is not None and other.pointer_order is not None:
            if self.pointer_order != other.pointer_order:
                result.value = 0
        return result

    def __or__(self, other):
        result = super().__or__(other)
        if not hasattr(self, "pointer_order") or not hasattr(other, "pointer_order"):
            return result
        if self.pointer_order is not None and other.pointer_order is not None:
            if self.pointer_order != other.pointer_order:
                result.value = 0
        if self.pointer_order is not None:
            result.pointer_order = self.pointer_order
        elif other.pointer_order is not None:
            result.pointer_order = other.pointer_order
        return result

    def __xor__(self, other):
        result = super().__xor__(other)
        if not hasattr(self, "pointer_order") or not hasattr(other, "pointer_order"):
            return result
        if self.pointer_order is not None and other.pointer_order is not None:
            if self.pointer_order != other.pointer_order:
                result.value = 0
        if self.pointer_order is not None:
            result.pointer_order = self.pointer_order
        elif other.pointer_order is not None:
            result.pointer_order = other.pointer_order
        return result

    __ror__ = __or__
    __rand__ = __and__
    __rxor__ = __xor__

    def __eq__(self, other):
        result = super().__eq__(other)
        if not hasattr(self, "pointer_order") or not hasattr(other, "pointer_order"):
            return result
        if self.pointer_order is not None and other.pointer_order is not None:
            if self.pointer_order != other.pointer_order:
                return False
        return result

    @property
    def is_reference(self) -> bool:
        return self.value & TypeModification.REFERENCE

    @property
    def is_pointer(self) -> bool:
        return self.value & TypeModification.POINTER

    @property
    def is_const(self) -> bool:
        return self.value & TypeModification.CONST

    @property
    def is_template(self) -> bool:
        return self.value & TypeModification.TEMPLATE

    @property
    def is_static(self) -> bool:
        return self.value & TypeModification.STATIC

    @property
    def is_array(self) -> bool:
        return self.value & TypeModification.ARRAY

    @property
    def is_rvalue_ref(self) -> bool:
        return self.value & TypeModification.RVALUE_REF

    @property
    def is_volatile(self) -> bool:
        return self.value & TypeModification.VOLATILE

    @property
    def is_restrict(self) -> bool:
        return self.value & TypeModification.RESTRICT

    @property
    def is_constexpr(self) -> bool:
        return self.value & TypeModification.CONSTEXPR

    @property
    def is_no_modification(self) -> bool:
        return self.value == TypeModification.NONE


class TypeExpression:
    """Hold information about C++ type usage in common expression, for example function argument declaration,
    class field, function return value or part of typedef declaration."""

    def __init__(self, cursor: Optional[Union[cindex.Cursor, cindex.Type]] = None, parent: Optional = None):
        self._cursor = cursor
        self._parent = parent
        self._is_input_type = False
        if cursor is None:
            self._name = ""
            self._modification = TypeModification.NONE
            self._details = None
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
        self._lexicon = Lexicon.create(self)

    @property
    @lazy_invoke
    def name(self) -> str:
        """Used name of type in current context.

        Name of type is exactly the same name as used in expression, with all type modifications, namespace,
        template arguments and use or not type aliases."""

        name = ""
        if self.modification.is_static:
            name += "static "
        if self.modification.is_const:
            name += "const "
        elif self.modification.is_volatile:
            name += "volatile "
        elif self.modification.is_restrict:
            name += "restrict "
        elif self.modification.is_constexpr:
            name += "constexpr "

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
            name += r"[]"
        elif self.modification.is_rvalue_ref:
            name += r"&&"
        self._name = name
        return self._name

    @property
    @lazy_invoke
    def modification(self) -> TypeModification:
        """Usages modifications."""
        self._modification = TypeModification.NONE
        if self._cursor.kind == cindex.CursorKind.VAR_DECL:
            self._modification |= TypeModification.STATIC
            if self.text_source is not None and self.text_source.text.find("static ") == -1:
                self._modification &= ~TypeModification.STATIC
        tmp_modification = TypeModification.NONE
        type_c = self._base_type_c

        if type_c.kind == cindex.TypeKind.CONSTANTARRAY or type_c.kind == cindex.TypeKind.INCOMPLETEARRAY:
            raise NotImplementedError("Static arrays are not allowed.")

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
            tmp_modification |= TypeModification.POINTER(order)
        if type_c.kind == cindex.TypeKind.RVALUEREFERENCE:
            tmp_modification |= TypeModification.RVALUE_REF
        type_source = type_c
        if tmp_modification.is_pointer or tmp_modification.is_reference or tmp_modification.is_rvalue_ref:
            if tmp_modification.is_pointer:
                type_source = TypeExpression.cursor_parse_from_pointer(type_c)
            else:
                type_source = type_c.get_pointee()
        if type_source.is_const_qualified():
            if self.text_source is not None and self.text_source.text.find("constexpr ") != -1:
                tmp_modification |= TypeModification.CONSTEXPR
            else:
                tmp_modification |= TypeModification.CONST
        if type_source.is_volatile_qualified():
            tmp_modification |= TypeModification.VOLATILE

        self._modification |= tmp_modification
        return self._modification

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
            return self._namespaces
        for children in self._cursor.get_children():
            if children.kind == cindex.CursorKind.NAMESPACE_REF:
                self._namespaces.append(children.spelling)
        self._namespaces = self._namespaces
        return self._namespaces

    @namespaces.setter
    def namespaces(self, value):
        self._namespaces = value

    @property
    @lazy_invoke
    def template_arguments(self) -> Optional[List]:
        """Arguments list of template concretization. None if  type is not template."""
        self._template_arguments = []
        type_c = self._base_type_c
        if self.modification.is_pointer or self.modification.is_reference or self.modification.is_rvalue_ref:
            if self.modification.is_pointer:
                type_c = TypeExpression.cursor_parse_from_pointer(type_c)
            else:
                type_c = type_c.get_pointee()
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
        from devana.syntax_abstraction.templateinfo import GenericTypeParameter
        return type(self.details) is GenericTypeParameter

    @property
    @lazy_invoke
    def details(self) -> any:
        """Object linked to all type information.

        This field linked to first type information. If TypeExpression is used by alias, details contain typedef
        information, so jump to root of typedef declaration may be needed."""
        type_c = self._base_type_c
        if self.modification.is_pointer or self.modification.is_reference or self.modification.is_rvalue_ref:
            if self.modification.is_pointer:
                type_c = TypeExpression.cursor_parse_from_pointer(type_c)
            else:
                type_c = type_c.get_pointee()

        if type_c.kind == cindex.TypeKind.FUNCTIONPROTO:
            raise NotImplementedError("Function pointers are not supported yet.")

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
                    self._details = self.parent.lexicon.find_type(type_c.spelling)
                if self._details is None:
                    self._details = self.parent.lexicon.find_type(type_c)
            # check external types
            if self._details is None:
                from devana.syntax_abstraction.typedefinfo import TypedefInfo
                self._details = TypedefInfo(type_c)

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
    def parent(self) -> any:
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
