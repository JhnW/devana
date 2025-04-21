import re
from pathlib import Path
from typing import Optional, List, Union, Tuple, Any, Iterable
from clang import cindex
from devana.syntax_abstraction.codepiece import CodePiece
from devana.syntax_abstraction.typeexpression import TypeExpression, TypeModification
from devana.syntax_abstraction.conceptinfo import ConceptUsage
from devana.syntax_abstraction.organizers.codecontainer import CodeContainer
from devana.syntax_abstraction.organizers.lexicon import Lexicon
from devana.utility.lazy import LazyNotInit, lazy_invoke
from devana.utility.errors import ParserError
from devana.utility.traits import IBasicCreatable, ICursorValidate
from devana.utility.init_params import init_params
from devana.syntax_abstraction.syntax import ISyntaxElement
from devana.configuration import Configuration


class GenericTypeParameter(ISyntaxElement):
    """An unresolved generic template parameter, known idiomatically in C++ as T."""

    def __init__(self, name: str, parent: Optional = None):
        self._name = name
        self._parent = parent

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @staticmethod
    def from_cursor(type_c, cursor: cindex.Cursor, parent: Optional = None) -> Optional["GenericTypeParameter"]:
        if type_c.kind == cindex.TypeKind.UNEXPOSED:
            if type_c.get_num_template_arguments() > 0:
                return None
            if hasattr(cursor, 'get_children'):
                for c in cursor.get_children():
                    if c.kind == cindex.CursorKind.TYPE_REF:
                        return GenericTypeParameter(c.type.spelling, parent)
                    elif c.kind == cindex.CursorKind.TEMPLATE_REF:
                        if getattr(c, "referenced", None) and c.referenced.kind == cindex.CursorKind.CONCEPT_DECL:
                            text = type_c.spelling
                            return GenericTypeParameter(text[len("const "):] if text.startswith("const ") else text, parent)
                        return None
            text = type_c.spelling
            if "::" in text:
                return None
            return GenericTypeParameter(text[len("const "):] if text.startswith("const ") else text, parent)
        return None

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.name == other.name

    def __repr__(self):
        return f"{type(self).__name__}:{self.name} ({super().__repr__()})"


class TemplateInfo(IBasicCreatable, ICursorValidate, ISyntaxElement):
    """General template syntax information abut template definition."""

    class TemplateParameter(IBasicCreatable, ICursorValidate, ISyntaxElement):
        """A description of the generic component for the type/function claim."""
        def __init__(self, cursor: Optional[cindex.Cursor] = None, parent: Optional = None):
            self._cursor = cursor
            self._parent = parent
            if cursor is None:
                self._specifier = "typename"
                self._name = "T"
                self._default_value = None
                self._is_variadic = False
            else:
                if not self.is_cursor_valid(cursor):
                    raise ParserError("Template parameter expect TEMPLATE_TYPE_PARAMETER cursor kind.")
                self._specifier = LazyNotInit
                self._name = LazyNotInit
                self._default_value = LazyNotInit
                self._is_variadic = LazyNotInit
            self._lexicon = Lexicon.create(self)

        @classmethod
        def create_default(cls, parent: Optional = None) -> "TemplateInfo.TemplateParameter":
            return cls(None, parent)

        @classmethod
        @init_params(skip={"parent"})
        def from_params( # pylint: disable=unused-argument, too-many-positional-arguments
                cls,
                parent: Optional[ISyntaxElement] = None,
                specifier: Optional[Union[str, ConceptUsage]] = None,
                name: Optional[str] = None,
                default_value: Optional[str] = None,
                is_variadic: Optional[bool] = None,
        ) -> "TemplateInfo.TemplateParameter":
            return cls(None, parent)

        @classmethod
        def from_cursor(cls, cursor: cindex.Cursor, parent: Optional = None) -> Optional[("TemplateInfo"
                                                                                          ".TemplateParameter")]:
            if not cls.is_cursor_valid(cursor):
                return None
            return cls(cursor, parent)

        @staticmethod
        def is_cursor_valid(cursor: cindex.Cursor) -> bool:
            return cursor.kind == cindex.CursorKind.TEMPLATE_TYPE_PARAMETER

        @property
        @lazy_invoke
        def specifier(self) -> Union[ConceptUsage, str]:
            """Keyword or ConceptUsage instance preceding the name."""

            if maybe_concept := ConceptUsage.from_cursor(cursor=self._cursor, parent=self):
                self._specifier = maybe_concept
                return self._specifier

            self._specifier = "class" if CodePiece(self._cursor).text.find("class ") != -1 else "typename"
            return self._specifier

        @specifier.setter
        def specifier(self, value: Union[ConceptUsage, str]):
            if not isinstance(value, ConceptUsage) and value not in ("class", "typename"):
                raise ValueError("Specifier must be class, typename, or an instance of ConceptUsage.")
            self._specifier = value

        @property
        @lazy_invoke
        def name(self) -> str:
            """Name of string parameter."""
            self._name = self._cursor.spelling
            return self._name

        @name.setter
        def name(self, value):
            self._name = value

        @property
        @lazy_invoke
        def default_value(self) -> Optional[str]:
            """Default value of parameter."""
            self._default_value = None
            text = CodePiece(self._cursor).text
            value = re.compile(self.name + r"\s*=\s*(.+)").findall(text)
            if len(value) == 1:
                self._default_value = value[0]
            elif len(value) > 1:
                raise TypeError("Invalid text.")
            return self._default_value

        @default_value.setter
        def default_value(self, value):
            self._default_value = value

        @property
        @lazy_invoke
        def is_variadic(self) -> bool:
            self._is_variadic = False
            text = CodePiece(self._cursor).text
            if re.search(r"\.\.\.\s*" + self.name, text):
                self._is_variadic = True
            return self._is_variadic

        @is_variadic.setter
        def is_variadic(self, value):
            self._is_variadic = value

        @property
        def lexicon(self) -> CodeContainer:
            """Current lexicon storage of an object."""
            return self._lexicon

        @property
        def parent(self):
            return self._parent

        def __eq__(self, other):
            if not isinstance(other, type(self)):
                return False
            return self.name == other.name and self.is_variadic == other.is_variadic

    def __init__(self, cursor: Optional[cindex.Cursor] = None, parent: Optional = None):
        self._cursor = cursor
        self._parent = parent
        if cursor is None:
            self._specialisation_values = []
            self._specialisations = []
            self._parameters = []
            self._is_empty = True
            self._is_variadic = False
            self._requires = None
        else:
            if not self.is_cursor_valid(cursor):
                raise ParserError("Template parameter expect FUNCTION_TEMPLATE cursor kind.")
            self._specialisations_value = LazyNotInit
            self._specialisations = LazyNotInit
            self._parameters = LazyNotInit
            self._is_empty = LazyNotInit
            self._is_variadic = LazyNotInit
            self._requires = LazyNotInit
        self._lexicon = Lexicon.create(self)

    @classmethod
    def create_default(cls, parent: Optional = None) -> "TemplateInfo":
        return cls(None, parent)

    @classmethod
    @init_params(skip={"parent"})
    def from_params( # pylint: disable=unused-argument, too-many-positional-arguments
            cls,
            parent: Optional[ISyntaxElement] = None,
            specialisation_values: Optional[List[Union[TypeExpression, str]]] = None,
            specialisations: Optional[Tuple[Any, ...]] = None,
            parameters: Optional[List[TemplateParameter]] = None,
            is_empty: Optional[bool] = None,
            lexicon: Optional[Lexicon] = None,
            requires: Optional[List[Union[str, ConceptUsage]]] = None
    ) -> "TemplateInfo":
        return cls(None, parent)

    @classmethod
    def from_cursor(cls, cursor: cindex.Cursor, parent: Optional = None) -> Optional["TemplateInfo"]:
        if not cls.is_cursor_valid(cursor):
            return None
        return cls(cursor, parent)

    @staticmethod
    def is_cursor_valid(cursor: cindex.Cursor) -> bool:
        valid_cursors = (
            cindex.CursorKind.FUNCTION_TEMPLATE,
            cindex.CursorKind.CLASS_TEMPLATE,
            cindex.CursorKind.CLASS_TEMPLATE_PARTIAL_SPECIALIZATION,
            cindex.CursorKind.CONCEPT_DECL,
            cindex.CursorKind.TYPE_ALIAS_TEMPLATE_DECL
        )
        return cursor.kind in valid_cursors or re.search(
            r"template\s*<>", CodePiece(cursor).text
        ) is not None

    @property
    @lazy_invoke
    def specialisation_values(self) -> List[Union[TypeExpression, str]]:
        """Used values for partial specialisation, types or string for other values.
        Return all other defined specialisations of template."""
        self._specialisation_values = []
        num_args = self._cursor.type.get_num_template_arguments()
        is_type = True
        if num_args <= 0:
            num_args = self._cursor.get_num_template_arguments()
            is_type = False
        for i in range(num_args):
            if is_type:
                t = TypeExpression(self._cursor.type.get_template_argument_type(i), self)
            else:
                t = TypeExpression(self._cursor.get_template_argument_type(i), self)
            self._specialisation_values.append(t)
            # reformat type names
            if t.is_generic:
                m = re.match(r"type-parameter-(\d+)-(\d+)", t.name)
                i = int(m.group(2))
                t._name = self.parameters[i].name  # pylint: disable=protected-access
                t.details._name = t.name  # pylint: disable=protected-access

        if self._specialisation_values:
            return self._specialisation_values

        # here be dragons
        # for some cases cursor will not return template parameters, so we will do a very ugly hack with parse fake file
        if self.parent is None:
            return self._specialisation_values

        tokens = list(self._cursor.get_tokens())
        tokens = [t.spelling for t in tokens]
        base_text = "".join(tokens)
        pattern = self.parent.name + r"<(.+)>\("
        match = re.findall(pattern, base_text)
        if match:
            arguments = match[0].split(",")
            num_args = len(arguments)
            code_piece = CodePiece(self._cursor.lexical_parent)
            text = code_piece.text
            fnc_text = self.parent.text_source.text
            text = text.split(fnc_text)
            function_placeholder = "void ___devana______fooPlaceholderToGetParm("
            for i, arg in enumerate(arguments):
                function_placeholder += arg + f" a_{i}, "
            function_placeholder += "int a);\n"
            text = text[0] + "\n" + fnc_text + "\n" + function_placeholder + "\n" + text[1]

            from devana.syntax_abstraction.functioninfo import FunctionInfo  # pylint: disable=import-outside-toplevel
            # pylint: disable=import-outside-toplevel
            from devana.syntax_abstraction.organizers.sourcefile import SourceFile
            idx = cindex.Index.create()
            tu = idx.parse('tmp.h', args=Configuration.get_configuration(self).parsing.parsing_options(),
                           unsaved_files=[('tmp.h', text)], options=0)
            file = SourceFile(tu.cursor)
            file.path = Path('tmp.h')  # normally file uses absolute paths, we need to work around

            parents = []
            element = self.parent
            while True:
                parent = element.parent
                if parent is None or isinstance(parent, SourceFile):
                    break
                parents.append(parent.name)

            container = file
            for p in reversed(parents):
                container = container.content
                # pylint: disable=cell-var-from-loop
                container = list(filter(lambda x: hasattr(x, "name") and x.name == p, container))[0]

            stub_function_find = filter(
                lambda f: hasattr(f, "name") and f.name == "___devana______fooPlaceholderToGetParm",
                container.content)
            stub_function: FunctionInfo = list(stub_function_find)[0]
            stub_function._parent = self.parent.parent  # pylint: disable=protected-access
            stub_function._lexicon = self.parent.lexicon  # pylint: disable=protected-access

            # now extracts type information based on stub functions args
            for i in range(num_args):
                arg = stub_function.arguments[i]
                self._specialisation_values.append(arg.type)

        return self._specialisation_values

    @specialisation_values.setter
    def specialisation_values(self, value):
        self._specialisation_values = value

    @property
    @lazy_invoke
    def specialisations(self) -> Tuple:
        """Return all others defined specialisations of template."""
        self._specialisations = []
        if self.lexicon is None:
            return ()
        if self.parent is None:
            return ()

        values = self._lexicon.find_content(self.parent.name)
        if values is None:
            return ()
        values = filter(lambda v: isinstance(v, type(self.parent)), values)
        values = filter(lambda v: v.template is not None, values)
        values = filter(lambda v: v.template.specialisation_values, values)

        from devana.syntax_abstraction.functioninfo import FunctionInfo  # pylint: disable=import-outside-toplevel
        if isinstance(self.parent, FunctionInfo):  # handle overloading functions
            if self.parent.template.specialisation_values:
                return ()

            # find index of generic with names
            for s in values:
                if len(s.template.specialisation_values) != len(self.parameters):
                    return ()
                if len(self.parent.arguments) != len(s.arguments):
                    continue
                is_valid = True
                for i in range(len(self.parent.arguments)):
                    if self.parent.arguments[i].type.is_generic:
                        # find template parameter
                        param_id = None
                        for _, p in enumerate(self.parameters):
                            if p.name == self.parent.arguments[i].type.details.name:
                                param_id = i
                        if param_id is None:
                            is_valid = False
                            break
                        spe_type = s.template.specialisation_values[i]
                        expected_type_mod = self.parent.arguments[i].type.modification
                        spec_type_mod = spe_type.modification
                        # check type mod duplicated (we do not support a multiple pointer)
                        if not ~((expected_type_mod & spec_type_mod) & ~TypeModification.NONE):
                            is_valid = False
                            break
                        if s.arguments[i].type.details != spe_type.details:
                            is_valid = False
                            break
                        if (expected_type_mod | spec_type_mod) != s.arguments[i].type.modification:
                            is_valid = False
                            break
                        is_valid = True
                    else:
                        if self.parent.arguments[i].type != s.arguments[i].type:
                            is_valid = False
                            break
                if is_valid:
                    self._specialisations.append(s)
        return tuple(self._specialisations)

    @specialisations.setter
    def specialisations(self, value):
        self._specialisations = value

    @property
    def specialisations_family(self) -> Tuple:
        """Return all defined specializations of template including this one."""
        if self._lexicon is None:
            return ()

        functions = self._lexicon.find_content(self.parent.name)
        if functions is None:
            return ()
        functions = tuple(filter(lambda x: x.template is not None, functions))

        return functions

    @property
    @lazy_invoke
    def parameters(self) -> List[TemplateParameter]:
        """Template parameters list."""
        self._parameters = []
        for c in self._cursor.get_children():
            try:
                self._parameters.append(self.TemplateParameter(c, self.parent))
            except ValueError:
                break
        return self._parameters

    @parameters.setter
    def parameters(self, value):
        self._parameters = value

    @property
    @lazy_invoke
    def is_empty(self) -> bool:
        self._is_empty = False
        return self._is_empty

    @is_empty.setter
    def is_empty(self, value):
        self._is_empty = value

    @property
    def lexicon(self) -> CodeContainer:
        """Current lexicon storage of an object."""
        return self._lexicon

    @lexicon.setter
    def lexicon(self, value):
        self._lexicon = value

    @property
    def parent(self) -> ISyntaxElement:
        return self._parent

    @property
    @lazy_invoke
    def requires(self) -> Optional[List[Union[str, ConceptUsage]]]:
        """Extracts constraints from the 'requires' clause of the template. None if absent."""
        match = re.search(
            r"template\s*<[^>]+>\s*(?:\r?\n\s*)?requires\s+(?:\r?\n\s*)?(.+?)(?=\r?\n\S|$)",
            CodePiece(self._cursor).text,
            flags=re.DOTALL
        )
        if not match:
            self._requires = None
            return self._requires
        self._requires = []

        def find_concepts(cursor: cindex.Cursor) -> Iterable[cindex.Cursor]:
            for child in cursor.get_children():
                if child.kind == cindex.CursorKind.CONCEPT_SPECIALIZATION_EXPR:
                    yield child
                if child.kind in (
                        cindex.CursorKind.BINARY_OPERATOR,
                        cindex.CursorKind.PAREN_EXPR
                ):
                    yield from find_concepts(child)

        # clang does not provide info for all things in the requires (e.g., 'or', 'true'),
        raw_elements: List[str] = re.findall(
            r'\(|\)|[^\s()<]+(?:\s*<\s*[^\s>]+(?:\s+[^\s>]+)*\s*>)?',
            match.group(1)
        )
        cursors: List[cindex.Cursor] = list(find_concepts(self._cursor))
        for raw_element in raw_elements:
            if len(cursors) > 0 and re.search(r'<[^>]+>', raw_element):

                maybe_concept = ConceptUsage.from_cursor(cursor=cursors.pop(0), parent=self.parent)
                if maybe_concept is not None:
                    self._requires.append(maybe_concept)
                    continue
            self._requires.append(raw_element.strip())
        return self._requires

    @requires.setter
    def requires(self, value: Optional[List[Union[str, ConceptUsage]]]) -> None:
        self._requires = value
