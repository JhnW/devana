import unittest
from devana.code_generation.printers.default.enumprinter import EnumPrinter, EnumAsTypePrinter
from devana.syntax_abstraction.enuminfo import EnumInfo
from devana.code_generation.printers.default.functionprinter import FunctionPrinter
from devana.code_generation.printers.default.variableprinter import VariablePrinter
from devana.code_generation.printers.default.basictypeprinter import BasicTypePrinter
from devana.code_generation.printers.default.typeexpressionprinter import TypeExpressionPrinter
from devana.code_generation.printers.codeprinter import CodePrinter
from devana.syntax_abstraction.functioninfo import FunctionInfo
from devana.syntax_abstraction.typeexpression import TypeModification, TypeExpression, BasicType
from devana.syntax_abstraction.variable import Variable


class TestContextBasic(unittest.TestCase):

    def setUp(self):
        printer = CodePrinter()
        printer.register(BasicTypePrinter, BasicType)
        printer.register(EnumAsTypePrinter, EnumInfo, TypeExpression)
        printer.register(EnumPrinter, EnumInfo)
        printer.register(FunctionPrinter, FunctionInfo)
        printer.register(VariablePrinter, Variable)
        printer.register(BasicTypePrinter, BasicType)
        printer.register(TypeExpressionPrinter, TypeExpression)
        printer.register(VariablePrinter, FunctionInfo.Argument)
        self.printer: CodePrinter = printer

    def test_context_basic(self):
        enum_type = EnumInfo()
        enum_type.name = "TextEnum"
        source = FunctionInfo()
        source.name = "foo"
        source.return_type = TypeExpression()
        source.return_type.details = BasicType.LONG
        arg1 = FunctionInfo.Argument()
        arg1.type = TypeExpression()
        arg1.type.details = enum_type
        arg1.name = "a"
        arg1.type.modification = TypeModification.POINTER | TypeModification.CONST
        arg2 = FunctionInfo.Argument()
        arg2.type = TypeExpression()
        arg2.type.details = BasicType.INT
        arg2.type.modification = TypeModification.POINTER
        arg2.default_value = "nullptr"
        arg2.name = "b"
        source.arguments = [arg1, arg2]
        result = self.printer.print(source)
        self.assertEqual(result, "long foo(const TextEnum* a, int* b = nullptr);\n")
