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

    def test_definition_basic(self):
        source = TypedefInfo.create_default()
        source.name = "const_ptr_t"
        source.type_info = TypeExpression.create_default()
        source.type_info.details = BasicType.CHAR
        source.type_info.modification |= TypeModification.POINTER | TypeModification.CONST
        result = self.printer.print(source)
        self.assertEqual(result, "typedef const char* const_ptr_t;\n")

    def test_array(self):
        source = TypedefInfo.create_default()
        source.name = "array_typedef"
        source.type_info = TypeExpression.create_default()
        source.type_info.details = BasicType.FLOAT
        source.type_info.modification |= TypeModification.create_array(["16", "32"])
        result = self.printer.print(source)
        self.assertEqual(result, "typedef float array_typedef[16][32];\n")
