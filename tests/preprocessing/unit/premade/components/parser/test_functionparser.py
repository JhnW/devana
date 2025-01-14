import unittest
from devana.preprocessing.premade.components.parser.functionparser import FunctionParser


class TestFunctionParser(unittest.TestCase):


    def test_parse_one_function_with_empty_arguments(self):
        parser = FunctionParser()
        result = parser.parse("foo()")
        self.assertEqual(1, len(result))
        self.assertEqual("foo", result[0].name)
        self.assertEqual([], result[0].namespaces)
        self.assertEqual("", result[0].arguments)

    def test_parse_one_function_name_with_underscore(self):
        parser = FunctionParser()
        result = parser.parse('foo_bar()')
        self.assertEqual(1, len(result))
        self.assertEqual("foo_bar", result[0].name)
        self.assertEqual([], result[0].namespaces)
        self.assertEqual("", result[0].arguments)

    def test_parse_one_function_without_arguments(self):
        parser = FunctionParser()
        result = parser.parse("foo")
        self.assertEqual(1, len(result))
        self.assertEqual("foo", result[0].name)
        self.assertEqual([], result[0].namespaces)
        self.assertEqual("", result[0].arguments)

    def test_parse_one_function_one_argument(self):
        parser = FunctionParser()
        result = parser.parse("foo(67.9)")
        self.assertEqual(1, len(result))
        self.assertEqual("foo", result[0].name)
        self.assertEqual([], result[0].namespaces)
        self.assertEqual("67.9", result[0].arguments)

    def test_parse_one_function_multiple_argument(self):
        parser = FunctionParser()
        result = parser.parse("foo(67.9, baz)")
        self.assertEqual(1, len(result))
        self.assertEqual("foo", result[0].name)
        self.assertEqual([], result[0].namespaces)
        self.assertEqual("67.9, baz", result[0].arguments)

    def test_parse_one_function_multiple_argument(self):
        parser = FunctionParser()
        result = parser.parse("foo(67.9, baz)")
        self.assertEqual(1, len(result))
        self.assertEqual("foo", result[0].name)
        self.assertEqual([], result[0].namespaces)
        self.assertEqual("67.9, baz", result[0].arguments)

    def test_parse_one_function_string(self):
        parser = FunctionParser()
        result = parser.parse('foo("67.9, baz")')
        self.assertEqual(1, len(result))
        self.assertEqual("foo", result[0].name)
        self.assertEqual([], result[0].namespaces)
        self.assertEqual('"67.9, baz"', result[0].arguments)

    def test_parse_one_function_string_escape(self):
        parser = FunctionParser()
        result = parser.parse('foo("67.9, /"baz")')
        self.assertEqual(1, len(result))
        self.assertEqual("foo", result[0].name)
        self.assertEqual([], result[0].namespaces)
        self.assertEqual('"67.9, /"baz"', result[0].arguments)

    def test_parse_one_function_namespace_in_arguments(self):
        parser = FunctionParser()
        result = parser.parse('foo(baz::goo)')
        self.assertEqual(1, len(result))
        self.assertEqual("foo", result[0].name)
        self.assertEqual([], result[0].namespaces)
        self.assertEqual('baz::goo', result[0].arguments)

    def test_parse_one_function_namespace(self):
        parser = FunctionParser()
        result = parser.parse('baz::foo()')
        self.assertEqual(1, len(result))
        self.assertEqual("foo", result[0].name)
        self.assertEqual(["baz"], result[0].namespaces)
        self.assertEqual("", result[0].arguments)

    def test_parse_one_function_namespace_with_underscore(self):
        parser = FunctionParser()
        result = parser.parse('baz_bar::foo()')
        self.assertEqual(1, len(result))
        self.assertEqual("foo", result[0].name)
        self.assertEqual(["baz_bar"], result[0].namespaces)
        self.assertEqual("", result[0].arguments)

    def test_parse_one_function_multiple_namespace(self):
        parser = FunctionParser()
        result = parser.parse('bar::baz::foo()')
        self.assertEqual(1, len(result))
        self.assertEqual("foo", result[0].name)
        self.assertEqual(["bar", "baz"], result[0].namespaces)
        self.assertEqual("", result[0].arguments)

    def test_parse_one_function_incomplete_namespace(self):
        parser = FunctionParser()
        self.assertRaises(ValueError, parser.parse, 'bar:baz::foo()')

    def test_parse_one_function_incomplete_arguments(self):
        parser = FunctionParser()
        self.assertRaises(ValueError, parser.parse, 'foo(')

    def test_parse_one_function_bad_symbol(self):
        parser = FunctionParser()
        self.assertRaises(ValueError, parser.parse, 'fo-')

    def test_parse_one_function_bad_whitespace(self):
        parser = FunctionParser()
        self.assertRaises(ValueError, parser.parse, 'f o')

    def test_parse_multiple_function_empty_args(self):
        parser = FunctionParser()
        result = parser.parse('foo(), bar')
        self.assertEqual(2, len(result))
        self.assertEqual("foo", result[0].name)
        self.assertEqual([], result[0].namespaces)
        self.assertEqual("", result[0].arguments)
        self.assertEqual("bar", result[1].name)
        self.assertEqual([], result[1].namespaces)
        self.assertEqual("", result[1].arguments)
