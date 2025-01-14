import unittest
from typing import List, Optional, Union
from devana.preprocessing.premade.components.executor.executable import CallFrame, Signature
from devana.preprocessing.premade.components.parser.typechecker import is_arguments_valid, is_type_valid


class TestTypeChecker(unittest.TestCase):

    def test_string(self):
        self.assertTrue(is_type_valid("string", str))

    def test_missmatch_string(self):
        self.assertFalse(is_type_valid(7, str))

    def test_int(self):
        self.assertTrue(is_type_valid(7, int))

    def test_bool_to_int(self):
        self.assertFalse(is_type_valid(7, bool))

    def test_int_to_float(self):
        self.assertTrue(is_type_valid(7, float))

    def test_float(self):
        self.assertTrue(is_type_valid(7.5, float))

    def test_bool(self):
        self.assertTrue(is_type_valid(True, bool))

    def test_missmatch_bool(self):
        self.assertFalse(is_type_valid(True, int))

    def test_optional_value(self):
        self.assertTrue(is_type_valid("test", Optional[str]))

    def test_optional_none(self):
        self.assertTrue(is_type_valid(None, Optional[str]))

    def test_optional_mismatch(self):
        self.assertFalse(is_type_valid(7, Optional[str]))

    def test_list(self):
        self.assertTrue(is_type_valid([7, 8, 9], List[int]))

    def test_list_in_list(self):
        self.assertTrue(is_type_valid([[7, 8], [9]], List[List[int]]))

    def test_list_wrong_value(self):
        self.assertFalse(is_type_valid(8, List[int]))

    def test_list_wrong_value_inside(self):
        self.assertFalse(is_type_valid([8, 9, "str"], List[int]))

    def test_simple_union(self):
        self.assertTrue(is_type_valid("str", Union[str, int]))
        self.assertTrue(is_type_valid(9, Union[str, int]))

    def test_union_mismatch(self):
        self.assertFalse(is_type_valid(True, Union[str, int]))

    def test_complex(self):
        self.assertTrue(is_type_valid([7, "str", None], List[Optional[Union[str, int]]]))


class TestArgumentValidator(unittest.TestCase):


    def test_validate_expected_empty_given_empty(self):
        given = CallFrame.Arguments([], {})
        expected = Signature.Arguments([], {})
        self.assertTrue(is_arguments_valid(given, expected))

    def test_validate_expected_default_given_empty(self):
        given = CallFrame.Arguments([], {})
        expected = Signature.Arguments([], {"test_name": str})
        self.assertTrue(is_arguments_valid(given, expected))

    def test_validate_expected_named_given_named(self):
        given = CallFrame.Arguments([], {"test_name": CallFrame.Arguments.Value("7")})
        expected = Signature.Arguments([], {"test_name": str})
        self.assertTrue(is_arguments_valid(given, expected))

    def test_validate_expected_positional_given_positional(self):
        given = CallFrame.Arguments([CallFrame.Arguments.Value("7")], {})
        expected = Signature.Arguments([str], {})
        self.assertTrue(is_arguments_valid(given, expected))

    def test_validate_expected_positional_and_named_given_positional(self):
        given = CallFrame.Arguments([CallFrame.Arguments.Value("7")], {})
        expected = Signature.Arguments([str], {})
        self.assertTrue(is_arguments_valid(given, expected))