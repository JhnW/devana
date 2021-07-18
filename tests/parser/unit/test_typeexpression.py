import unittest
import clang.cindex
import clang
import sys
from tests.helpers import find_by_name, stub_lexicon
from devana.syntax_abstraction.typeexpression import TypeExpression, BasicType, TypeModification
from devana.syntax_abstraction.functioninfo import FunctionInfo
from devana.syntax_abstraction.organizers.sourcefile import SourceFile


class TestTypeExpressionBasic(unittest.TestCase):

    def setUp(self):
        index = clang.cindex.Index.create()
        self.cursor = index.parse(sys.path[0] + r"/source_files/core_types.hpp").cursor

    def test_basic_types(self):
        cases = (
            ("common_integer", "int", BasicType.INT),
            ("common_u_integer", "unsigned int", BasicType.U_INT),
            ("common_short", "short", BasicType.SHORT),
            ("common_u_short", "unsigned short", BasicType.U_SHORT),
            ("common_char", "char", BasicType.CHAR),
            ("common_u_char", "unsigned char", BasicType.U_CHAR),
            ("common_long", "long", BasicType.LONG),
            ("common_u_long", "unsigned long", BasicType.U_LONG),
            ("common_long_long", "long long", BasicType.LONG_LONG),
            ("common_u_long_long", "unsigned long long", BasicType.U_LONG_LONG),
            ("common_bool", "bool", BasicType.BOOL),
            ("common_float", "float", BasicType.FLOAT),
            ("common_double", "double", BasicType.DOUBLE),
            ("common_long_double", "long double", BasicType.LONG_DOUBLE)
        )

        for c in cases:
            with self.subTest(c[0]):
                node = find_by_name(self.cursor, c[0])
                result = TypeExpression(node)
                name = c[1]
                self.assertEqual(result.name, name)
                self.assertEqual(len(result.namespaces), 0)
                self.assertEqual(result.template_arguments, None)
                self.assertFalse(result.is_generic)
                self.assertEqual(result.details, c[2])
                self.assertNotEqual(result.text_source, None)
                self.assertEqual(result.parent, None)
                self.assertEqual(result.modification, TypeModification.NONE)

    def test_const_types(self):
        cases = (
            ("const_integer", "int", BasicType.INT),
            ("const_u_integer", "unsigned int", BasicType.U_INT),
            ("const_short", "short", BasicType.SHORT),
            ("const_u_short", "unsigned short", BasicType.U_SHORT),
            ("const_char", "char", BasicType.CHAR),
            ("const_u_char", "unsigned char", BasicType.U_CHAR),
            ("const_long", "long", BasicType.LONG),
            ("const_u_long", "unsigned long", BasicType.U_LONG),
            ("const_long_long", "long long", BasicType.LONG_LONG),
            ("const_u_long_long", "unsigned long long", BasicType.U_LONG_LONG),
            ("const_bool", "bool", BasicType.BOOL),
            ("const_float", "float", BasicType.FLOAT),
            ("const_double", "double", BasicType.DOUBLE),
            ("const_long_double", "long double", BasicType.LONG_DOUBLE)
        )

        for c in cases:
            with self.subTest(c[0]):
                node = find_by_name(self.cursor, c[0])
                result = TypeExpression(node)
                name = "const " + c[1]
                self.assertEqual(result.name, name)
                self.assertEqual(len(result.namespaces), 0)
                self.assertEqual(result.template_arguments, None)
                self.assertFalse(result.is_generic)
                self.assertEqual(result.details, c[2])
                self.assertNotEqual(result.text_source, None)
                self.assertEqual(result.parent, None)
                self.assertTrue(result.modification.is_const)

    def test_ref_types(self):
        cases = (
            ("ref_integer", "int", BasicType.INT),
            ("ref_u_integer", "unsigned int", BasicType.U_INT),
            ("ref_short", "short", BasicType.SHORT),
            ("ref_u_short", "unsigned short", BasicType.U_SHORT),
            ("ref_char", "char", BasicType.CHAR),
            ("ref_u_char", "unsigned char", BasicType.U_CHAR),
            ("ref_long", "long", BasicType.LONG),
            ("ref_u_long", "unsigned long", BasicType.U_LONG),
            ("ref_long_long", "long long", BasicType.LONG_LONG),
            ("ref_u_long_long", "unsigned long long", BasicType.U_LONG_LONG),
            ("ref_bool", "bool", BasicType.BOOL),
            ("ref_float", "float", BasicType.FLOAT),
            ("ref_double", "double", BasicType.DOUBLE),
            ("ref_long_double", "long double", BasicType.LONG_DOUBLE)
        )

        for c in cases:
            with self.subTest(c[0]):
                node = find_by_name(self.cursor, c[0])
                result = TypeExpression(node)
                name = c[1] + "&"
                self.assertEqual(result.name, name)
                self.assertEqual(len(result.namespaces), 0)
                self.assertEqual(result.template_arguments, None)
                self.assertFalse(result.is_generic)
                self.assertEqual(result.details, c[2])
                self.assertNotEqual(result.text_source, None)
                self.assertEqual(result.parent, None)
                self.assertTrue(result.modification.is_reference)

    def test_pointer_types(self):
        cases = (
            ("ptr_integer", "int", BasicType.INT),
            ("ptr_u_integer", "unsigned int", BasicType.U_INT),
            ("ptr_short", "short", BasicType.SHORT),
            ("ptr_u_short", "unsigned short", BasicType.U_SHORT),
            ("ptr_char", "char", BasicType.CHAR),
            ("ptr_u_char", "unsigned char", BasicType.U_CHAR),
            ("ptr_long", "long", BasicType.LONG),
            ("ptr_u_long", "unsigned long", BasicType.U_LONG),
            ("ptr_long_long", "long long", BasicType.LONG_LONG),
            ("ptr_u_long_long", "unsigned long long", BasicType.U_LONG_LONG),
            ("ptr_bool", "bool", BasicType.BOOL),
            ("ptr_float", "float", BasicType.FLOAT),
            ("ptr_double", "double", BasicType.DOUBLE),
            ("ptr_long_double", "long double", BasicType.LONG_DOUBLE)
        )

        for c in cases:
            with self.subTest(c[0]):
                node = find_by_name(self.cursor, c[0])
                result = TypeExpression(node)
                name = c[1] + "*"
                self.assertEqual(result.name, name)
                self.assertEqual(len(result.namespaces), 0)
                self.assertEqual(result.template_arguments, None)
                self.assertFalse(result.is_generic)
                self.assertEqual(result.details, c[2])
                self.assertNotEqual(result.text_source, None)
                self.assertEqual(result.parent, None)
                self.assertTrue(result.modification.is_pointer)

    def test_static_types(self):
        cases = (
            ("static_integer", "int", BasicType.INT),
            ("static_u_integer", "unsigned int", BasicType.U_INT),
            ("static_short", "short", BasicType.SHORT),
            ("static_u_short", "unsigned short", BasicType.U_SHORT),
            ("static_char", "char", BasicType.CHAR),
            ("static_u_char", "unsigned char", BasicType.U_CHAR),
            ("static_long", "long", BasicType.LONG),
            ("static_u_long", "unsigned long", BasicType.U_LONG),
            ("static_long_long", "long long", BasicType.LONG_LONG),
            ("static_u_long_long", "unsigned long long", BasicType.U_LONG_LONG),
            ("static_bool", "bool", BasicType.BOOL),
            ("static_float", "float", BasicType.FLOAT),
            ("static_double", "double", BasicType.DOUBLE),
            ("static_long_double", "long double", BasicType.LONG_DOUBLE)
        )

        for c in cases:
            with self.subTest(c[0]):
                node = find_by_name(self.cursor, c[0])
                result = TypeExpression(node)
                name = "static " + c[1]
                self.assertEqual(result.name, name)
                self.assertEqual(len(result.namespaces), 0)
                self.assertEqual(result.template_arguments, None)
                self.assertFalse(result.is_generic)
                self.assertEqual(result.details, c[2])
                self.assertNotEqual(result.text_source, None)
                self.assertEqual(result.parent, None)
                self.assertTrue(result.modification.is_static)

    def test_volatile_types(self):
        cases = (
            ("volatile_integer", "int", BasicType.INT),
            ("volatile_u_integer", "unsigned int", BasicType.U_INT),
            ("volatile_short", "short", BasicType.SHORT),
            ("volatile_u_short", "unsigned short", BasicType.U_SHORT),
            ("volatile_char", "char", BasicType.CHAR),
            ("volatile_u_char", "unsigned char", BasicType.U_CHAR),
            ("volatile_long", "long", BasicType.LONG),
            ("volatile_u_long", "unsigned long", BasicType.U_LONG),
            ("volatile_long_long", "long long", BasicType.LONG_LONG),
            ("volatile_u_long_long", "unsigned long long", BasicType.U_LONG_LONG),
            ("volatile_bool", "bool", BasicType.BOOL),
            ("volatile_float", "float", BasicType.FLOAT),
            ("volatile_double", "double", BasicType.DOUBLE),
            ("volatile_long_double", "long double", BasicType.LONG_DOUBLE)
        )

        for c in cases:
            with self.subTest(c[0]):
                node = find_by_name(self.cursor, c[0])
                result = TypeExpression(node)
                name = "volatile " + c[1]
                self.assertEqual(result.name, name)
                self.assertEqual(len(result.namespaces), 0)
                self.assertEqual(result.template_arguments, None)
                self.assertFalse(result.is_generic)
                self.assertEqual(result.details, c[2])
                self.assertNotEqual(result.text_source, None)
                self.assertEqual(result.parent, None)
                self.assertTrue(result.modification.is_volatile)

    def test_mixed_types(self):
        cases = (
            ("const_ref_integer", "int", BasicType.INT),
            ("static_ptr_float", "float", BasicType.FLOAT),
            ("ptr_void", "void", BasicType.VOID),
        )

        c = cases[0]
        with self.subTest(c[0]):
            node = find_by_name(self.cursor, c[0])
            result = TypeExpression(node)
            name = "const " + c[1] + "&"
            self.assertEqual(result.name, name)
            self.assertEqual(len(result.namespaces), 0)
            self.assertEqual(result.template_arguments, None)
            self.assertFalse(result.is_generic)
            self.assertEqual(result.details, c[2])
            self.assertNotEqual(result.text_source, None)
            self.assertEqual(result.parent, None)
            self.assertTrue(result.modification.is_const)
            self.assertTrue(result.modification.is_reference)

        c = cases[1]
        with self.subTest(c[0]):
            node = find_by_name(self.cursor, c[0])
            result = TypeExpression(node)
            name = "static " + c[1] + "*"
            self.assertEqual(result.name, name)
            self.assertEqual(len(result.namespaces), 0)
            self.assertEqual(result.template_arguments, None)
            self.assertFalse(result.is_generic)
            self.assertEqual(result.details, c[2])
            self.assertNotEqual(result.text_source, None)
            self.assertEqual(result.parent, None)
            self.assertTrue(result.modification.is_static)
            self.assertTrue(result.modification.is_pointer)

        c = cases[2]
        with self.subTest(c[0]):
            node = find_by_name(self.cursor, c[0])
            result = TypeExpression(node)
            name = c[1] + "*"
            self.assertEqual(result.name, name)
            self.assertEqual(len(result.namespaces), 0)
            self.assertEqual(result.template_arguments, None)
            self.assertFalse(result.is_generic)
            self.assertEqual(result.details, c[2])
            self.assertNotEqual(result.text_source, None)
            self.assertEqual(result.parent, None)
            self.assertTrue(result.modification.is_pointer)

    def test_td_type_t_types(self):
        cases = (
            ("unknown_int64", "int64_t"),
            ("unknown_u_int64", "uint64_t"),
            ("unknown_int32", "int32_t"),
            ("unknown_u_int32", "uint32_t"),
            ("unknown_int16", "int16_t"),
            ("unknown_u_int16", "uint16_t"),
            ("unknown_int8", "int8_t"),
            ("unknown_u_int8", "uint8_t")
        )

        for c in cases:
            with self.subTest(c[0]):
                node = find_by_name(self.cursor, c[0])
                result = TypeExpression(node)
                name = c[1]
                self.assertEqual(result.name, name)
                self.assertEqual(len(result.namespaces), 0)
                self.assertEqual(result.template_arguments, None)
                self.assertFalse(result.is_generic)
                self.assertEqual(result.details.name, c[1])
                self.assertNotEqual(result.text_source, None)
                self.assertEqual(result.parent, None)
                self.assertEqual(result.modification, TypeModification.NONE)

    def test_modification_std_type_t_types(self):

        with self.subTest("unknown_const_u_int8"):
            node = find_by_name(self.cursor, "unknown_const_u_int8")
            result = TypeExpression(node)
            self.assertEqual(result.name, "const uint8_t")
            self.assertEqual(len(result.namespaces), 0)
            self.assertEqual(result.template_arguments, None)
            self.assertFalse(result.is_generic)
            self.assertEqual(result.details.name, "uint8_t")
            self.assertNotEqual(result.text_source, None)
            self.assertEqual(result.parent, None)
            self.assertTrue(result.modification.is_const)

        with self.subTest("unknown_const_ref_int8"):
            node = find_by_name(self.cursor, "unknown_const_ref_int8")
            result = TypeExpression(node)
            self.assertEqual(result.name, "const int8_t&")
            self.assertEqual(len(result.namespaces), 0)
            self.assertEqual(result.template_arguments, None)
            self.assertFalse(result.is_generic)
            self.assertEqual(result.details.name, "int8_t")
            self.assertNotEqual(result.text_source, None)
            self.assertEqual(result.parent, None)
            self.assertTrue(result.modification.is_const)
            self.assertTrue(result.modification.is_reference)

        with self.subTest("unknown_ptr_int16"):
            node = find_by_name(self.cursor, "unknown_ptr_int16")
            result = TypeExpression(node)
            self.assertEqual(result.name, "int16_t*")
            self.assertEqual(len(result.namespaces), 0)
            self.assertEqual(result.template_arguments, None)
            self.assertFalse(result.is_generic)
            self.assertEqual(result.details.name, "int16_t")
            self.assertNotEqual(result.text_source, None)
            self.assertEqual(result.parent, None)
            self.assertTrue(result.modification.is_pointer)

        with self.subTest("unknown_static_int16"):
            node = find_by_name(self.cursor, "unknown_static_int16")
            result = TypeExpression(node)
            self.assertEqual(result.name, "static int16_t")
            self.assertEqual(len(result.namespaces), 0)
            self.assertEqual(result.template_arguments, None)
            self.assertFalse(result.is_generic)
            self.assertEqual(result.details.name, "int16_t")
            self.assertNotEqual(result.text_source, None)
            self.assertEqual(result.parent, None)
            self.assertTrue(result.modification.is_static)

    def test_custom_typedefs(self):

        with self.subTest("typedef_typechar"):
            node = find_by_name(self.cursor, "typedef_typechar")
            result = TypeExpression(node)
            self.assertEqual(result.name, "typechar")
            self.assertEqual(len(result.namespaces), 0)
            self.assertEqual(result.template_arguments, None)
            self.assertFalse(result.is_generic)
            self.assertEqual(result.details.name, "typechar")
            self.assertNotEqual(result.text_source, None)
            self.assertEqual(result.parent, None)
            self.assertEqual(result.modification, TypeModification.NONE)

        with self.subTest("typedef_const_typechar"):
            node = find_by_name(self.cursor, "typedef_const_typechar")
            result = TypeExpression(node)
            self.assertEqual(result.name, "const typechar")
            self.assertEqual(len(result.namespaces), 0)
            self.assertEqual(result.template_arguments, None)
            self.assertFalse(result.is_generic)
            self.assertEqual(result.details.name, "typechar")
            self.assertNotEqual(result.text_source, None)
            self.assertEqual(result.parent, None)
            self.assertTrue(result.modification.is_const)

        with self.subTest("typedef_static_typechar"):
            node = find_by_name(self.cursor, "typedef_static_typechar")
            result = TypeExpression(node)
            self.assertEqual(result.name, "static typechar")
            self.assertEqual(len(result.namespaces), 0)
            self.assertEqual(result.template_arguments, None)
            self.assertFalse(result.is_generic)
            self.assertEqual(result.details.name, "typechar")
            self.assertNotEqual(result.text_source, None)
            self.assertEqual(result.parent, None)
            self.assertTrue(result.modification.is_static)

    def test_namespaces_typedefs(self):

        with self.subTest("typedef_namespace_typereal"):
            node = find_by_name(self.cursor, "typedef_namespace_typereal")
            result = TypeExpression(node)
            self.assertEqual(result.name, "const typereal")
            self.assertEqual(result.template_arguments, None)
            self.assertFalse(result.is_generic)
            self.assertEqual(result.details.name, "typereal")
            self.assertNotEqual(result.text_source, None)
            self.assertEqual(result.parent, None)
            self.assertTrue(result.modification.is_const)
            self.assertEqual(result.namespaces, ["test_namespace", ])

        with self.subTest("typedef_namespace_static_nested"):
            node = find_by_name(self.cursor, "typedef_namespace_static_nested")
            result = TypeExpression(node)
            self.assertEqual(result.name, "static typeint16")
            self.assertEqual(result.template_arguments, None)
            self.assertFalse(result.is_generic)
            self.assertEqual(result.details.name, "typeint16")
            self.assertNotEqual(result.text_source, None)
            self.assertEqual(result.parent, None)
            self.assertTrue(result.modification.is_static)
            self.assertEqual(result.namespaces, ["test_namespace", "test_namespace_v2"])

        with self.subTest("typedef_namespace_depend_typereal_ptr"):
            file: SourceFile = SourceFile(self.cursor)
            result = file.content[5].content[104].type
            self.assertEqual(result.name, "depend_typereal*")
            self.assertEqual(result.template_arguments, None)
            self.assertFalse(result.is_generic)
            self.assertEqual(result.details.name, "depend_typereal")
            self.assertEqual(result.details.type_info.namespaces, ["test_namespace", ])
            self.assertNotEqual(result.text_source, None)
            self.assertTrue(result.modification.is_pointer)
            self.assertEqual(len(result.namespaces), 0)

    def test_not_allowed_mod_pointer_to_pointer(self):
        node = find_by_name(self.cursor, "tab")
        result: TypeExpression = TypeExpression(node)
        with self.assertRaises(NotImplementedError):
            print(result.modification)

    def test_not_allowed_mod_array(self):
        node = find_by_name(self.cursor, "array")
        result: TypeExpression = TypeExpression(node)
        with self.assertRaises(NotImplementedError):
            print(result.modification)
        node = find_by_name(self.cursor, "arrayofarray")
        result: TypeExpression = TypeExpression(node)
        with self.assertRaises(NotImplementedError):
            print(result.modification)
        node = find_by_name(self.cursor, "arrayGetFunction")
        result: FunctionInfo = FunctionInfo(node)
        stub_lexicon(result)
        with self.assertRaises(NotImplementedError):
            print(result.arguments[0].type.modification)

    def test_not_allowed_function_pointer(self):
        node = find_by_name(self.cursor, "callback")
        result: TypeExpression = TypeExpression(node)
        with self.assertRaises(NotImplementedError):
            print(result.modification)
