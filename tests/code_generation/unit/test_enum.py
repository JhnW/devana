import unittest
from devana.code_generation.printers.default.basictypeprinter import BasicTypePrinter
from devana.code_generation.printers.default.enumprinter import EnumPrinter
from devana.code_generation.printers.codeprinter import CodePrinter
from devana.syntax_abstraction.typeexpression import BasicType
from devana.syntax_abstraction.enuminfo import EnumInfo


class TestEnum(unittest.TestCase):

    def setUp(self):
        printer = CodePrinter()
        printer.register(BasicTypePrinter, BasicType)
        printer.register(EnumPrinter, EnumInfo)
        self.printer: CodePrinter = printer

    def test_enum_basic(self):
        source = EnumInfo()
        source.name = "foo"
        source.values = [EnumInfo.EnumValue(), EnumInfo.EnumValue(), EnumInfo.EnumValue()]
        source.values[0].name = "A"
        source.values[0].is_default = True
        source.values[1].name = "B"
        source.values[1].is_default = False
        source.values[1].value = 7
        source.values[2].name = "C"
        source.values[2].is_default = True
        result = self.printer.print(source)
        self.assertEqual("enum foo\n{\n    A,\n    B = 7,\n    C\n};\n", result)

    def test_empty_enum_basic(self):
        source = EnumInfo()
        source.name = "foo"
        source.values = []
        result = self.printer.print(source)
        self.assertEqual(result, "enum foo\n{\n};\n")

    def test_numeric_type_enum(self):
        source = EnumInfo()
        source.name = "foo"
        source.numeric_type = BasicType.CHAR
        source.values = [EnumInfo.EnumValue(), EnumInfo.EnumValue(), EnumInfo.EnumValue()]
        source.values[0].name = "A"
        source.values[0].is_default = True
        source.values[1].name = "B"
        source.values[1].is_default = False
        source.values[1].value = 7
        source.values[2].name = "C"
        source.values[2].is_default = True
        result = self.printer.print(source)
        self.assertEqual("enum foo: char\n{\n    A,\n    B = 7,\n    C\n};\n", result)