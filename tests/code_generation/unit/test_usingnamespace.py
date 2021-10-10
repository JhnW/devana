import unittest
from devana.code_generation.printers.default.basictypeprinter import BasicTypePrinter
from devana.code_generation.printers.default.typeexpressionprinter import TypeExpressionPrinter
from devana.code_generation.printers.default.usingnamespaceprinter import UsingNamespacePrinter
from devana.code_generation.printers.default.classprinter import FieldPrinter
from devana.code_generation.printers.codeprinter import CodePrinter
from devana.syntax_abstraction.typeexpression import BasicType
from devana.syntax_abstraction.classinfo import FieldInfo
from devana.syntax_abstraction.typeexpression import TypeExpression
from devana.syntax_abstraction.usingnamespace import UsingNamespace


class TestUsingNamespace(unittest.TestCase):

    def setUp(self):
        printer = CodePrinter()
        printer.register(BasicTypePrinter, BasicType)
        printer.register(TypeExpressionPrinter, TypeExpression)
        printer.register(FieldPrinter, FieldInfo)
        printer.register(UsingNamespacePrinter, UsingNamespace)
        self.printer: CodePrinter = printer

    def test_print_simple_using_namespace(self):
        source = UsingNamespace()
        source.namespaces = ["Test1"]
        result = self.printer.print(source)
        self.assertEqual("using namespace Test1;\n", result)

    def test_print_multiple_using_namespace(self):
        source = UsingNamespace()
        source.namespaces = ["Test1", "Test2", "A"]
        result = self.printer.print(source)
        self.assertEqual("using namespace Test1::Test2::A;\n", result)
