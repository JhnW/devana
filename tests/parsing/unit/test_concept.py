import unittest
import clang
import os

from devana.syntax_abstraction.conceptinfo import ConceptInfo
from devana.syntax_abstraction.functioninfo import FunctionInfo
from tests.helpers import find_by_name, stub_lexicon


class TestConcept(unittest.TestCase):

    def setUp(self):
        index = clang.cindex.Index.create()
        self.cursor = index.parse(
            os.path.dirname(__file__) + r"/source_files/concept.hpp",
            args=("-std=c++20",)
        ).cursor

    def test_decrementable(self):
        node = find_by_name(self.cursor, "ConceptCase1")
        result = ConceptInfo.from_cursor(node)
        stub_lexicon(result)
        self.assertIsNone(result.parent)
        self.assertEqual(result.name, "ConceptCase1")
        self.assertEqual(result.body, "requires(T a) {\n    { --a };\n    { a-- };\n}")
        self.assertEqual(len(result.template.parameters), 1)

    def test_addable(self):
        node = find_by_name(self.cursor, "ConceptCase2")
        result = ConceptInfo.from_cursor(node)
        stub_lexicon(result)
        self.assertIsNone(result.parent)
        self.assertEqual(result.name, "ConceptCase2")
        self.assertEqual(result.body, "requires(T a, T b) {\n    { a + b };\n}")
        self.assertEqual(len(result.template.parameters), 1)

    def test_assignable(self):
        node = find_by_name(self.cursor, "ConceptCase3")
        result = ConceptInfo.from_cursor(node)
        stub_lexicon(result)
        self.assertIsNone(result.parent)
        self.assertEqual(result.name, "ConceptCase3")
        self.assertEqual(result.body,
    "requires(T a, T b) {\n    a = b;\n} || requires(T a, T b) {\n    b = a;\n}"
        )
        self.assertEqual(len(result.template.parameters), 1)

    def test_default_constructible(self):
        node = find_by_name(self.cursor, "ConceptCase4")
        result = ConceptInfo.from_cursor(node)
        stub_lexicon(result)
        self.assertIsNone(result.parent)
        self.assertEqual(result.name, "ConceptCase4")
        self.assertEqual(result.body, "requires {\n    T{};\n}")
        self.assertEqual(len(result.template.parameters), 1)

    def test_signed(self):
        node = find_by_name(self.cursor, "ConceptCase5")
        result = ConceptInfo.from_cursor(node)
        stub_lexicon(result)
        self.assertIsNone(result.parent)
        self.assertEqual(result.name, "ConceptCase5")
        self.assertEqual(result.body, "requires {\n    T(-1) < T(0); \n}")
        self.assertEqual(len(result.template.parameters), 1)

    def test_rev_iterator(self):
        node = find_by_name(self.cursor, "ConceptCase6")
        result = ConceptInfo.from_cursor(node)
        stub_lexicon(result)
        self.assertIsNone(result.parent)
        self.assertEqual(result.name, "ConceptCase6")
        self.assertEqual(result.body, "ConceptCase1<T> && requires(T t) {\n    *t;\n}")
        self.assertEqual(len(result.template.parameters), 1)

    def test_default_positive(self):
        node = find_by_name(self.cursor, "ConceptCase7")
        result = ConceptInfo.from_cursor(node)
        stub_lexicon(result)
        self.assertIsNone(result.parent)
        self.assertEqual(result.name, "ConceptCase7")
        self.assertEqual(result.body, "(T{} > 0)")
        self.assertEqual(len(result.template.parameters), 1)

    def test_integral(self):
        node = find_by_name(self.cursor, "ConceptCase8")
        result = ConceptInfo.from_cursor(node)
        stub_lexicon(result)
        self.assertIsNone(result.parent)
        self.assertEqual(result.name, "ConceptCase8")
        self.assertEqual(result.body, "ConceptCase7<T>")
        self.assertEqual(len(result.template.parameters), 1)
        self.assertEqual(result.template.parameters[0].specifier.name, "ConceptCase7")

    def test_decrementable_and_addable(self):
        node = find_by_name(self.cursor, "ConceptCase9")
        result = ConceptInfo.from_cursor(node)
        stub_lexicon(result)
        self.assertIsNone(result.parent)
        self.assertEqual(result.name, "ConceptCase9")
        self.assertEqual(result.body, "ConceptCase1<T> && ConceptCase2<T>")
        self.assertEqual(len(result.template.parameters), 1)

    def test_decrementable_or_addable(self):
        node = find_by_name(self.cursor, "ConceptCase10")
        result = ConceptInfo.from_cursor(node)
        stub_lexicon(result)
        self.assertIsNone(result.parent)
        self.assertEqual(result.name, "ConceptCase10")
        self.assertEqual(result.body, "ConceptCase1<T> || ConceptCase2<T>")
        self.assertEqual(len(result.template.parameters), 1)

    def test_always_true(self):
        node = find_by_name(self.cursor, "ConceptCase11")
        result = ConceptInfo.from_cursor(node)
        stub_lexicon(result)
        self.assertIsNone(result.parent)
        self.assertEqual(result.name, "ConceptCase11")
        self.assertEqual(result.body, "true")
        self.assertEqual(len(result.template.parameters), 1)

    def test_has_value_with_bool(self):
        node = find_by_name(self.cursor, "ConceptCase12")
        result = ConceptInfo.from_cursor(node)
        stub_lexicon(result)
        self.assertIsNone(result.parent)
        self.assertEqual(result.name, "ConceptCase12")
        self.assertEqual(result.body, "T::value || true")
        self.assertEqual(len(result.template.parameters), 1)

    def test_pointer(self):
        node = find_by_name(self.cursor, "ConceptCase13")
        result = ConceptInfo.from_cursor(node)
        stub_lexicon(result)
        self.assertIsNone(result.parent)
        self.assertEqual(result.name, "ConceptCase13")
        self.assertEqual(result.body, "ConceptCase11<U*>")
        self.assertEqual(len(result.template.parameters), 1)
