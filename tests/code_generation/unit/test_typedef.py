import unittest
from devana.code_generation.printers.default.basictypeprinter import BasicTypePrinter
from devana.code_generation.printers.default.typeexpressionprinter import TypeExpressionPrinter
from devana.code_generation.printers.default.typedefprinter import TypedefPrinter
from devana.code_generation.printers.codeprinter import CodePrinter
from devana.syntax_abstraction.typedefinfo import TypedefInfo
from devana.syntax_abstraction.typeexpression import BasicType, TypeExpression, TypeModification


class TestTypedef(unittest.TestCase):

    def setUp(self):
        printer = CodePrinter()
        printer.register(BasicTypePrinter, BasicType)
        printer.register(TypeExpressionPrinter, TypeExpression)
        printer.register(TypedefPrinter, TypedefInfo)
        self.printer: CodePrinter = printer

    def test_namespace_definition_basic(self):
        source = TypedefInfo()
        source.name = "const_ptr_t"
        source.type_info = TypeExpression()
        source.type_info.details = BasicType.CHAR
        source.type_info.modification |= TypeModification.POINTER | TypeModification.CONST
        result = self.printer.print(source)
        self.assertEqual(result, "typedef const char* const_ptr_t;\n")
