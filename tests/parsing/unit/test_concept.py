import unittest
from difflib import restore

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

    def test_concept_case_1(self):
        node = find_by_name(self.cursor, "ConceptCase1")
        result = ConceptInfo.from_cursor(node)
        self.assertIsNone(result.parent)
        self.assertEqual(result.name, "ConceptCase1")
        self.assertEqual(result.body.replace("\r\n", "\n"), "requires(T a) {\n    { --a };\n    { a-- };\n}")
        self.assertEqual(len(result.template.parameters), 1)
        self.assertEqual(result.is_requirement, False)

    def test_concept_case_2(self):
        node = find_by_name(self.cursor, "ConceptCase2")
        result = ConceptInfo.from_cursor(node)
        self.assertIsNone(result.parent)
        self.assertEqual(result.name, "ConceptCase2")
        self.assertEqual(
            result.body.replace("\r\n", "\n"),
            "requires(T a, T b) {\n    { a + b };\n}"
        )
        self.assertEqual(len(result.template.parameters), 1)
        self.assertEqual(result.is_requirement, False)

    def test_concept_case_3(self):
        node = find_by_name(self.cursor, "ConceptCase3")
        result = ConceptInfo.from_cursor(node)
        self.assertIsNone(result.parent)
        self.assertEqual(result.name, "ConceptCase3")
        self.assertEqual(
            result.body.replace("\r\n", "\n"),
    "requires(T a, T b) {\n    a = b;\n} || requires(T a, T b) {\n    b = a;\n}"
        )
        self.assertEqual(len(result.template.parameters), 1)
        self.assertEqual(result.is_requirement, False)

    def test_concept_case_4(self):
        node = find_by_name(self.cursor, "ConceptCase4")
        result = ConceptInfo.from_cursor(node)
        self.assertIsNone(result.parent)
        self.assertEqual(result.name, "ConceptCase4")
        self.assertEqual(result.body.replace("\r\n", "\n"), "requires {\n    T{};\n}")
        self.assertEqual(len(result.template.parameters), 1)
        self.assertEqual(result.is_requirement, False)

    def test_concept_case_5(self):
        node = find_by_name(self.cursor, "ConceptCase5")
        result = ConceptInfo.from_cursor(node)
        self.assertIsNone(result.parent)
        self.assertEqual(result.name, "ConceptCase5")
        self.assertEqual(
            result.body.replace("\r\n", "\n"),
            "requires {\n    T(-1) < T(0); \n}"
        )
        self.assertEqual(len(result.template.parameters), 1)
        self.assertEqual(result.is_requirement, False)

    def test_concept_case_6(self):
        node = find_by_name(self.cursor, "ConceptCase6")
        result = ConceptInfo.from_cursor(node)
        self.assertIsNone(result.parent)
        self.assertEqual(result.name, "ConceptCase6")
        self.assertEqual(
            result.body.replace("\r\n", "\n"),
            "ConceptCase1<T> && requires(T t) {\n    *t;\n}"
        )
        self.assertEqual(len(result.template.parameters), 1)
        self.assertEqual(result.is_requirement, False)

    def test_concept_case_7(self):
        node = find_by_name(self.cursor, "ConceptCase7")
        result = ConceptInfo.from_cursor(node)
        self.assertIsNone(result.parent)
        self.assertEqual(result.name, "ConceptCase7")
        self.assertEqual(result.body, "(T{} > 0)")
        self.assertEqual(len(result.template.parameters), 1)
        self.assertEqual(result.is_requirement, False)

    def test_concept_case_8(self):
        node = find_by_name(self.cursor, "ConceptCase8")
        result = ConceptInfo.from_cursor(node)
        self.assertIsNone(result.parent)
        self.assertEqual(result.name, "ConceptCase8")
        self.assertEqual(result.body, "ConceptCase7<T>")
        self.assertEqual(len(result.template.parameters), 1)
        self.assertEqual(result.is_requirement, False)
        self.assertEqual(result.template.parameters[0].specifier.name, "ConceptCase7")
        self.assertEqual(result.template.parameters[0].specifier.is_requirement, True)

    def test_concept_case_9(self):
        node = find_by_name(self.cursor, "ConceptCase9")
        result = ConceptInfo.from_cursor(node)
        self.assertIsNone(result.parent)
        self.assertEqual(result.name, "ConceptCase9")
        self.assertEqual(result.body, "ConceptCase1<T> && ConceptCase2<T>")
        self.assertEqual(len(result.template.parameters), 1)
        self.assertEqual(result.is_requirement, False)

    def test_concept_case_10(self):
        node = find_by_name(self.cursor, "ConceptCase10")
        result = ConceptInfo.from_cursor(node)
        self.assertIsNone(result.parent)
        self.assertEqual(result.name, "ConceptCase10")
        self.assertEqual(result.body, "ConceptCase1<T> || ConceptCase2<T>")
        self.assertEqual(len(result.template.parameters), 1)
        self.assertEqual(result.is_requirement, False)

    def test_concept_case_11(self):
        node = find_by_name(self.cursor, "ConceptCase11")
        result = ConceptInfo.from_cursor(node)
        self.assertIsNone(result.parent)
        self.assertEqual(result.name, "ConceptCase11")
        self.assertEqual(result.body, "true")
        self.assertEqual(len(result.template.parameters), 1)
        self.assertEqual(result.is_requirement, False)

    def test_concept_case_12(self):
        node = find_by_name(self.cursor, "ConceptCase12")
        result = ConceptInfo.from_cursor(node)
        self.assertIsNone(result.parent)
        self.assertEqual(result.name, "ConceptCase12")
        self.assertEqual(result.body, "T::value || true")
        self.assertEqual(len(result.template.parameters), 1)
        self.assertEqual(result.is_requirement, False)

    def test_concept_case_13(self):
        node = find_by_name(self.cursor, "ConceptCase13")
        result = ConceptInfo.from_cursor(node)
        self.assertIsNone(result.parent)
        self.assertEqual(result.name, "ConceptCase13")
        self.assertEqual(result.body, "ConceptCase11<U*>")
        self.assertEqual(len(result.template.parameters), 1)
        self.assertEqual(result.is_requirement, False)

    def test_concept_template(self):
        node = find_by_name(self.cursor, "ConceptTemplate")
        result = ConceptInfo.from_cursor(node)
        self.assertIsNone(result.parent)
        self.assertEqual(result.name, "ConceptTemplate")
        self.assertEqual(result.body, "true")
        self.assertEqual(result.template.parent, None)
        self.assertEqual(result.template.is_empty, False)
        self.assertEqual(result.template.requires, None)
        self.assertEqual(len(result.template.parameters), 3)

        self.assertEqual(result.template.parameters[0].name, "A")
        self.assertEqual(result.template.parameters[0].specifier, "typename")
        self.assertEqual(result.template.parameters[0].is_variadic, False)
        self.assertEqual(result.template.parameters[0].default_value, None)

        self.assertEqual(result.template.parameters[1].name, "B")
        self.assertEqual(result.template.parameters[1].specifier, "class")
        self.assertEqual(result.template.parameters[1].is_variadic, False)
        self.assertEqual(result.template.parameters[1].default_value, "int")

        self.assertEqual(result.template.parameters[2].name, "Args")
        self.assertEqual(result.template.parameters[2].specifier, "typename")
        self.assertEqual(result.template.parameters[2].is_variadic, True)
        self.assertEqual(result.template.parameters[2].default_value, None)