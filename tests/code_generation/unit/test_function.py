import unittest
from devana.code_generation.printers.default.functionprinter import FunctionPrinter
from devana.code_generation.printers.default.variableprinter import VariablePrinter
from devana.code_generation.printers.default.basictypeprinter import BasicTypePrinter
from devana.code_generation.printers.default.typeexpressionprinter import TypeExpressionPrinter
from devana.code_generation.printers.codeprinter import CodePrinter
from devana.syntax_abstraction.functioninfo import FunctionInfo, FunctionModification
from devana.syntax_abstraction.typeexpression import TypeModification, TypeExpression, BasicType
from devana.syntax_abstraction.variable import Variable


class TestFunctionCore(unittest.TestCase):

    def setUp(self):
        printer = CodePrinter()
        printer.register(FunctionPrinter, FunctionInfo)
        printer.register(VariablePrinter, Variable)
        printer.register(BasicTypePrinter, BasicType)
        printer.register(TypeExpressionPrinter, TypeExpression)
        printer.register(VariablePrinter, FunctionInfo.Argument)
        self.printer: CodePrinter = printer

    def test_basic_function_declaration_basic(self):
        source = FunctionInfo()
        source.name = "foo"
        source.return_type = TypeExpression()
        source.return_type.details = BasicType.LONG
        arg1 = FunctionInfo.Argument()
        arg1.type = TypeExpression()
        arg1.type.details = BasicType.FLOAT
        arg1.name = "a"
        arg2 = FunctionInfo.Argument()
        arg2.type = TypeExpression()
        arg2.type.details = BasicType.INT
        arg2.type.modification = TypeModification.POINTER
        arg2.default_value = "nullptr"
        arg2.name = "b"
        source.arguments = [arg1, arg2]
        result = self.printer.print(source)
        self.assertEqual(result, "long foo(float a, int* b = nullptr);\n")

    def test_basic_function_declaration_mods_basic(self):
        source = FunctionInfo()
        source.name = "foo"
        source.return_type = TypeExpression()
        source.return_type.details = BasicType.LONG
        arg1 = FunctionInfo.Argument()
        arg1.type = TypeExpression()
        arg1.type.details = BasicType.FLOAT
        arg1.name = "a"
        arg2 = FunctionInfo.Argument()
        arg2.type = TypeExpression()
        arg2.type.details = BasicType.INT
        arg2.name = "b"
        arg2.type.modification = TypeModification.POINTER
        arg2.default_value = "nullptr"
        source.arguments = [arg1, arg2]
        with self.subTest("static"):
            source.modification = FunctionModification.STATIC
            result = self.printer.print(source)
            self.assertEqual(result, "static long foo(float a, int* b = nullptr);\n")
        with self.subTest("inline"):
            source.modification = FunctionModification.INLINE
            result = self.printer.print(source)
            self.assertEqual(result, "inline long foo(float a, int* b = nullptr);\n")
        with self.subTest("constexpr"):
            source.modification = FunctionModification.CONSTEXPR
            result = self.printer.print(source)
            self.assertEqual(result, "constexpr long foo(float a, int* b = nullptr);\n")
        with self.subTest("const"):
            source.modification = FunctionModification.CONST
            result = self.printer.print(source)
            self.assertEqual(result, "long foo(float a, int* b = nullptr) const;\n")
        with self.subTest("volatile"):
            source.modification = FunctionModification.VOLATILE
            result = self.printer.print(source)
            self.assertEqual(result, "long foo(float a, int* b = nullptr) volatile;\n")
        with self.subTest("default"):
            source.modification = FunctionModification.DEFAULT
            result = self.printer.print(source)
            self.assertEqual(result, "long foo(float a, int* b = nullptr) = default;\n")
        with self.subTest("delete"):
            source.modification = FunctionModification.DELETE
            result = self.printer.print(source)
            self.assertEqual(result, "long foo(float a, int* b = nullptr) = delete;\n")
        with self.subTest("pure virtual"):
            source.modification = FunctionModification.PURE_VIRTUAL
            result = self.printer.print(source)
            self.assertEqual(result, "virtual long foo(float a, int* b = nullptr) = 0;\n")
        with self.subTest("explicit"):
            source.modification = FunctionModification.EXPLICIT
            result = self.printer.print(source)
            self.assertEqual(result, "long foo(float a, int* b = nullptr);\n")
        with self.subTest("override"):
            source.modification = FunctionModification.OVERRIDE
            result = self.printer.print(source)
            self.assertEqual(result, "long foo(float a, int* b = nullptr);\n")
        with self.subTest("virtual"):
            source.modification = FunctionModification.VIRTUAL
            result = self.printer.print(source)
            self.assertEqual(result, "long foo(float a, int* b = nullptr);\n")
        with self.subTest("final"):
            source.modification = FunctionModification.FINAL
            result = self.printer.print(source)
            self.assertEqual(result, "long foo(float a, int* b = nullptr);\n")

    def test_basic_function_definition(self):
        source = FunctionInfo()
        source.name = "foo"
        source.return_type = TypeExpression()
        source.return_type.details = BasicType.LONG
        arg1 = FunctionInfo.Argument()
        arg1.type = TypeExpression()
        arg1.type.details = BasicType.FLOAT
        arg1.name = "a"
        arg2 = FunctionInfo.Argument()
        arg2.type = TypeExpression()
        arg2.type.details = BasicType.INT
        arg2.type.modification = TypeModification.POINTER
        arg2.name = "b"
        arg2.default_value = "nullptr"
        source.arguments = [arg1, arg2]
        source.body = "float c = a * *b;\nif(c > 10.0f)\n    c *=0.5f;\nreturn c;"
        result = self.printer.print(source)
        self.assertEqual(result, """long foo(float a, int* b = nullptr)\n{\n    float c = a * *b;\n    if(c > 10.0f)\n        c *=0.5f;\n    return c;\n}\n""")
