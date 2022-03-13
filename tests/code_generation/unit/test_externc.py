import unittest
from devana.code_generation.printers.default.functionprinter import FunctionPrinter
from devana.code_generation.printers.default.variableprinter import VariablePrinter
from devana.code_generation.printers.default.basictypeprinter import BasicTypePrinter
from devana.code_generation.printers.default.namespaceprinter import NamespacePrinter
from devana.code_generation.printers.default.typeexpressionprinter import TypeExpressionPrinter
from devana.code_generation.printers.default.externcprinter import ExternCPrinter
from devana.code_generation.printers.codeprinter import CodePrinter
from devana.syntax_abstraction.functioninfo import FunctionInfo
from devana.syntax_abstraction.namespaceinfo import NamespaceInfo
from devana.syntax_abstraction.typeexpression import TypeExpression, BasicType
from devana.syntax_abstraction.variable import Variable
from devana.syntax_abstraction.externc import ExternC


class TestExternC(unittest.TestCase):

    def setUp(self):
        printer = CodePrinter()
        printer.register(FunctionPrinter, FunctionInfo)
        printer.register(VariablePrinter, Variable)
        printer.register(BasicTypePrinter, BasicType)
        printer.register(TypeExpressionPrinter, TypeExpression)
        printer.register(VariablePrinter, FunctionInfo.Argument)
        printer.register(NamespacePrinter, NamespaceInfo)
        printer.register(ExternCPrinter, ExternC)
        self.printer: CodePrinter = printer

    def test_extern_c_empty(self):
        source = ExternC()
        result = self.printer.print(source)
        self.assertEqual(result, 'extern "C"\n{\n}\n')

    def test_extern_c_one_line(self):
        source = ExternC()
        function = FunctionInfo()
        function.name = "foo"
        function.return_type = BasicType.FLOAT
        source.content.append(function)
        result = self.printer.print(source)
        self.assertEqual(result, 'extern "C" float foo();\n')

    def test_extern_c_one_line_function_body(self):
        source = ExternC()
        function = FunctionInfo()
        function.name = "foo"
        function.return_type = BasicType.FLOAT
        function.body = "return 7.6;"
        source.content.append(function)
        result = self.printer.print(source)
        self.assertEqual(result, 'extern "C" float foo()\n{\n    return 7.6;\n}\n')

    def test_extern_c_multiple_lines(self):
        source = ExternC()
        function = FunctionInfo()
        function.name = "foo"
        function.return_type = BasicType.FLOAT
        source.content.append(function)
        function = FunctionInfo()
        function.name = "bar"
        function.return_type = BasicType.INT
        function.body = "return 777+foo();"
        source.content.append(function)
        result = self.printer.print(source)
        self.assertEqual(result, 'extern "C"\n{\n    float foo();\n    int bar()\n    {\n        return 777+foo();\n  '
                                 '  }\n}\n')

    def test_extern_c_one_line_namespace_indent(self):
        namespace = NamespaceInfo()
        namespace.name = "Namespace"
        extern = ExternC()
        function = FunctionInfo()
        function.name = "foo"
        function.return_type = BasicType.FLOAT
        extern.content.append(function)
        namespace.content.append(extern)
        result = self.printer.print(namespace)
        self.assertEqual(result, 'namespace Namespace\n{\n    extern "C" float foo();\n}\n')
