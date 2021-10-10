import unittest
from devana.code_generation.printers.default.functionprinter import FunctionPrinter
from devana.code_generation.printers.default.variableprinter import VariablePrinter
from devana.code_generation.printers.default.basictypeprinter import BasicTypePrinter
from devana.code_generation.printers.default.typeexpressionprinter import TypeExpressionPrinter
from devana.code_generation.printers.default.enumprinter import EnumPrinter
from devana.code_generation.printers.default.namespaceprinter import NamespacePrinter
from devana.code_generation.printers.codeprinter import CodePrinter
from devana.syntax_abstraction.functioninfo import FunctionInfo
from devana.syntax_abstraction.typeexpression import TypeModification, TypeExpression, BasicType
from devana.syntax_abstraction.variable import Variable
from devana.syntax_abstraction.namespaceinfo import NamespaceInfo
from devana.syntax_abstraction.enuminfo import EnumInfo


class TestNamespaceContent(unittest.TestCase):

    def setUp(self):
        printer = CodePrinter()
        printer.register(FunctionPrinter, FunctionInfo)
        printer.register(VariablePrinter, Variable)
        printer.register(BasicTypePrinter, BasicType)
        printer.register(TypeExpressionPrinter, TypeExpression)
        printer.register(VariablePrinter, FunctionInfo.Argument)
        printer.register(EnumPrinter, EnumInfo)
        printer.register(NamespacePrinter, NamespaceInfo)
        self.printer: CodePrinter = printer

    def test_namespace_definition_basic(self):
        namespace = NamespaceInfo()
        namespace.name = "TestNamespace"
        namespace.content = []
        function = FunctionInfo()
        function.name = "foo"
        function.return_type = TypeExpression()
        function.return_type.details = BasicType.FLOAT
        namespace.content.append(function)
        function = FunctionInfo()
        function.name = "bar"
        function.return_type = TypeExpression()
        function.return_type.details = BasicType.DOUBLE
        function.arguments = [FunctionInfo.Argument()]
        function.arguments[0].name = "a"
        function.arguments[0].type = TypeExpression()
        function.arguments[0].type.details = BasicType.CHAR
        function.arguments[0].type.modification |= TypeModification.CONST
        namespace.content.append(function)
        result = self.printer.print(namespace)
        self.assertEqual("namespace TestNamespace\n{\n    float foo();\n    double bar(const char a);\n}\n", result)

    def test_namespace_nested(self):
        namespace = NamespaceInfo()
        namespace.name = "TestNamespace"
        namespace.content = []
        function = FunctionInfo()
        function.name = "foo"
        function.return_type = TypeExpression()
        function.return_type.details = BasicType.FLOAT
        namespace.content.append(function)

        nested_namespace = NamespaceInfo()
        nested_namespace.name = "TestNested"
        function = FunctionInfo()
        function.name = "foo2"
        function.return_type = TypeExpression()
        function.return_type.details = BasicType.BOOL
        function.body = "return true;"
        nested_namespace.content = [function]
        namespace.content.append(nested_namespace)

        function = FunctionInfo()
        function.name = "bar"
        function.return_type = TypeExpression()
        function.return_type.details = BasicType.DOUBLE
        function.arguments = [FunctionInfo.Argument()]
        function.arguments[0].name = "a"
        function.arguments[0].type = TypeExpression()
        function.arguments[0].type.details = BasicType.CHAR
        function.arguments[0].type.modification |= TypeModification.CONST
        namespace.content.append(function)

        result = self.printer.print(namespace)
        self.assertEqual("namespace TestNamespace\n{\n    float foo();\n    namespace TestNested\n    {\n        bool foo2()\n        {\n            return true;\n        }\n    }\n    double bar(const char a);\n}\n", result)
