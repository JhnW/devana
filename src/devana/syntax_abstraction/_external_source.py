from typing import Optional, Any
from clang import cindex


def create_external(cursor: cindex.Cursor) -> Optional[Any]:
    """Create external content without lexicon."""
    # pylint: disable=import-outside-toplevel
    from devana.syntax_abstraction.classinfo import ClassInfo
    from devana.syntax_abstraction.unioninfo import UnionInfo
    from devana.syntax_abstraction.functioninfo import FunctionInfo
    from devana.syntax_abstraction.typedefinfo import TypedefInfo
    from devana.syntax_abstraction.namespaceinfo import NamespaceInfo
    from devana.syntax_abstraction.usingnamespace import UsingNamespace
    from devana.syntax_abstraction.enuminfo import EnumInfo
    from devana.syntax_abstraction.variable import GlobalVariable
    from devana.syntax_abstraction.externc import ExternC
    from devana.syntax_abstraction.using import Using
    types = [ClassInfo, UnionInfo, FunctionInfo, EnumInfo, TypedefInfo, NamespaceInfo, UsingNamespace,
             GlobalVariable, ExternC, Using]
    for candidate in types:
        instance: Optional = candidate.from_cursor(cursor)
        if instance:
            return instance
    return None
