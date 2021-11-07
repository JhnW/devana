from devana.code_generation.printers.codeprinter import CodePrinter
from devana.code_generation.printers.default.enumprinter import EnumAsTypePrinter
from devana.code_generation.printers.default.fileprinter import FilePrinter, IncludePrinter
from devana.syntax_abstraction.organizers.sourcefile import SourceFile, IncludeInfo
from devana.code_generation.printers.default.templateparameterprinter import TemplateParameterPrinter
from devana.code_generation.printers.default.namespaceprinter import NamespacePrinter
from devana.syntax_abstraction.namespaceinfo import NamespaceInfo
from devana.code_generation.printers.default.typeexpressionprinter import GenericTypeParameterPrinter
from devana.code_generation.printers.default.typedefprinter import TypedefPrinter
from devana.code_generation.printers.default.enumprinter import EnumPrinter
from devana.code_generation.printers.default.classprinter import *
from devana.code_generation.printers.default.stubtypeprinter import StubTypePrinter
from devana.syntax_abstraction.classinfo import ClassInfo
from devana.syntax_abstraction.templateinfo import GenericTypeParameter
from devana.syntax_abstraction.typedefinfo import TypedefInfo
from devana.syntax_abstraction.enuminfo import EnumInfo
from devana.code_generation.printers.default.unionprinter import UnionPrinter
from devana.syntax_abstraction.unioninfo import UnionInfo
from devana.code_generation.printers.default.usingnamespaceprinter import UsingNamespacePrinter
from devana.code_generation.printers.default.classprinter import FieldPrinter
from devana.syntax_abstraction.classinfo import FieldInfo
from devana.syntax_abstraction.usingnamespace import UsingNamespace
from devana.code_generation.printers.default.basictypeprinter import BasicTypePrinter
from devana.code_generation.printers.default.typeexpressionprinter import TypeExpressionPrinter
from devana.code_generation.printers.default.variableprinter import VariablePrinter, GlobalVariablePrinter
from devana.syntax_abstraction.typeexpression import BasicType, TypeExpression
from devana.syntax_abstraction.variable import Variable, GlobalVariable
from devana.code_generation.stubtype import StubType


def create_default_printer() -> CodePrinter:
    printer = CodePrinter()
    printer.register(BasicTypePrinter, BasicType)
    printer.register(AccessSpecifierPrinter, AccessSpecifier)
    printer.register(MethodPrinter, MethodInfo)
    printer.register(ConstructorPrinter, ConstructorInfo)
    printer.register(DestructorPrinter, DestructorInfo)
    printer.register(FieldPrinter, FieldInfo)
    printer.register(ClassPrinter, ClassInfo)
    printer.register(EnumPrinter, EnumInfo)
    printer.register(EnumAsTypePrinter, EnumInfo, TypeExpression)
    printer.register(FilePrinter, SourceFile)
    printer.register(IncludePrinter, IncludeInfo)
    printer.register(FunctionPrinter, FunctionInfo)
    printer.register(VariablePrinter, FunctionInfo.Argument)
    printer.register(NamespacePrinter, NamespaceInfo)
    printer.register(TemplateParameterPrinter, TemplateInfo.TemplateParameter)
    printer.register(TypedefPrinter, TypedefInfo)
    printer.register(TypeExpressionPrinter, TypeExpression)
    printer.register(GenericTypeParameterPrinter, GenericTypeParameter)
    printer.register(UnionPrinter, UnionInfo)
    printer.register(UsingNamespacePrinter, UsingNamespace)
    printer.register(VariablePrinter, Variable)
    printer.register(GlobalVariablePrinter, GlobalVariable)
    printer.register(StubTypePrinter, StubType)

    return printer
