import unittest
from devana.code_generation.printers.default.basictypeprinter import BasicTypePrinter
from devana.code_generation.printers.default.typeexpressionprinter import TypeExpressionPrinter
from devana.code_generation.printers.default.variableprinter import VariablePrinter, GlobalVariablePrinter
from devana.syntax_abstraction.variable import Variable, GlobalVariable
from devana.code_generation.printers.codeprinter import CodePrinter
from devana.syntax_abstraction.typeexpression import TypeModification, TypeExpression, BasicType
from devana.syntax_abstraction.functiontype import FunctionType
from devana.code_generation.printers.default.functiontypeprinter import FunctionTypePrinter


class TestVariableCore(unittest.TestCase):

    def test_print_variable_basic(self):
        source = Variable.create_default()
        source.name = "test_var"
        source.type = TypeExpression.create_default()
        source.type.modification |= TypeModification.CONST
        source.type.details = BasicType.U_SHORT
        printer = VariablePrinter(TypeExpressionPrinter(BasicTypePrinter()))
        result = printer.print(source)
        self.assertEqual(result, "const unsigned short test_var")

    def test_print_global_variable(self):
        source = GlobalVariable.create_default()
        source.name = "test_var"
        source.type = TypeExpression.create_default()
        source.type.modification |= TypeModification.CONST
        source.type.details = BasicType.U_SHORT
        printer = GlobalVariablePrinter(TypeExpressionPrinter(BasicTypePrinter()))
        result = printer.print(source)
        self.assertEqual(result, "const unsigned short test_var;\n")

    def test_print_variable_with_default_value(self):
        source = Variable.create_default()
        source.name = "test_var"
        source.type = TypeExpression.create_default()
        source.type.modification |= TypeModification.CONST
        source.type.details = BasicType.U_SHORT
        source.default_value = "(unsigned short)56.7f"
        printer = VariablePrinter(TypeExpressionPrinter(BasicTypePrinter()))
        result = printer.print(source)
        self.assertEqual(result, "const unsigned short test_var = (unsigned short)56.7f")

    def test_print_variable_array(self):
        source = Variable.create_default()
        source.name = "test_var"
        source.type = TypeExpression.create_default()
        source.type.modification |= TypeModification.ARRAY
        source.type.details = BasicType.U_SHORT
        source.default_value = "{5}"
        printer = VariablePrinter(TypeExpressionPrinter(BasicTypePrinter()))
        result = printer.print(source)
        self.assertEqual(result, "unsigned short test_var[] = {5}")

    def test_print_variable_function_pointer(self):
        printer = CodePrinter()
        printer.register(FunctionTypePrinter, FunctionType)
        printer.register(VariablePrinter, Variable)
        printer.register(BasicTypePrinter, BasicType)
        printer.register(TypeExpressionPrinter, TypeExpression)
        printer.register(GlobalVariablePrinter, GlobalVariable)

        details_type = FunctionType()
        details_type.return_type = TypeExpression.create_default()
        details_type.return_type.details = BasicType.FLOAT
        details_type.arguments = [TypeExpression.create_default(), TypeExpression.create_default()]
        details_type.arguments[0].details = BasicType.DOUBLE
        details_type.arguments[0].modification |= TypeModification.POINTER
        details_type.arguments[1].details = BasicType.CHAR

        with self.subTest("Variable"):
            source = Variable.create_default()
            source.name = "test_var"
            source.type = TypeExpression.create_default()
            source.type.modification \
                |= TypeModification.ARRAY(["20"]) | TypeModification.POINTER | TypeModification.CONST
            source.type.details = details_type
            result = printer.print(source)
            self.assertEqual(result, "float (const *test_var[20])(double*, char)")

        with self.subTest("Global variable"):
            source = GlobalVariable.create_default()
            source.name = "test_var"
            source.type = TypeExpression.create_default()
            source.type.modification \
                |= TypeModification.ARRAY(["20"]) | TypeModification.POINTER | TypeModification.CONST
            source.type.details = details_type
            result = printer.print(source)
            self.assertEqual(result, "float (const *test_var[20])(double*, char);\n")
