import unittest
import clang.cindex
import clang
import os
from tests.helpers import find_by_name, stub_lexicon
from devana.syntax_abstraction.typeexpression import BasicType, TypeModification
from devana.syntax_abstraction.functioninfo import FunctionInfo, FunctionModification
from devana.utility.errors import CodeError
from devana.syntax_abstraction.externc import ExternC
from devana.syntax_abstraction.organizers.sourcefile import SourceFile
from devana.syntax_abstraction.namespaceinfo import NamespaceInfo


class TestFunctionsExternSimple(unittest.TestCase):

    def setUp(self):
        index = clang.cindex.Index.create()
        self.cursor = index.parse(os.path.dirname(__file__) + r"/source_files/extern.hpp").cursor
        self.externs = list(self.cursor.get_children())

    def test_function_declaration_extern_c_one_line(self):
        c = self.externs[0]
        extern = ExternC(c)
        self.assertEqual(extern.name, 'extern "C"')
        self.assertEqual(extern.namespace, None)
        self.assertEqual(extern.allowed_namespaces, [])
        self.assertEqual(extern.text_source.text, 'extern "C" void foo()')

        self.assertEqual(len(extern.content), 1)
        self.assertEqual(type(extern.content[0]), FunctionInfo)
        function: FunctionInfo = extern.content[0]
        self.assertEqual(function.name, "foo")
        self.assertEqual(function.body, None)

    def test_function_definition_extern_c_one_line(self):
        c = self.externs[1]
        extern = ExternC(c)
        self.assertEqual(extern.name, 'extern "C"')
        self.assertEqual(extern.namespace, None)
        self.assertEqual(extern.allowed_namespaces, [])

        self.assertEqual(len(extern.content), 1)
        self.assertEqual(type(extern.content[0]), FunctionInfo)
        function: FunctionInfo = extern.content[0]
        self.assertEqual(function.name, "foo2")
        self.assertNotEqual(function.body, None)

    def test_function_definition_declaration_extern_c_multiple_lines(self):
        c = self.externs[2]
        extern = ExternC(c)
        self.assertEqual(extern.name, 'extern "C"')
        self.assertEqual(extern.namespace, None)
        self.assertEqual(extern.allowed_namespaces, [])

        self.assertEqual(len(extern.content), 2)
        self.assertEqual(type(extern.content[0]), FunctionInfo)
        self.assertEqual(type(extern.content[1]), FunctionInfo)
        function: FunctionInfo = extern.content[0]
        self.assertEqual(function.name, "foo3")
        self.assertEqual(function.body, None)
        function: FunctionInfo = extern.content[1]
        self.assertEqual(function.name, "foo4")
        self.assertNotEqual(function.body, None)

    def test_function_definition_declaration_extern_c_multiple_lines(self):
        c = self.externs[2]
        extern = ExternC(c)
        self.assertEqual(extern.name, 'extern "C"')
        self.assertEqual(extern.namespace, None)
        self.assertEqual(extern.allowed_namespaces, [])

        self.assertEqual(len(extern.content), 2)
        self.assertEqual(type(extern.content[0]), FunctionInfo)
        self.assertEqual(type(extern.content[1]), FunctionInfo)
        function: FunctionInfo = extern.content[0]
        self.assertEqual(function.name, "foo3")
        self.assertEqual(function.body, None)
        function: FunctionInfo = extern.content[1]
        self.assertEqual(function.name, "foo4")
        self.assertNotEqual(function.body, None)


class TestFunctionsExternNamespace(unittest.TestCase):

    def setUp(self):
        index = clang.cindex.Index.create()
        self.cursor = index.parse(os.path.dirname(__file__) + r"/source_files/extern.hpp").cursor
        self.file = SourceFile(self.cursor)

    def test_function_declaration_definition_extern_c_namespace(self):
        namespace: NamespaceInfo = self.file.content[3]
        self.assertEqual(len(namespace.content), 1)
        self.assertEqual(namespace.name, "ExternNamespace")
        extern: ExternC = namespace.content[0]
        self.assertEqual(type(extern), ExternC)
        self.assertEqual(len(extern.content), 1)
        function: FunctionInfo = extern.content[0]
        self.assertEqual(type(function), FunctionInfo)
        declaration: FunctionInfo = function
        definition: FunctionInfo = self.file.content[4]

        self.assertEqual(definition.definition, definition)
        self.assertEqual(declaration.definition, definition)
