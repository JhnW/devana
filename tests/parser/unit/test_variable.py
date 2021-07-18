import unittest
import clang.cindex
import clang
import sys
from tests.helpers import find_by_name, stub_lexicon
from devana.syntax_abstraction.typeexpression import BasicType, TypeModification
from devana.syntax_abstraction.variable import Variable, GlobalVariable


class TestVariableBasic(unittest.TestCase):

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
                result = Variable(node)
                stub_lexicon(result)
                self.assertEqual(result.name, c[0])
                result = result.type
                name = c[1]
                self.assertEqual(result.name, name)
                self.assertEqual(len(result.namespaces), 0)
                self.assertEqual(result.template_arguments, None)
                self.assertFalse(result.is_generic)
                self.assertEqual(result.details, c[2])
                self.assertNotEqual(result.text_source, None)
                self.assertNotEqual(result.parent, None)
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
                result = Variable(node)
                stub_lexicon(result)
                self.assertEqual(result.name, c[0])
                result = result.type
                name = "const " + c[1]
                self.assertEqual(result.name, name)
                self.assertEqual(len(result.namespaces), 0)
                self.assertEqual(result.template_arguments, None)
                self.assertFalse(result.is_generic)
                self.assertEqual(result.details, c[2])
                self.assertNotEqual(result.text_source, None)
                self.assertNotEqual(result.parent, None)
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
                result = Variable(node)
                stub_lexicon(result)
                self.assertEqual(result.name, c[0])
                result = result.type
                name = c[1]+"&"
                self.assertEqual(result.name, name)
                self.assertEqual(len(result.namespaces), 0)
                self.assertEqual(result.template_arguments, None)
                self.assertFalse(result.is_generic)
                self.assertEqual(result.details, c[2])
                self.assertNotEqual(result.text_source, None)
                self.assertNotEqual(result.parent, None)
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
                result = Variable(node)
                stub_lexicon(result)
                self.assertEqual(result.name, c[0])
                result = result.type
                name = c[1]+"*"
                self.assertEqual(result.name, name)
                self.assertEqual(len(result.namespaces), 0)
                self.assertEqual(result.template_arguments, None)
                self.assertFalse(result.is_generic)
                self.assertEqual(result.details, c[2])
                self.assertNotEqual(result.text_source, None)
                self.assertNotEqual(result.parent, None)
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
                result = Variable(node)
                stub_lexicon(result)
                self.assertEqual(result.name, c[0])
                result = result.type
                name = "static " + c[1]
                self.assertEqual(result.name, name)
                self.assertEqual(len(result.namespaces), 0)
                self.assertEqual(result.template_arguments, None)
                self.assertFalse(result.is_generic)
                self.assertEqual(result.details, c[2])
                self.assertNotEqual(result.text_source, None)
                self.assertNotEqual(result.parent, None)
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
                result = Variable(node)
                stub_lexicon(result)
                self.assertEqual(result.name, c[0])
                result = result.type
                name = "volatile " + c[1]
                self.assertEqual(result.name, name)
                self.assertEqual(len(result.namespaces), 0)
                self.assertEqual(result.template_arguments, None)
                self.assertFalse(result.is_generic)
                self.assertEqual(result.details, c[2])
                self.assertNotEqual(result.text_source, None)
                self.assertNotEqual(result.parent, None)
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
            result = Variable(node)
            stub_lexicon(result)
            self.assertEqual(result.name, c[0])
            result = result.type
            name = "const " + c[1]+"&"
            self.assertEqual(result.name, name)
            self.assertEqual(len(result.namespaces), 0)
            self.assertEqual(result.template_arguments, None)
            self.assertFalse(result.is_generic)
            self.assertEqual(result.details, c[2])
            self.assertNotEqual(result.text_source, None)
            self.assertNotEqual(result.parent, None)
            self.assertTrue(result.modification.is_const)
            self.assertTrue(result.modification.is_reference)

        c = cases[1]
        with self.subTest(c[0]):
            node = find_by_name(self.cursor, c[0])
            result = Variable(node)
            stub_lexicon(result)
            self.assertEqual(result.name, c[0])
            result = result.type
            name = "static " + c[1]+"*"
            self.assertEqual(result.name, name)
            self.assertEqual(len(result.namespaces), 0)
            self.assertEqual(result.template_arguments, None)
            self.assertFalse(result.is_generic)
            self.assertEqual(result.details, c[2])
            self.assertNotEqual(result.text_source, None)
            self.assertNotEqual(result.parent, None)
            self.assertTrue(result.modification.is_static)
            self.assertTrue(result.modification.is_pointer)

        c = cases[2]
        with self.subTest(c[0]):
            node = find_by_name(self.cursor, c[0])
            result = Variable(node)
            stub_lexicon(result)
            self.assertEqual(result.name, c[0])
            result = result.type
            name = c[1]+"*"
            self.assertEqual(result.name, name)
            self.assertEqual(len(result.namespaces), 0)
            self.assertEqual(result.template_arguments, None)
            self.assertFalse(result.is_generic)
            self.assertEqual(result.details, c[2])
            self.assertNotEqual(result.text_source, None)
            self.assertNotEqual(result.parent, None)
            self.assertTrue(result.modification.is_pointer)

    def test_global_variable(self):
        node = find_by_name(self.cursor, "global_var")
        result = GlobalVariable(node)
        stub_lexicon(result)
        with self.subTest(result.name):
            self.assertEqual(result.name, "global_var")
            self.assertEqual(result.type.details, BasicType.CHAR)
            self.assertTrue(result.type.modification.is_pointer)
            self.assertFalse(result.type.modification.is_static)
            self.assertEqual(result.default_value, None)
        node = find_by_name(self.cursor, "constexpr_global_var")
        result = GlobalVariable(node)
        stub_lexicon(result)
        with self.subTest(result.name):
            self.assertEqual(result.name, "constexpr_global_var")
            self.assertEqual(result.type.details, BasicType.INT)
            self.assertTrue(result.type.modification.is_constexpr)
            self.assertFalse(result.type.modification.is_static)
            self.assertEqual(result.default_value, "77")
