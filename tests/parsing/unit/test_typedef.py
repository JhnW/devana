import unittest
import clang.cindex
import clang
import os
from tests.helpers import find_by_name, stub_lexicon
from devana.syntax_abstraction.typeexpression import BasicType, TypeModification
from devana.syntax_abstraction.typedefinfo import TypedefInfo
from devana.syntax_abstraction.organizers.sourcefile import SourceFile


class TestTypedefSimple(unittest.TestCase):

    def setUp(self):
        index = clang.cindex.Index.create()
        self.cursor = index.parse(os.path.dirname(__file__) + r"/source_files/simple_typedefs.hpp").cursor

    def test_pointer_typedef(self):
        node = find_by_name(self.cursor, "def_char_ptr")
        result = TypedefInfo.from_cursor(node)
        stub_lexicon(result)
        self.assertEqual(result.name, "def_char_ptr")
        self.assertEqual(result.type_info.name, "char*")
        self.assertTrue(result.type_info.modification.is_pointer)
        self.assertEqual(result.type_info.details, BasicType.CHAR)

    def test_common_typedef(self):
        node = find_by_name(self.cursor, "def_float")
        result = TypedefInfo.from_cursor(node)
        stub_lexicon(result)
        self.assertEqual(result.name, "def_float")
        self.assertEqual(result.type_info.name, "float")
        self.assertEqual(result.type_info.modification, TypeModification.NONE)
        self.assertEqual(result.type_info.details, BasicType.FLOAT)

    def test_nested_typedef(self):
        file = SourceFile(self.cursor)

        with self.subTest("nested_typedef_add_const"):
            result = file.content[2]
            self.assertEqual(result.name, "const_def_float")
            self.assertEqual(result.type_info.name, "const def_float")
            self.assertTrue(result.type_info.modification.is_const)
            self.assertEqual(result.type_info.details.name, "def_float")
            self.assertEqual(result.type_info.details.type_info.name, "float")
            self.assertEqual(result.type_info.details.type_info.modification, TypeModification.NONE)
            self.assertEqual(result.type_info.details.type_info.details, BasicType.FLOAT)

        with self.subTest("nested_typedef_add_pointer"):
            result = file.content[3]
            self.assertEqual(result.name, "ptr_def_float")
            self.assertEqual(result.type_info.name, "def_float*")
            self.assertTrue(result.type_info.modification.is_pointer)
            self.assertEqual(result.type_info.details.name, "def_float")
            self.assertEqual(result.type_info.details.type_info.name, "float")
            self.assertEqual(result.type_info.details.type_info.modification, TypeModification.NONE)
            self.assertEqual(result.type_info.details.type_info.details, BasicType.FLOAT)

        with self.subTest("nested_typedef_multiple_level"):
            result = file.content[4]
            self.assertEqual(result.name, "const_def_char_ptr")
            self.assertEqual(result.type_info.name, "const def_char_ptr")
            self.assertTrue(result.type_info.modification.is_const)
            self.assertEqual(result.type_info.details.name, "def_char_ptr")
            self.assertTrue(result.type_info.details.type_info.modification.is_pointer)
            self.assertEqual(result.type_info.details.type_info.name, "char*")
            self.assertEqual(result.type_info.details.type_info.details, BasicType.CHAR)

    def test_namespaces_typedef(self):
        file = SourceFile(self.cursor)

        with self.subTest("typereal"):
            node = find_by_name(self.cursor, "typereal")
            result = TypedefInfo.from_cursor(node)
            stub_lexicon(result)
            self.assertEqual(result.name, "typereal")
            self.assertEqual(result.type_info.name, "double")
            self.assertTrue(result.type_info.modification.is_no_modification)
            self.assertEqual(result.type_info.details, BasicType.DOUBLE)
            self.assertEqual(len(result.type_info.namespaces), 0)

        with self.subTest("typeint16"):
            node = find_by_name(self.cursor, "typeint16")
            result = TypedefInfo.from_cursor(node)
            stub_lexicon(result)
            self.assertEqual(result.name, "typeint16")
            self.assertEqual(result.type_info.name, "short")
            self.assertTrue(result.type_info.modification.is_no_modification)
            self.assertEqual(result.type_info.details, BasicType.SHORT)
            self.assertEqual(len(result.type_info.namespaces), 0)

        with self.subTest("depend_typereal"):
            result: TypedefInfo = file.content[6]
            self.assertEqual(result.name, "depend_typereal")
            self.assertEqual(result.type_info.name, "typereal")
            self.assertTrue(result.type_info.modification.is_no_modification)
            self.assertEqual(result.type_info.namespaces, ["test_namespace", ])

        with self.subTest("depend_depend_typeint16"):
            result: TypedefInfo = file.content[7]
            self.assertEqual(result.name, "depend_depend_typeint16")
            self.assertEqual(result.type_info.name, "typeint16")
            self.assertTrue(result.type_info.modification.is_no_modification)
            self.assertEqual(result.type_info.namespaces, ["test_namespace", "test_namespace_v2"])

    def test_array_typedef(self):
        node = find_by_name(self.cursor, "array_1")
        result = TypedefInfo.from_cursor(node)
        stub_lexicon(result)
        self.assertTrue(result.type_info.modification.is_array)
        self.assertEqual(result.type_info.modification.array_order, [""])

        node = find_by_name(self.cursor, "array_2")
        result = TypedefInfo.from_cursor(node)
        stub_lexicon(result)
        self.assertTrue(result.type_info.modification.is_array)
        self.assertEqual(result.type_info.modification.array_order, ["5", "12"])