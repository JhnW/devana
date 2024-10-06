import unittest
from devana.preprocessing.components.property.parsers.parser import ParsingBackend
from devana.preprocessing.components.property.parsers.types import *


class TestPreprocessorParsingTypesBoolean(unittest.TestCase):

    def setUp(self):
        self._parser: IParsableElement = BooleanType()

    def test_extract_true(self):
        parser = self._parser
        text = "true"
        result = parser.parse(text)
        self.assertEqual(result, True)

    def test_extract_false(self):
        parser = self._parser
        text = "false"
        result = parser.parse(text)
        self.assertEqual(result, False)

    def test_extract_incorrect(self):
        parser = self._parser
        text = "false2"
        result = parser.parse(text)
        self.assertEqual(result, ParsableElementError())

    def test_extract_two(self):
        parser = self._parser
        text = "false false"
        result = parser.parse(text)
        self.assertEqual(result, ParsableElementError())

    def test_extract_spaces(self):
        parser = self._parser
        text = " false  "
        result = parser.parse(text)
        self.assertEqual(result, False)


class TestPreprocessorParsingTypesInteger(unittest.TestCase):

    def setUp(self):
        self._parser: IParsableElement = IntegerType()

    def test_extract(self):
        parser = self._parser
        text = "78"
        result = parser.parse(text)
        self.assertEqual(result, 78)

    def test_extract_negative(self):
        parser = self._parser
        text = "-78"
        result = parser.parse(text)
        self.assertEqual(result, -78)

    def test_extract_positive(self):
        parser = self._parser
        text = "+78"
        result = parser.parse(text)
        self.assertEqual(result, 78)

    def test_extract_not_integer(self):
        parser = self._parser
        text = "ax"
        result = parser.parse(text)
        self.assertEqual(result, ParsableElementError())

    def test_extract_spaces(self):
        parser = self._parser
        text = "   56456 "
        result = parser.parse(text)
        self.assertEqual(result, 56456)


class TestPreprocessorParsingTypesFloat(unittest.TestCase):

    def setUp(self):
        self._parser: IParsableElement = FloatType()

    def test_extract(self):
        parser = self._parser
        text = "78.7456"
        result = parser.parse(text)
        self.assertEqual(result, 78.7456)

    def test_extract_simpler(self):
        parser = self._parser
        text = "78"
        result = parser.parse(text)
        self.assertEqual(result, 78)

    def test_extract_negative(self):
        parser = self._parser
        text = "-78.7456"
        result = parser.parse(text)
        self.assertEqual(result, -78.7456)

    def test_extract_positive(self):
        parser = self._parser
        text = "+78.7456"
        result = parser.parse(text)
        self.assertEqual(result, 78.7456)

    def test_spaces(self):
        parser = self._parser
        text = "  78.7456   "
        result = parser.parse(text)
        self.assertEqual(result, 78.7456)


class TestPreprocessorParsingTypesString(unittest.TestCase):

    def setUp(self):
        self._parser: IParsableElement = StringType()

    def test_extract(self):
        parser = self._parser
        text = '"test with somme data"'
        result = parser.parse(text)
        self.assertEqual(result, "test with somme data")

    def test_extract_spaces(self):
        parser = self._parser
        text = '     "test with somme data"      '
        result = parser.parse(text)
        self.assertEqual(result, "test with somme data")

    def test_extract_wrong(self):
        parser = self._parser
        text = '"test with somme data'
        result = parser.parse(text)
        self.assertEqual(result, ParsableElementError())

    def test_extract_space(self):
        parser = self._parser
        text = '  "  test with somme data  " '
        result = parser.parse(text)
        self.assertEqual(result, "  test with somme data  ")


class TestPreprocessorParsingBackendParseArgumentStructure(unittest.TestCase):

    def setUp(self):
        self._parser = ParsingBackend()
        self._parser.add_type(BooleanType())
        self._parser.add_type(StringType())
        self._parser.add_type(FloatType())

    def test_parse_stand_alone_argument(self):
        parser = self._parser
        text = "true"
        result = parser.parse_argument(text)
        self.assertEqual(result.value, True)
        self.assertEqual(result.name, None)

    def test_parse_named_argument(self):
        parser = self._parser
        text = "argument=true"
        result = parser.parse_argument(text)
        self.assertEqual(result.value, True)
        self.assertEqual(result.name, "argument")

    def test_parse_named_argument_complex(self):
        parser = self._parser
        text = " argument  = true  "
        result = parser.parse_argument(text)
        self.assertEqual(result.value, True)
        self.assertEqual(result.name, "argument")

    def test_parse_named_argument_double_eq(self):
        parser = self._parser
        text = " argument =  = true  "
        with self.assertRaises(ValueError):
            parser.parse_argument(text)

    def test_parse_named_argument_no_eq_eq(self):
        parser = self._parser
        text = " argument true  "
        with self.assertRaises(ValueError):
            parser.parse_argument(text)

    def test_parse_positional_string_without_space(self):
        parser = self._parser
        text = '"Text"'
        result = parser.parse_argument(text)
        self.assertEqual(result.value, "Text")

    def test_parse_positional_string_with_space(self):
        parser = self._parser
        text = '"Text 1"'
        result = parser.parse_argument(text)
        self.assertEqual(result.value, "Text 1")

    def test_parse_named_string_without_space(self):
        parser = self._parser
        text = 'name= "Text"'
        result = parser.parse_argument(text)
        self.assertEqual(result.value, "Text")

    def test_parse_named_string_with_space(self):
        parser = self._parser
        text = 'name= "Text 2"'
        result = parser.parse_argument(text)
        self.assertEqual(result.value, "Text 2")

    def test_parse_only_space(self):
        parser = self._parser
        text = '   '
        with self.assertRaises(ValueError):
            parser.parse_argument(text)

    def test_parse_float_with_dot(self):
        parser = self._parser
        text = '7.5'
        result = parser.parse_argument(text)
        self.assertEqual(result.value, 7.5)

    def test_parse_eq_inside_string(self):
        parser = self._parser
        text = '"arg = 7"'
        result = parser.parse_argument(text)
        self.assertEqual(result.value, "arg = 7")
        self.assertEqual(result.name, None)

    def test_parse_eq_inside_string_named(self):
        parser = self._parser
        text = 'arg2 ="arg = 7"'
        result = parser.parse_argument(text)
        self.assertEqual(result.value, "arg = 7")
        self.assertEqual(result.name, "arg2")
