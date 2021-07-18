from typing import Optional, List, NoReturn, Union
from devana.syntax_abstraction.organizers.codecontainer import CodeContainer
from devana.utility.errors import ParserError, CodeError
from clang import cindex


class Lexicon:
    """Class storage all multiple usage code elements in working context.

    Lexicon hold reference to all definitions and declarations. It will hold all typedefs, namespaces, classes,
    functions, methods and templates. Main application of Lexicon is avoid parsing or created source code data types
    again. Existing data can be taken from lexicon.
    Additional, Lexicon can hold data who are not present in source files e.g. for make consistent devana structures
    and handcrafted code generation.
    Lexicon data are stacked in tree-like structures by data namespaces."""

    @classmethod
    def create(cls, source=None):
        """Use this method to create lexicon inside syntax object to fit lexicon scope."""
        if source is None:
            if issubclass(type(source), CodeContainer):
                return cls(source)
            raise ValueError("CodeContainer source is needed for root lexicon.")
        if source.parent is None:
            if issubclass(type(source), CodeContainer):
                return cls(source)
            return None
        if source.parent.lexicon is None:
            if issubclass(type(source), CodeContainer):
                return cls(source)
            raise ValueError("CodeContainer source is needed for root lexicon.")

        if issubclass(type(source), CodeContainer):
            match = list(x for x in source.parent.lexicon.nodes if x.namespace == source.namespace)
            if match:
                assert len(match) == 1
                instance: Lexicon = match[0]

                # do not add multiple definitions of the same type to Lexington and replace definition by
                # declaration if possible

                if hasattr(source, "is_declaration") and (hasattr(source, "template") and source.template is None):
                    sources = []
                    for s in instance._sources:
                        if not hasattr(s, "is_declaration"):
                            sources.append(s)
                            continue
                        if hasattr(s, "template") and s.template is not None:
                            sources.append(s)
                            continue
                        if s.name == source.name:
                            if source.is_declaration:
                                if s.is_declaration:
                                    sources.append(s)
                                else:
                                    sources.append(source)
                            else:  # source is definition
                                if s.is_definition:
                                    raise ParserError("Multiple definitions.")
                                sources.append(source)
                    instance._sources = sources
                else:
                    instance._sources.append(source)

                return instance
            return cls(source)
        else:
            return source.parent.lexicon

    def __init__(self, source=None):
        assert issubclass(type(source), CodeContainer) or source is None
        self._sources: List[CodeContainer] = []
        self._sources.append(source)
        self._content_internal = []
        self._nodes = []
        if source is None:
            self._namespace = None
            self._parent = None
        else:
            self._namespace = source.namespace
            if source.parent is None:
                self._parent = None
            else:
                self._parent = source.parent.lexicon
                self._parent.nodes.append(self)

    @property
    def parent(self) -> Optional:
        return self._parent

    @property
    def namespace(self) -> Optional[str]:
        return self._namespace

    def merge(self, lexicon) -> NoReturn:
        """Merge lexicon with another one."""
        pass

    @property
    def nodes(self) -> List:
        """Return list of nested lexicons."""
        return self._nodes

    def find_node(self, name):
        """Deep search node (namespace)."""
        content = self.nodes
        result = list(c for c in content if c.namespace == name)
        if result:
            return result[0]

        for n in self.allowed_namespaces:
            if n.namespace == name:
                return n

        if self.parent is None:
            return None
        return self.parent.find_node(name)

    @property
    def sources(self) -> List[CodeContainer]:
        return self._sources

    @property
    def content(self) -> List:
        """Return code content."""
        content = []
        for s in self._sources:
            if hasattr(s, "content"):
                content.extend(s.content)
            if s is not None:
                content.append(s)
            for c in self._content_internal:
                if issubclass(type(c), CodeContainer):
                    content.extend(c.content)
                else:
                    content.append(c)
        return content

    def append_content(self, value):
        self._content_internal.append(value)

    def find_content(self, name: str, namespaces=None) -> Optional[List]:
        if namespaces is None:
            namespaces = []

        if namespaces:
            node = self.find_node(namespaces[0])
            if node is None:
                raise CodeError("Namespace do not know in Lexicon.")
            return node.find_content(name, namespaces[1:])

        content = self.content
        result = list(c for c in content if hasattr(c, "name") and c.name == name)
        if result:
            return result

        for s in self._sources:
            if s is not None:
                for n in s.allowed_namespaces:
                    if isinstance(n, CodeContainer):
                        if n.lexicon is not None:
                            content = n.lexicon.content
                            result = list(c for c in content if hasattr(c, "name") and c.name == name)
                            if result:
                                return result
        if self.parent is None:
            return None
        return self.parent.find_content(name)

    def _find_type_from_name(self, name: str) -> Optional:
        from devana.syntax_abstraction.typedefinfo import TypedefInfo
        from devana.syntax_abstraction.namespaceinfo import NamespaceInfo
        content = self.find_content(name)
        if content is None:
            return None
        content = list(
            filter(lambda x: issubclass(type(x), CodeContainer) or issubclass(type(x), TypedefInfo), content))
        content = list(filter(lambda x: not isinstance(x, NamespaceInfo), content))

        if content:
            definition = list(filter(lambda x: hasattr(x, "is_definition") and x.is_definition, content))
            assert len(definition) <= 1
            if definition:
                return definition[0]
            return content[0]
        return None

    def _find_type_from_cursor(self, cursor: cindex.Cursor):
        result = self.find_type(cursor.spelling)

        namespaces: List[str] = []
        c = cursor
        for _ in range(2048):
            if c is None:
                raise ParserError("Class template namespace is not allowed.")
            if c.kind == cindex.CursorKind.TRANSLATION_UNIT:
                break
            namespaces.append(c.spelling)
            c = c.semantic_parent

        if not namespaces:
            return result

        lex = self.root
        result = None
        templates_count = 0
        from devana.syntax_abstraction.classinfo import ClassInfo
        for i, n in enumerate(reversed(namespaces)):
            if i == len(namespaces) - 1:
                result = lex.find_content(n)
            else:
                result = lex.find_node(n)
                if result is None:
                    result = lex.find_content(n)
            if result is None:
                return None

            if isinstance(result, Lexicon):
                lex = result
                template_check = result.sources[0]
            else:
                results = result
                result = result[0]
                for r in results:
                    if hasattr(r, "is_definition") and r.is_definition:
                        result = r
                        break
                template_check = result
                lex = result.lexicon
            if isinstance(template_check, ClassInfo):
                if template_check.template is not None:
                    templates_count += 1

        if templates_count > 0:
            if templates_count == 1:
                if isinstance(result, ClassInfo):
                    if result.template is None:
                        raise ParserError("Class template namespace is not allowed.")
                else:
                    raise ParserError("Class template namespace is not allowed.")
            else:
                raise ParserError("Class template namespace is not allowed.")

        return result

    def find_type(self, element: Union[str, cindex.Cursor]) -> Optional:
        if type(element) is str:
            return self._find_type_from_name(element)
        else:
            return self._find_type_from_cursor(element)

    def find_cursor(self, cursor: cindex.Cursor) -> Optional:

        def finder(lexicon, searched_cursor):
            for c in lexicon.content:
                if c._cursor == searched_cursor:
                    return c
            for node in lexicon.nodes:
                result = finder(node, searched_cursor)
                if result is not None:
                    return result
            return None

        return finder(self.root, cursor)

    @property
    def allowed_namespaces(self) -> List:
        """List of all other allowed namespaces in container without Name:: prefix given by using namespace."""
        from devana.syntax_abstraction.usingnamespace import UsingNamespace
        allowed = []
        for c in self.content:
            if isinstance(c, UsingNamespace):
                if c.namespace is not None:
                    allowed += c.namespace.allowed_namespaces
        if self.namespace is not None:
            allowed.append(self)
        return allowed

    @property
    def namespaces_chain(self) -> List[str]:
        """From root to current lexicon namespaces."""
        chain = []
        lex = self
        while True:
            namespace = lex.namespace
            if namespace is None:
                break
            chain.append(namespace)
            lex = lex.parent
            if lex is None:
                break
        chain.reverse()
        return chain

    @property
    def root(self) -> Optional:
        """Root of lexicon."""
        if self.parent is None:
            return self
        else:
            return self.parent.root
