import unittest
import clang.cindex
import clang
import os
from devana.syntax_abstraction.organizers.sourcefile import SourceFile
from devana.syntax_abstraction.classinfo import ClassInfo, MethodInfo
from devana.syntax_abstraction.enuminfo import EnumInfo
from devana.syntax_abstraction.functioninfo import FunctionInfo
from devana.syntax_abstraction.unioninfo import UnionInfo


class TestDeclarationDefinition(unittest.TestCase):

    def setUp(self):
        index = clang.cindex.Index.create()
        self.cursor = index.parse(os.path.dirname(__file__) + r"/source_files/definition_declaration.hpp").cursor
        self.file = SourceFile.from_cursor(self.cursor)

    def test_declaration_only(self):
        with self.subTest("Enum declaration"):
            result = self.file.content[0]
            self.assertTrue(result.is_declaration)
            self.assertFalse(result.is_definition)
        with self.subTest("Class declaration"):
            result = self.file.content[1]
            self.assertTrue(result.is_declaration)
            self.assertFalse(result.is_definition)
        with self.subTest("Struct declaration"):
            result = self.file.content[2]
            self.assertTrue(result.is_declaration)
            self.assertFalse(result.is_definition)
        with self.subTest("Function declaration"):
            result = self.file.content[3]
            self.assertTrue(result.is_declaration)
            self.assertFalse(result.is_definition)
            result = self.file.content[4]
            self.assertTrue(result.is_declaration)
            self.assertFalse(result.is_definition)
        with self.subTest("Union declaration"):
            result = self.file.content[5]
            self.assertTrue(result.is_declaration)
            self.assertFalse(result.is_definition)

    def test_definition(self):
        with self.subTest("Enum declaration"):
            result = self.file.content[6]
            self.assertFalse(result.is_declaration)
            self.assertTrue(result.is_definition)
        with self.subTest("Class declaration"):
            result = self.file.content[7]
            self.assertFalse(result.is_declaration)
            self.assertTrue(result.is_definition)
        with self.subTest("Struct declaration"):
            result = self.file.content[8]
            self.assertFalse(result.is_declaration)
            self.assertTrue(result.is_definition)
        with self.subTest("Function declaration"):
            result = self.file.content[9]
            self.assertFalse(result.is_declaration)
            self.assertTrue(result.is_definition)
            result = self.file.content[10]
            self.assertFalse(result.is_declaration)
            self.assertTrue(result.is_definition)
        with self.subTest("Union declaration"):
            result = self.file.content[11]
            self.assertFalse(result.is_declaration)
            self.assertTrue(result.is_definition)

    def test_declaration_link_to_definition(self):
        with self.subTest("Enum declaration"):
            declaration: EnumInfo = self.file.content[0]
            definition: EnumInfo = self.file.content[6]
            self.assertEqual(definition.definition, definition)
            self.assertEqual(declaration.definition, definition)
        with self.subTest("Class declaration"):
            declaration: ClassInfo = self.file.content[1]
            definition: ClassInfo = self.file.content[7]
            self.assertEqual(definition.definition, definition)
            self.assertEqual(declaration.definition, definition)
        with self.subTest("Struct declaration"):
            declaration: ClassInfo = self.file.content[2]
            definition: ClassInfo = self.file.content[8]
            self.assertEqual(definition.definition, definition)
            self.assertEqual(declaration.definition, definition)
        with self.subTest("Function declaration"):
            declaration: FunctionInfo = self.file.content[3]
            definition: FunctionInfo = self.file.content[9]
            self.assertEqual(definition.definition, definition)
            self.assertEqual(declaration.definition, definition)
            self.assertEqual(len(declaration.overloading_family), 4)
            self.assertEqual(len(definition.overloading_family), 4)

            self.assertEqual(definition.overloading_family[0], definition)
            self.assertEqual(definition.overloading_family[1], self.file.content[10])
            self.assertEqual(definition.overloading_family[2], self.file.content[12])
            self.assertEqual(definition.overloading_family[3], self.file.content[13])

            declaration: FunctionInfo = self.file.content[4]
            definition: FunctionInfo = self.file.content[10]
            self.assertEqual(definition.definition, definition)
            self.assertEqual(declaration.definition, definition)

        with self.subTest("Union declaration"):
            declaration: UnionInfo = self.file.content[4]
            definition: UnionInfo = self.file.content[10]
            self.assertEqual(definition.definition, definition)
            self.assertEqual(declaration.definition, definition)

    def test_declaration_link_to_definition_in_namespace(self):
        with self.subTest("Class declaration"):
            definition: ClassInfo = self.file.content[14].content[0]
            declaration: ClassInfo = self.file.content[15]
            self.assertEqual(definition.definition, definition)
            self.assertEqual(declaration.definition, definition)
        with self.subTest("Function declaration"):
            definition: FunctionInfo = self.file.content[14].content[1]
            declaration: FunctionInfo = self.file.content[16]
            self.assertEqual(definition.definition, definition)
            self.assertEqual(declaration.definition, definition)
        with self.subTest("Function definition"):
            definition: FunctionInfo = self.file.content[17]
            declaration: FunctionInfo = self.file.content[14].content[2]
            self.assertEqual(definition.definition, definition)
            self.assertEqual(declaration.definition, definition)
        with self.subTest("Method definition"):
            declaration: MethodInfo = self.file.content[14].content[0].content[1]
            definition: MethodInfo = self.file.content[18]
            self.assertEqual(declaration.definition, definition)
            self.assertEqual(definition.definition, definition)

    def test_class_declaration_namespace_str(self):
        declaration = self.file.content[19].content[0]
        self.assertEqual(declaration.namespaces, [])
