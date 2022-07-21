import unittest
from devana.code_generation.printers.default.basictypeprinter import BasicTypePrinter
from devana.code_generation.printers.default.typeexpressionprinter import TypeExpressionPrinter
from devana.code_generation.printers.default.classprinter import *
from devana.code_generation.printers.codeprinter import CodePrinter
from devana.syntax_abstraction.typeexpression import TypeModification, BasicType
from devana.syntax_abstraction.classinfo import *
from devana.code_generation.stubtype import StubType
from devana.code_generation.printers.default.stubtypeprinter import StubTypePrinter


class TestStubType(unittest.TestCase):

    def setUp(self):
        printer = CodePrinter()
        printer.register(FunctionPrinter, FunctionInfo)
        printer.register(VariablePrinter, Variable)
        printer.register(BasicTypePrinter, BasicType)
        printer.register(TypeExpressionPrinter, TypeExpression)
        printer.register(MethodPrinter, MethodInfo)
        printer.register(AccessSpecifierPrinter, AccessSpecifier)
        printer.register(VariablePrinter, FunctionInfo.Argument)
        printer.register(ClassPrinter, ClassInfo)
        printer.register(FieldPrinter, FieldInfo)
        printer.register(StubTypePrinter, StubType)

        self.printer: CodePrinter = printer

    def test_function_stub_argument(self):
        source = FunctionInfo.create_default()
        source.name = "foo"
        argument = FunctionInfo.Argument()
        argument.name = "a"
        argument.default_value = 0
        argument.type = TypeExpression.create_default()
        argument.type.modification = TypeModification.CONST
        argument.type.details = StubType("size_t")
        source.arguments = [argument]
        result = self.printer.print(source)
        self.assertEqual(result, "void foo(const size_t a = 0);\n")

    def test_function_stub_return(self):
        source = FunctionInfo()
        source.name = "foo"
        source.return_type.details = StubType("std::string")
        source.return_type.modification = TypeModification.CONST | TypeModification.REFERENCE
        result = self.printer.print(source)
        self.assertEqual(result, "const std::string& foo();\n")

    def test_class_stub_field(self):
        source = ClassInfo()
        source.name = "Foo"
        field = FieldInfo()
        field.name = "a"
        field.type = TypeExpression()
        field.type.modification = TypeModification.CONST
        field.type.details = StubType("std::string")
        source.content.append(field)
        result = self.printer.print(source)
        self.assertEqual(result, "struct Foo\n{\n    const std::string a;\n};\n")
