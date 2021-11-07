import unittest
from devana.code_generation.printers.default.basictypeprinter import BasicTypePrinter
from devana.code_generation.printers.default.typeexpressionprinter import TypeExpressionPrinter
from devana.code_generation.printers.default.classprinter import *
from devana.code_generation.printers.default.fileprinter import FilePrinter, IncludePrinter
from devana.code_generation.printers.codeprinter import CodePrinter
from devana.syntax_abstraction.typeexpression import BasicType
from devana.syntax_abstraction.organizers.sourcefile import SourceFile, IncludeInfo
from devana.syntax_abstraction.classinfo import *


class TestFile(unittest.TestCase):

    def setUp(self):
        printer = CodePrinter()
        printer.register(FunctionPrinter, FunctionInfo)
        printer.register(MethodPrinter, MethodInfo)
        printer.register(ConstructorPrinter, ConstructorInfo)
        printer.register(DestructorPrinter, DestructorInfo)
        printer.register(AccessSpecifierPrinter, AccessSpecifier)
        printer.register(VariablePrinter, Variable)
        printer.register(BasicTypePrinter, BasicType)
        printer.register(TypeExpressionPrinter, TypeExpression)
        printer.register(IncludePrinter, IncludeInfo)
        printer.register(FilePrinter, SourceFile)
        printer.register(VariablePrinter, FunctionInfo.Argument)

        self.printer: CodePrinter = printer

    def test_standard_include(self):
        source = IncludeInfo()
        source.value = "vector"
        source.is_standard = True
        result = self.printer.print(source)
        self.assertEqual(result, '#include <vector>\n')

    def test_common_include(self):
        source = IncludeInfo()
        source.value = "foo.hpp"
        source.is_standard = False
        result = self.printer.print(source)
        self.assertEqual(result, '#include "foo.hpp"\n')

    def test_empty_file(self):
        source = SourceFile()
        result = self.printer.print(source)
        self.assertEqual(result, "\n")

    def test_includes_in_file(self):
        source = SourceFile()
        source.includes = []
        include = IncludeInfo()
        include.value = "foo.hpp"
        include.is_standard = False
        source.includes.append(include)
        include = IncludeInfo()
        include.value = "bar.h"
        include.is_standard = False
        source.includes.append(include)
        result = self.printer.print(source)
        self.assertEqual(result, '#include "foo.hpp"\n#include "bar.h"\n\n')

    def test_content_in_file(self):
        source = SourceFile()
        source.content = []
        element = FunctionInfo()
        element.name = "foo"
        element.return_type = TypeExpression()
        element.return_type.details = BasicType.FLOAT
        source.content.append(element)
        element = FunctionInfo()
        element.name = "bar"
        element.return_type = TypeExpression()
        element.return_type.details = BasicType.DOUBLE
        source.content.append(element)
        result = self.printer.print(source)
        self.assertEqual(result, 'float foo();\ndouble bar();\n\n')

    def test_content_and_include_in_file(self):
        source = SourceFile()
        source.content = []
        source.includes = []
        element = FunctionInfo()
        element.name = "foo"
        element.return_type = TypeExpression()
        element.return_type.details = BasicType.FLOAT
        source.content.append(element)
        element = FunctionInfo()
        element.name = "bar"
        element.return_type = TypeExpression()
        element.return_type.details = BasicType.DOUBLE
        source.content.append(element)
        include = IncludeInfo()
        include.value = "foo.hpp"
        include.is_standard = False
        source.includes.append(include)
        include = IncludeInfo()
        include.value = "bar.h"
        include.is_standard = False
        source.includes.append(include)
        result = self.printer.print(source)
        self.assertEqual(result, '#include "foo.hpp"\n#include "bar.h"\n\nfloat foo();\ndouble bar();\n\n')

    def test_header_guard(self):
        source = SourceFile()
        source.content = []
        source.includes = []
        element = FunctionInfo()
        element.name = "foo"
        element.return_type = TypeExpression()
        element.return_type.details = BasicType.FLOAT
        source.content.append(element)
        element = FunctionInfo()
        element.name = "bar"
        element.return_type = TypeExpression()
        element.return_type.details = BasicType.DOUBLE
        source.content.append(element)
        include = IncludeInfo()
        include.value = "foo.hpp"
        include.is_standard = False
        source.includes.append(include)
        include = IncludeInfo()
        include.value = "bar.h"
        include.is_standard = False
        source.includes.append(include)
        source.header_guard = "TEST_H"
        result = self.printer.print(source)
        expected = "#ifndef TEST_H\n"
        expected += "#define TEST_H\n"
        expected += '\n#include "foo.hpp"\n#include "bar.h"\n\nfloat foo();\ndouble bar();\n\n'
        expected += "#endif //TEST_H\n"
        self.assertEqual(result, expected)
