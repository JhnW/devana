import unittest
from devana.code_generation.printers.codeprinter import CodePrinter
from devana.syntax_abstraction.typeexpression import TypeModification, TypeExpression, BasicType
from devana.syntax_abstraction.functiontype import FunctionType
from devana.code_generation.printers.default.functiontypeprinter import FunctionTypePrinter


class TestFunctionTypeCore(unittest.TestCase):

    def setUp(self):
        printer = CodePrinter()
        printer.register(FunctionTypePrinter, FunctionType)
        self.printer: CodePrinter = printer

    def test_print_function_type(self):
        source = FunctionType()
        source.arguments = [TypeExpression()]
        source.arguments[0].modification |= TypeModification.CONST
        source.arguments[0].details = BasicType.CHAR
        source.return_type = TypeExpression()
        source.return_type.details = BasicType.VOID
        result = self.printer.print(source)
        self.assertEqual(result, "void ()(const char)")
