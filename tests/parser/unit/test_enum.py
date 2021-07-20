import unittest
import clang.cindex
import clang
import sys
from tests.helpers import find_by_name
from devana.syntax_abstraction.typeexpression import BasicType
from devana.syntax_abstraction.enuminfo import EnumInfo


class TestEnum(unittest.TestCase):

    def setUp(self):
        index = clang.cindex.Index.create()
        self.cursor = index.parse(sys.path[0] + r"/source_files/enum.hpp").cursor

    def test_enum_value(self):
        expected_values = (
            ("VALUE_TEST_1", 0, True),
            ("VALUE_TEST_2", 1, True),
            ("VALUE_TEST_3", 100, False),
            ("VALUE_TEST_4", 101, True),
            ("VALUE_TEST_5", 0xdf, False),
            ("VALUE_TEST_6", 0xdf + 1, True),
            ("VALUE_TEST_7", 0xdf + 2, True),
        )
        node = find_by_name(self.cursor, "TestEnum")
        result = EnumInfo(node)
        self.assertEqual(result.name, "TestEnum")
        self.assertEqual(result.namespace, "TestEnum")
        self.assertFalse(result.is_scoped)
        self.assertEqual(result.prefix, None)
        # windows vs linux compatibility:
        self.assertTrue(result.numeric_type == BasicType.U_INT or result.numeric_type == BasicType.INT)
        values = result.values
        self.assertEqual(len(values), 7)
        for i in range(len(expected_values)):
            self.assertEqual(expected_values[i][0], values[i].name)
            self.assertEqual(expected_values[i][1], values[i].value)
            self.assertEqual(expected_values[i][2], values[i].is_default)

    def test_enum_class(self):
        expected_values = (
            ("VALUE_TEST_1", 0, True),
            ("VALUE_TEST_2", 1, True),
            ("VALUE_TEST_3", 100, False),
            ("VALUE_TEST_4", 101, True),
            ("VALUE_TEST_5", 0xdf, False),
            ("VALUE_TEST_6", 0xdf + 1, True),
            ("VALUE_TEST_7", 0xdf + 2, True),
        )
        node = find_by_name(self.cursor, "TestEnumClass")
        result = EnumInfo(node)
        self.assertEqual(result.name, "TestEnumClass")
        self.assertTrue(result.is_scoped)
        self.assertEqual(result.prefix, "class")
        self.assertEqual(result.numeric_type, BasicType.INT)
        values = result.values
        self.assertEqual(len(values), 7)
        for i in range(len(expected_values)):
            self.assertEqual(expected_values[i][0], values[i].name)
            self.assertEqual(expected_values[i][1], values[i].value)
            self.assertEqual(expected_values[i][2], values[i].is_default)

    def test_enum_struct(self):
        expected_values = (
            ("NUM_VALUE_TEST_1", 0, True),
            ("NUM_VALUE_TEST_2", 97, False),  # ASCII value for a is 97
            ("NUM_VALUE_TEST_3", 98, True),
        )
        node = find_by_name(self.cursor, "TestEnumNumber")
        result = EnumInfo(node)
        self.assertEqual(result.name, "TestEnumNumber")
        self.assertFalse(result.is_scoped)
        self.assertTrue(result.prefix is None)
        self.assertEqual(result.numeric_type, BasicType.CHAR)
        values = result.values
        self.assertEqual(len(values), 3)
        for i in range(len(expected_values)):
            self.assertEqual(expected_values[i][0], values[i].name)
            self.assertEqual(expected_values[i][1], values[i].value)
            self.assertEqual(expected_values[i][2], values[i].is_default,)




