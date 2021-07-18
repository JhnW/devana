import unittest
import clang.cindex
import clang
import sys
from tests.helpers import find_by_name
from devana.syntax_abstraction.typeexpression import BasicType
from devana.syntax_abstraction.namespaceinfo import NamespaceInfo
from devana.syntax_abstraction.functioninfo import FunctionInfo
from devana.syntax_abstraction.classinfo import FieldInfo, ClassInfo
from devana.syntax_abstraction.typedefinfo import TypedefInfo
from devana.syntax_abstraction.organizers.sourcefile import SourceFile


class TestNamespaces(unittest.TestCase):

    def setUp(self):
        index = clang.cindex.Index.create()
        self.cursor = index.parse(sys.path[0] + r"/source_files/namespaces.hpp").cursor

    def test_simple_namespace(self):
        node = find_by_name(self.cursor, "SimpleNamespace")
        result = NamespaceInfo(node)
        self.assertEqual(result.name, "SimpleNamespace")
        self.assertEqual(len(result.content), 1)
        func: FunctionInfo = result.content[0]
        self.assertEqual(func.name, "foo")
        self.assertEqual(len(func.arguments), 0)
        self.assertEqual(func.return_type.details, BasicType.DOUBLE)

    def test_nested_namespace(self):
        node = find_by_name(self.cursor, "NestedNamespace")
        result = NamespaceInfo(node)
        self.assertEqual(result.name, "NestedNamespace")
        self.assertEqual(len(result.content), 2)
        func: FunctionInfo = result.content[0]
        self.assertEqual(func.name, "bar")
        self.assertEqual(len(func.arguments), 0)
        self.assertEqual(func.return_type.details, BasicType.DOUBLE)
        namespace: NamespaceInfo = result.content[1]
        self.assertEqual(namespace.name, "InternalNamespace")
        self.assertEqual(len(namespace.content), 1)
        self.assertEqual(namespace.content[0].name, "bar")
        self.assertEqual(len(namespace.content[0].arguments), 0)
        self.assertEqual(namespace.content[0].return_type.details, BasicType.INT)


class TestNamespacesLexicon(unittest.TestCase):

    def setUp(self):
        index = clang.cindex.Index.create()
        self.cursor = index.parse(sys.path[0] + r"/source_files/advanced_namespace.hpp").cursor
        self.file = SourceFile(self.cursor)

    def test_function_return(self):
        result: FunctionInfo = self.file.content[2].content[2]
        with self.subTest(result.name):
            self.assertEqual(result.return_type.details, self.file.content[0].content[1].content[0])

        result: FunctionInfo = self.file.content[2].content[3]
        with self.subTest(result.name):
            self.assertEqual(result.return_type.details, self.file.content[0].content[1].content[0])

        result: FunctionInfo = self.file.content[2].content[4]
        with self.subTest(result.name):
            self.assertEqual(result.return_type.details, self.file.content[1].content[0].content[2])

        result: FunctionInfo = self.file.content[2].content[5]
        with self.subTest(result.name):
            from devana.utility.errors import ParserError
            with self.assertRaises(ParserError):
                self.assertEqual(result.return_type.details, self.file.content[1].content[2].content[1])

        result: FunctionInfo = self.file.content[2].content[6]
        with self.subTest(result.name):
            self.assertEqual(result.return_type.details, self.file.content[1].content[3])

    def test_function_argument(self):
        result: FunctionInfo = self.file.content[2].content[7]
        with self.subTest(result.name):
            self.assertEqual(len(result.arguments), 1)
            self.assertEqual(result.arguments[0].type.details, self.file.content[0].content[1].content[0])

        result: FunctionInfo = self.file.content[2].content[8]
        with self.subTest(result.name):
            self.assertEqual(len(result.arguments), 1)
            self.assertEqual(result.arguments[0].type.details, self.file.content[0].content[1].content[0])

        result: FunctionInfo = self.file.content[2].content[9]
        with self.subTest(result.name):
            self.assertEqual(len(result.arguments), 1)
            self.assertEqual(result.arguments[0].type.details, self.file.content[1].content[0].content[2])

        result: FunctionInfo = self.file.content[2].content[10]
        with self.subTest(result.name):
            self.assertEqual(len(result.arguments), 1)
            from devana.utility.errors import ParserError
            with self.assertRaises(ParserError):
                self.assertEqual(result.arguments[0].type.details, self.file.content[1].content[2].content[1])

        result: FunctionInfo = self.file.content[2].content[11]
        with self.subTest(result.name):
            self.assertEqual(len(result.arguments), 1)
            self.assertEqual(result.arguments[0].type.details, self.file.content[1].content[3])

    def test_templates(self):
        result: FunctionInfo = self.file.content[2].content[12]
        with self.subTest(result.name):
            from devana.utility.errors import ParserError
            with self.assertRaises(ParserError):
                _ = result.return_type.details
        result: FunctionInfo = self.file.content[2].content[13]
        with self.subTest(result.name):
            from devana.utility.errors import ParserError
            with self.assertRaises(ParserError):
                _ = result.arguments[0].type.details

    def test_fields(self):
        result: FieldInfo = self.file.content[2].content[14].content[0]
        with self.subTest(result.name):
            self.assertEqual(result.type.details, self.file.content[0].content[1].content[0])

        result: FieldInfo = self.file.content[2].content[14].content[1]
        with self.subTest(result.name):
            self.assertEqual(result.type.details, self.file.content[0].content[1].content[0])

        result: FieldInfo = self.file.content[2].content[14].content[2]
        with self.subTest(result.name):
            self.assertEqual(result.type.details, self.file.content[1].content[0].content[2])

        result: FieldInfo = self.file.content[2].content[14].content[3]
        with self.subTest(result.name):
            from devana.utility.errors import ParserError
            with self.assertRaises(ParserError):
                self.assertEqual(result.type.details, self.file.content[1].content[2].content[1])

        result: FieldInfo = self.file.content[2].content[14].content[4]
        with self.subTest(result.name):
            self.assertEqual(result.type.details, self.file.content[1].content[3])

    def test_typedef(self):
        result: TypedefInfo = self.file.content[2].content[15]
        with self.subTest(result.name):
            with self.subTest(result.name):
                self.assertEqual(result.type_info.details, self.file.content[0].content[1].content[0])

        result: TypedefInfo = self.file.content[2].content[16]
        with self.subTest(result.name):
            self.assertEqual(result.type_info.details, self.file.content[0].content[1].content[0])

        result: TypedefInfo = self.file.content[2].content[17]
        with self.subTest(result.name):
            self.assertEqual(result.type_info.details, self.file.content[1].content[0].content[2])

        result: TypedefInfo = self.file.content[2].content[18]
        with self.subTest(result.name):
            from devana.utility.errors import ParserError
            with self.assertRaises(ParserError):
                self.assertEqual(result.type_info.details, self.file.content[1].content[2].content[1])

        result: TypedefInfo = self.file.content[2].content[19]
        with self.subTest(result.name):
            self.assertEqual(result.type_info.details, self.file.content[1].content[3])

    def test_template_spec(self):
        result = self.file.content[2].content[21]
        self.assertEqual(len(result.template.specialisation_values), 1)
        self.assertEqual(result.template.specialisation_values[0].details, self.file.content[1].content[0])

        result = self.file.content[2].content[23]
        self.assertEqual(len(result.template.specialisation_values), 1)
        self.assertEqual(result.template.specialisation_values[0].details, self.file.content[1].content[0])

    def test_inheritance(self):
        result: ClassInfo = self.file.content[2].content[24]
        self.assertEqual(len(result.inheritance.type_parents), 1)
        self.assertEqual(result.inheritance.type_parents[0].type, self.file.content[1].content[0])

    def test_multiple_declaration(self):
        result: NamespaceInfo = self.file.content[3]
        self.assertEqual(len(result.lexicon.content), 5)

    def test_namespaces_chain(self):
        result: ClassInfo = self.file.content[0].content[1]
        lexicon = result.lexicon
        self.assertEqual(lexicon.namespaces_chain, ["foo1", "bar1"])



