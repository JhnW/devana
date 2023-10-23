from typing import Optional, List, Any
import re
from devana.utility.lazy import LazyNotInit, lazy_invoke
from devana.syntax_abstraction.codepiece import CodePiece


class Attribute:
    """An attribute defined by the C++11 and C23 standard. In addition to the standard attributes of the C ++ language,
    it can contain any custom attributes, both specific to compilers and not existing in any compiler.

    This behavior allows attributes to be defined and used only as needed by Devan. And it allows you to enter any
    compilers (no clear list of attributes, it is impossible to know all compiler-specific attributes). And it allows
    you to enter any compilers (no clear list of attributes, it is impossible to know all compiler-specific attributes).
    Whether the attributes will be printed depends on the currently used configuration.
    Attributes are pre-parsed to extract the namespace and arguments. """

    def __init__(self, name: str, namespace: Optional = None, arguments: Optional[List[str]] = None,
                 parent: Optional = None):
        self._name = name
        self._namespace = namespace
        self._arguments = [arg.strip() for arg in arguments] if arguments is not None else None
        self._parent = parent

    @classmethod
    def from_whole_declaration_text(cls, text: str, parent: Optional = None) -> List:
        using_pattern = r"^using (\w+) : "
        using_match = re.match(using_pattern, text)
        namespace = None
        input_text = text
        if using_match:
            namespace = using_match[1]
            input_text = input_text[using_match.span()[1]:]
        pattern = r"(?:\s*(\S+(?:\(.*?\)))\s*,?\s*)|(?:([\w:]+)\s*,?)"
        matches = re.findall(pattern, input_text)
        results = []
        for m in matches:
            match = m[0] if m[0] else m[1]
            attr: Optional[Attribute] = cls.from_text(match, parent)
            if attr:
                if namespace is not None:
                    attr.namespace = namespace
                results.append(attr)
        return results

    @classmethod
    def from_text(cls, text: str, parent: Optional = None) -> Optional:

        pattern = r"(:?(\w+)::)?(\w+)(\((.*?)\))?"
        matches = re.match(pattern, text)
        if not matches:
            return None
        if not matches[0]:
            return None
        else:
            args = None if not matches[5] else cls._parse_arguments(matches[5])
            if args is None and matches[4]:
                args = []
            return Attribute(matches[3], matches[2], args, parent)

    @staticmethod
    def _parse_arguments(text: str) -> List[str]:
        arguments = []
        quote_count = 0
        argument = ""
        for character in text:
            if quote_count == 1:
                argument += character
                if character == "\"":
                    arguments.append(argument)
                    argument = ""
                    quote_count = 0
            else:
                if character == ",":
                    if argument != "":
                        arguments.append(argument)
                    argument = ""
                    quote_count = 0
                elif character == "\"":
                    quote_count = 1
                    argument += character
                else:
                    argument += character
        if argument:
            arguments.append(argument)
        return arguments

    @property
    def name(self) -> str:
        """Attribute name."""
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def namespace(self) -> Optional[str]:
        """Explicitly declared namespace of attributes - not applicable to the using directive."""
        return self._namespace

    @namespace.setter
    def namespace(self, value: Optional[str]):
        self._namespace = value

    @property
    def arguments(self) -> Optional[List[str]]:
        """Arguments of attribute - parsed value."""
        return self._arguments

    @arguments.setter
    def arguments(self, value: List[str]):
        self._arguments = value

    @property
    def parent(self) -> Optional:
        return self._parent

    def __repr__(self):
        namespace = f"{self.namespace}::" if self._namespace else ""
        args = f"({'.'.join(self.arguments)})" if self.arguments is not None else ""
        data = f"{namespace}{self.name}{args}"
        return f"{type(self).__name__}:{data} ({super().__repr__()})"

    def clone(self):
        return Attribute(self.name, self.namespace,
                         self.arguments.copy() if self.arguments is not None else None, self.parent)


class AttributeDeclaration:
    """C++11 attribute declaration. Provides a description of a single declaration in curly braces that may contain
    either the using keyword or a list of multiple attributes."""

    def __init__(self, attributes: List[Attribute], using_namespace: Optional[str] = None, parent: Optional = None):
        self._attributes = attributes
        self._using_namespace = using_namespace
        self._parent = parent

    @property
    def attributes(self) -> List[Attribute]:
        """List of declared attributes."""
        return self._attributes

    @attributes.setter
    def attributes(self, value: List[Attribute]):
        self._attributes = value

    @property
    def using_namespace(self) -> Optional[str]:
        """Namespace with a using directive if present."""
        return self._using_namespace

    @using_namespace.setter
    def using_namespace(self, value: Optional[str]):
        self._using_namespace = value

    @property
    def parent(self) -> Optional:
        return self._parent

    @classmethod
    def create_from_element(cls, source: Any, scope: List[Any], parent: Optional = None) -> List:
        if not hasattr(source, "parent"):
            return []
        if source.parent is None:
            return []

        index_in_scope = scope.index(source)
        begin = source.parent.text_source.begin if index_in_scope == 0 else scope[index_in_scope - 1].text_source.end
        end = source.text_source.begin
        text = CodePiece.from_location(begin, end, source.parent.text_source.file).text
        pattern = r"\[\[(.*?)\]\]"
        attributes_declarations = re.findall(pattern, text)
        if attributes_declarations is None:
            return []
        result = []
        for decl in attributes_declarations:
            using_pattern = r"^using (\w+) : "
            using_match = re.match(using_pattern, decl)
            namespace = None
            if using_match:
                namespace = using_match[1]
            attributes = Attribute.from_whole_declaration_text(decl, parent)
            result.append(AttributeDeclaration(attributes, namespace, parent))

        return result

    def __repr__(self):
        result = ""
        if self.using_namespace is not None:
            result = f"using {self.using_namespace}: "
        result = result + ",".join([repr(a) for a in self.attributes])
        return f"{type(self).__name__}:{result} ({super().__repr__()})"

    def clone(self):
        return AttributeDeclaration([attr.clone() for attr in self.attributes], self.using_namespace, self.parent)


class DescriptiveByAttributes:
    """Mixin class for implement C++ standard attributes linked to code element."""

    def __init__(self, cursor: Optional, parent: Optional = None):
        if cursor is None:
            self._attributes = []
        else:
            self._attributes = LazyNotInit
        self._parent = parent

    @property
    @lazy_invoke
    def attributes(self) -> List[AttributeDeclaration]:
        """C++11/C23 attributes associated with the syntax."""
        self._attributes = AttributeDeclaration.create_from_element(self, self._parent.content if self._parent else [],
                                                                    self)
        return self._attributes

    @attributes.setter
    def attributes(self, value: List[AttributeDeclaration]):
        self._attributes = value

    @property
    def flatten_attributes(self) -> List[Attribute]:
        """List of all attributes without information on which declarations they belong to."""
        result = []
        for attr_decl in self.attributes:
            result = result + attr_decl.attributes
        return result
