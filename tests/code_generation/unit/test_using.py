import unittest
from devana.code_generation.printers.default.basictypeprinter import BasicTypePrinter
from devana.code_generation.printers.default.typeexpressionprinter import TypeExpressionPrinter
from devana.code_generation.printers.default.usingprinter import UsingPrinter
from devana.code_generation.printers.codeprinter import CodePrinter
from devana.syntax_abstraction.using import Using
from devana.syntax_abstraction.typeexpression import BasicType, TypeExpression, TypeModification


class TestUsing(unittest.TestCase):

    def setUp(self):
        printer = CodePrinter()
        printer.register(BasicTypePrinter, BasicType)
        printer.register(TypeExpressionPrinter, TypeExpression)
        printer.register(UsingPrinter, Using)
        self.printer: CodePrinter = printer

    def test_definition_basic(self):
        source = Using()
        source.name = "const_ptr_t"
        source.type_info = TypeExpression()
        source.type_info.details = BasicType.CHAR
        source.type_info.modification |= TypeModification.POINTER | TypeModification.CONST
        result = self.printer.print(source)
        self.assertEqual(result, "using const_ptr_t = const char*;\n")
