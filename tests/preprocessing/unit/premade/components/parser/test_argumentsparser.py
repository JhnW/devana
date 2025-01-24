import unittest
from enum import Enum, auto
from devana.preprocessing.premade.components.parser.argumentsparser import ArgumentsParser, ArgumentGenericTypeParser


class TestArgumentsParser(unittest.TestCase):


    def test_parse_empty(self):
        tokenizer = ArgumentsParser()
        result = tokenizer.tokenize("")
        self.assertEqual([], result)

    def test_parse_integer(self):
        tokenizer = ArgumentsParser()
        result = tokenizer.tokenize("589")
        self.assertEqual([589], result)

    def test_parse_minus_integer(self):
        tokenizer = ArgumentsParser()
        result = tokenizer.tokenize("-589")
        self.assertEqual([-589], result)

    def test_parse_plus_integer(self):
        tokenizer = ArgumentsParser()
        result = tokenizer.tokenize("+589")
        self.assertEqual([589], result)

    def test_parse_float(self):
        tokenizer = ArgumentsParser()
        result = tokenizer.tokenize("7.5")
        self.assertEqual([7.5], result)

        result = tokenizer.tokenize(".5")
        self.assertEqual([.5], result)

        result = tokenizer.tokenize("7.")
        self.assertEqual([7.], result)

    def test_parse_minus_float(self):
        tokenizer = ArgumentsParser()
        result = tokenizer.tokenize("-7.5")
        self.assertEqual([-7.5], result)

        result = tokenizer.tokenize("-.5")
        self.assertEqual([-.5], result)

        result = tokenizer.tokenize("-7.")
        self.assertEqual([-7.], result)

    def test_parse_plus_float(self):
        tokenizer = ArgumentsParser()
        result = tokenizer.tokenize("+7.5")
        self.assertEqual([7.5], result)

        result = tokenizer.tokenize("+.5")
        self.assertEqual([+.5], result)

        result = tokenizer.tokenize("+7.")
        self.assertEqual([+7.], result)

    def test_parse_string(self):
        tokenizer = ArgumentsParser()
        result = tokenizer.tokenize('"test str"')
        self.assertEqual(["test str"], result)

    def test_parse_escape_string(self):
        tokenizer = ArgumentsParser()
        result = tokenizer.tokenize(r'"test \"str"')
        self.assertEqual([r"test \"str"], result)

    def test_parse_none(self):
        tokenizer = ArgumentsParser()
        result = tokenizer.tokenize("None")
        self.assertEqual([None], result)

    def test_parse_true(self):
        tokenizer = ArgumentsParser()
        result = tokenizer.tokenize("true")
        self.assertEqual([True], result)

    def test_parse_false(self):
        tokenizer = ArgumentsParser()
        result = tokenizer.tokenize("false")
        self.assertEqual([False], result)

    def test_parse_list(self):
        tokenizer = ArgumentsParser()
        result = tokenizer.tokenize("[1, 3, 6.7]")
        self.assertEqual([[1, 3, 6.7]], result)

    def test_parse_empty_list(self):
        tokenizer = ArgumentsParser()
        result = tokenizer.tokenize("[]")
        self.assertEqual([[]], result)

    def test_parse_nested_list(self):
        tokenizer = ArgumentsParser()
        result = tokenizer.tokenize('[1, [2, 3]]')
        self.assertEqual([[1, [2, 3]]], result)

    def test_parse_complex_nested_list(self):
        tokenizer = ArgumentsParser()
        result = tokenizer.tokenize('[1, [], [6.7, ["str", 888]]]')
        self.assertEqual([[1, [], [6.7, ["str", 888]]]], result)

    def test_parse_multiple_arguments(self):
        tokenizer = ArgumentsParser()
        result = tokenizer.tokenize('true, 5.25, false')
        self.assertEqual([True, 5.25, False], result)

    def test_parse_named_argument(self):
        tokenizer = ArgumentsParser()
        result = tokenizer.tokenize('label=7')
        self.assertEqual([{"label": 7}], result)

    def test_parse_named_multiple_argument(self):
        tokenizer = ArgumentsParser()
        result = tokenizer.tokenize('9, label=7, label_2=45')
        self.assertEqual([9, {"label": 7}, {"label_2": 45}], result)

    def test_parse_enum(self):

        class TestEnum(Enum):
            TEST_VALUE_1 = auto()
            TEST_VALUE_2 = auto()
            TEST_VALUE_3 = auto()

        tokenizer = ArgumentsParser([ArgumentGenericTypeParser.create_from_enum(TestEnum)])
        result = tokenizer.tokenize("TEST_VALUE_1")
        self.assertEqual([TestEnum.TEST_VALUE_1], result)


    def test_parse_multiple_enum(self):

        class TestEnum(Enum):
            TEST_VALUE_1 = auto()
            TEST_VALUE_2 = auto()
            TEST_VALUE_3 = auto()

        tokenizer = ArgumentsParser([ArgumentGenericTypeParser.create_from_enum(TestEnum)])
        result = tokenizer.tokenize("[TEST_VALUE_1, 8], TEST_VALUE_3, TEST_VALUE_2", )
        self.assertEqual([[TestEnum.TEST_VALUE_1, 8], TestEnum.TEST_VALUE_3, TestEnum.TEST_VALUE_2], result)