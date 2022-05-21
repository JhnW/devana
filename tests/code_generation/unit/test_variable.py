import unittest
from devana.code_generation.printers.default.basictypeprinter import BasicTypePrinter
from devana.code_generation.printers.default.typeexpressionprinter import TypeExpressionPrinter
from devana.code_generation.printers.default.variableprinter import VariablePrinter, GlobalVariablePrinter
from devana.syntax_abstraction.typeexpression import BasicType, TypeExpression, TypeModification
from devana.syntax_abstraction.variable import Variable, GlobalVariable


class TestVariableCore(unittest.TestCase):

    def test_print_variable_basic(self):
        source = Variable()
        source.name = "test_var"
        source.type = TypeExpression()
        source.type.modification |= TypeModification.CONST
        source.type.details = BasicType.U_SHORT
        printer = VariablePrinter(TypeExpressionPrinter(BasicTypePrinter()))
        result = printer.print(source)
        self.assertEqual(result, "const unsigned short test_var")

    def test_print_global_variable(self):
        source = GlobalVariable()
        source.name = "test_var"
        source.type = TypeExpression()
        source.type.modification |= TypeModification.CONST
        source.type.details = BasicType.U_SHORT
        printer = GlobalVariablePrinter(TypeExpressionPrinter(BasicTypePrinter()))
        result = printer.print(source)
        self.assertEqual(result, "const unsigned short test_var;\n")

    def test_print_variable_with_default_value(self):
        source = Variable()
        source.name = "test_var"
        source.type = TypeExpression()
        source.type.modification |= TypeModification.CONST
        source.type.details = BasicType.U_SHORT
        source.default_value = "(unsigned short)56.7f"
        printer = VariablePrinter(TypeExpressionPrinter(BasicTypePrinter()))
        result = printer.print(source)
        self.assertEqual(result, "const unsigned short test_var = (unsigned short)56.7f")

    def test_print_variable_array(self):
        source = Variable()
        source.name = "test_var"
        source.type = TypeExpression()
        source.type.modification |= TypeModification.ARRAY
        source.type.details = BasicType.U_SHORT
        source.default_value = "{5}"
        printer = VariablePrinter(TypeExpressionPrinter(BasicTypePrinter()))
        result = printer.print(source)
        self.assertEqual(result, "unsigned short test_var[] = {5}")
