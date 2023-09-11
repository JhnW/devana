"""
Syntax abstraction provides pythons classes, representing C ++ code elements.
"""

from .variable import Variable, GlobalVariable
from .usingnamespace import UsingNamespace
from .unioninfo import UnionInfo
from .typeexpression import TypeExpression, BasicType, TypeModification
from .typedefinfo import TypedefInfo
from .templateinfo import GenericTypeParameter, TemplateInfo
from .namespaceinfo import NamespaceInfo
from .functioninfo import FunctionInfo, FunctionModification
from .enuminfo import EnumInfo
from .codepiece import CodePiece
from .codelocation import CodeLocation
from .comment import Comment, CommentMarker
from .classinfo import ClassMember, ConstructorInfo, DestructorInfo, FieldInfo, MethodInfo, SectionInfo, ClassInfo
from .externc import ExternC
from .functiontype import FunctionType
from .using import Using
from .syntax import ISyntaxElement
