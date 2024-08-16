import unittest
from devana.preprocessing.components.property.parsers.types import *
from devana.preprocessing.components.property.parsers.parser import IParsableElement, ParsableElementError


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
