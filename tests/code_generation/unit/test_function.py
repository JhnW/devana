import unittest
from devana.code_generation.printers.default.functionprinter import FunctionPrinter, ArgumentPrinter
from devana.code_generation.printers.default.variableprinter import VariablePrinter
from devana.code_generation.printers.default.basictypeprinter import BasicTypePrinter
from devana.code_generation.printers.default.typeexpressionprinter import TypeExpressionPrinter
from devana.code_generation.printers.default.templateparameterprinter import TemplateParameterPrinter
from devana.code_generation.printers.default.typeexpressionprinter import GenericTypeParameterPrinter
from devana.code_generation.printers.codeprinter import CodePrinter
from devana.syntax_abstraction.functioninfo import FunctionInfo, FunctionModification
from devana.syntax_abstraction.typeexpression import TypeModification, TypeExpression, BasicType
from devana.syntax_abstraction.variable import Variable
from devana.syntax_abstraction.templateinfo import TemplateInfo, GenericTypeParameter


class TestFunctionCore(unittest.TestCase):

    def setUp(self):
        printer = CodePrinter()
        printer.register(FunctionPrinter, FunctionInfo)
        printer.register(VariablePrinter, Variable)
        printer.register(BasicTypePrinter, BasicType)
        printer.register(TypeExpressionPrinter, TypeExpression)
        printer.register(ArgumentPrinter, FunctionInfo.Argument)
        self.printer: CodePrinter = printer

    def test_basic_function_declaration_basic(self):
        source = FunctionInfo.create_default()
        source.name = "foo"
        source.return_type = TypeExpression.create_default()
        source.return_type.details = BasicType.LONG
        arg1 = FunctionInfo.Argument()
        arg1.type = TypeExpression.create_default()
        arg1.type.details = BasicType.FLOAT
        arg1.name = "a"
        arg2 = FunctionInfo.Argument()
        arg2.type = TypeExpression.create_default()
        arg2.type.details = BasicType.INT
        arg2.type.modification = TypeModification.POINTER
        arg2.default_value = "nullptr"
        arg2.name = "b"
        source.arguments = [arg1, arg2]
        result = self.printer.print(source)
        self.assertEqual(result, "long foo(float a, int* b = nullptr);\n")

    def test_basic_function_declaration_mods_basic(self):
        source = FunctionInfo.create_default()
        source.name = "foo"
        source.return_type = TypeExpression.create_default()
        source.return_type.details = BasicType.LONG
        arg1 = FunctionInfo.Argument()
        arg1.type = TypeExpression.create_default()
        arg1.type.details = BasicType.FLOAT
        arg1.name = "a"
        arg2 = FunctionInfo.Argument()
        arg2.type = TypeExpression.create_default()
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
        with self.subTest("consteval"):
            source.modification = FunctionModification.CONSTEVAL
            result = self.printer.print(source)
            self.assertEqual(result, "consteval long foo(float a, int* b = nullptr);\n")
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
        with self.subTest("noexcept"):
            source.modification = FunctionModification.NOEXCEPT
            result = self.printer.print(source)
            self.assertEqual(result, "long foo(float a, int* b = nullptr) noexcept;\n")

    def test_basic_function_definition(self):
        source = FunctionInfo.create_default()
        source.name = "foo"
        source.return_type = TypeExpression.create_default()
        source.return_type.details = BasicType.LONG
        arg1 = FunctionInfo.Argument()
        arg1.type = TypeExpression.create_default()
        arg1.type.details = BasicType.FLOAT
        arg1.name = "a"
        arg2 = FunctionInfo.Argument()
        arg2.type = TypeExpression.create_default()
        arg2.type.details = BasicType.INT
        arg2.type.modification = TypeModification.POINTER
        arg2.name = "b"
        arg2.default_value = "nullptr"
        source.arguments = [arg1, arg2]
        source.body = "float c = a * *b;\nif(c > 10.0f)\n    c *=0.5f;\nreturn c;"
        result = self.printer.print(source)
        self.assertEqual(result,
                         """long foo(float a, int* b = nullptr)\n{\n    float c = a * *b;\n    if(c > 10.0f)\n        c *=0.5f;\n    return c;\n}\n""")

    def test_function_namespace(self):
        source = FunctionInfo.create_default()
        source.namespaces = ["Test1", "Test2"]
        source.name = "foo"
        source.return_type = TypeExpression.create_default()
        source.return_type.details = BasicType.FLOAT
        result = self.printer.print(source)
        self.assertEqual(result, "float Test1::Test2::foo();\n")

    def test_function_body_with_brace(self):
        source = FunctionInfo.create_default()
        source.name = "foo"
        source.return_type.details = BasicType.FLOAT
        source.body = "{\nreturn 6.7;\n}"
        result = self.printer.print(source)
        self.assertEqual(result, "float foo()\n{\n    return 6.7;\n}\n")


class TestFunctionTemplate(unittest.TestCase):

    def setUp(self):
        printer = CodePrinter()
        printer.register(FunctionPrinter, FunctionInfo)
        printer.register(VariablePrinter, Variable)
        printer.register(BasicTypePrinter, BasicType)
        printer.register(TypeExpressionPrinter, TypeExpression)
        printer.register(VariablePrinter, FunctionInfo.Argument)
        printer.register(TemplateParameterPrinter, TemplateInfo.TemplateParameter)
        printer.register(GenericTypeParameterPrinter, GenericTypeParameter)
        self.printer: CodePrinter = printer

    def test_function_simple_template(self):
        source = FunctionInfo.create_default()
        source.name = "foo"
        source.return_type = TypeExpression.create_default()
        source.return_type.details = BasicType.FLOAT
        source.template = TemplateInfo()
        template_param = TemplateInfo.TemplateParameter()
        template_param.name = "T"
        source.template.parameters = [template_param]
        result = self.printer.print(source)
        self.assertEqual(result, "template<typename T>\nfloat foo();\n")

    def test_function_empty_template(self):
        source = FunctionInfo.create_default()
        source.name = "foo"
        source.return_type = TypeExpression.create_default()
        source.return_type.details = BasicType.FLOAT
        source.template = TemplateInfo()
        result = self.printer.print(source)
        self.assertEqual(result, "template<>\nfloat foo();\n")

    def test_function_template_argument(self):
        source = FunctionInfo.create_default()
        source.name = "foo"
        source.return_type = TypeExpression.create_default()
        source.return_type.details = BasicType.FLOAT
        source.template = TemplateInfo()
        template_param = TemplateInfo.TemplateParameter()
        template_param.name = "T"
        source.template.parameters = [template_param]
        argument = FunctionInfo.Argument()
        argument.type = TypeExpression.create_default()
        argument.type.details = GenericTypeParameter("T")
        argument.type.modification = TypeModification.CONST
        argument.name = "a"
        source.arguments = [argument]
        result = self.printer.print(source)
        self.assertEqual(result, "template<typename T>\nfloat foo(const T a);\n")

    def test_function_template_return_value(self):
        source = FunctionInfo.create_default()
        source.name = "foo"
        source.template = TemplateInfo()
        template_param = TemplateInfo.TemplateParameter()
        template_param.name = "T"
        source.template.parameters = [template_param]
        source.return_type = TypeExpression.create_default()
        source.return_type.details = GenericTypeParameter("T")
        source.return_type.modification = TypeModification.POINTER
        result = self.printer.print(source)
        self.assertEqual(result, "template<typename T>\nT* foo();\n")

    def test_function_template_default_value(self):
        source = FunctionInfo.create_default()
        source.name = "foo"
        source.return_type = TypeExpression.create_default()
        source.return_type.details = BasicType.FLOAT
        source.template = TemplateInfo()
        template_param = TemplateInfo.TemplateParameter()
        template_param.name = "T"
        template_param.default_value = "int"
        source.template.parameters = [template_param]
        result = self.printer.print(source)
        self.assertEqual(result, "template<typename T = int>\nfloat foo();\n")

    def test_function_template_standard(self):
        source = FunctionInfo.create_default()
        source.name = "foo"
        source.return_type = TypeExpression.create_default()
        source.return_type.details = BasicType.FLOAT
        source.template = TemplateInfo()
        spec_1 = TypeExpression.create_default()
        spec_1.details = BasicType.INT
        spec_1.modification = TypeModification.REFERENCE
        spec_2 = TypeExpression.create_default()
        spec_2.details = BasicType.LONG
        spec_2.modification = TypeModification.CONST
        source.template.specialisation_values = [spec_1, spec_2]
        result = self.printer.print(source)
        self.assertEqual(result, "template<>\nfloat foo<int&,const long>();\n")

    def test_function_prefix(self):
        source = FunctionInfo.create_default()
        source.name = "foo"
        source.return_type = TypeExpression.create_default()
        source.return_type.details = BasicType.LONG
        source.prefix = "__declspec(dllexport)"
        result = self.printer.print(source)
        self.assertEqual(result, "__declspec(dllexport) long foo();\n")
