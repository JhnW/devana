import unittest
import clang.cindex
import clang
import os
from devana.syntax_abstraction.using import Using
from devana.syntax_abstraction.organizers.sourcefile import SourceFile
from devana.syntax_abstraction.functioninfo import FunctionInfo
from devana.syntax_abstraction.typeexpression import BasicType


class TestUsing(unittest.TestCase):

    def setUp(self):
        index = clang.cindex.Index.create()
        self.cursor = index.parse(
            os.path.dirname(__file__) + r"/source_files/using.hpp",
            args=("-std=c++20",)
        ).cursor
        self.file = SourceFile.from_cursor(self.cursor)

    def test_using_as_simple_alias(self):
        source: Using = self.file.content[1]
        self.assertEqual(source.name, "B")
        self.assertTrue(source.type_info.modification.is_const)
        self.assertTrue(source.type_info.modification.is_pointer)
        self.assertEqual(source.type_info.details, self.file.content[0].content[0])
        fnc: FunctionInfo = self.file.content[2]
        self.assertEqual(fnc.arguments[0].type.details, source)
        self.assertEqual(source.template, None)

    def test_using_as_template_alias(self):
        source: Using = self.file.content[4]
        self.assertEqual(source.name, "AT")
        self.assertTrue(source.type_info.modification.is_const)
        self.assertEqual(source.type_info.details, self.file.content[3])
        self.assertEqual(len(source.type_info.template_arguments), 1)
        self.assertEqual(source.type_info.template_arguments[0].details, BasicType.DOUBLE)
        self.assertEqual(source.template, None)

    def test_using_with_template(self):
        source: Using = self.file.content[8]
        self.assertEqual(source.name, "UsingTemplate")
        self.assertEqual(source.type_info.is_generic, True)
        self.assertEqual(source.type_info.details.name, "A")
        self.assertEqual(source.associated_comment, None)
        self.assertNotEqual(source.template, None)
        self.assertEqual(source.template.requires, None)

        self.assertEqual(len(source.template.parameters), 3)
        self.assertEqual(source.template.parameters[0].specifier, "typename")
        self.assertEqual(source.template.parameters[0].name, "A")
        self.assertEqual(source.template.parameters[0].default_value, None)
        self.assertEqual(source.template.parameters[0].is_variadic, False)
        self.assertEqual(source.template.parameters[1].specifier, "class")
        self.assertEqual(source.template.parameters[1].name, "B")
        self.assertEqual(source.template.parameters[1].default_value, "float")
        self.assertEqual(source.template.parameters[1].is_variadic, False)
        self.assertEqual(source.template.parameters[2].specifier, "typename")
        self.assertEqual(source.template.parameters[2].name, "Args")
        self.assertEqual(source.template.parameters[2].default_value, None)
        self.assertEqual(source.template.parameters[2].is_variadic, True)

    def test_using_with_template_requires(self):
        source: Using = self.file.content[9]
        self.assertEqual(source.name, "UsingTemplateRequires")
        self.assertEqual(source.type_info.is_generic, False)
        self.assertEqual(source.type_info.modification.is_const, True)
        self.assertEqual(source.type_info.details, self.file.content[6])
        self.assertEqual(len(source.type_info.template_arguments), 2)
        self.assertEqual(source.type_info.template_arguments[0].is_generic, True)
        self.assertEqual(source.type_info.template_arguments[0].details.name, "C")
        self.assertEqual(source.type_info.template_arguments[1].is_generic, True)
        self.assertEqual(source.type_info.template_arguments[1].details.name, "T")
        self.assertEqual(source.associated_comment, None)
        self.assertNotEqual(source.template, None)

        self.assertEqual(len(source.template.requires), 3)
        self.assertEqual(source.template.requires[0:2], ["true", "or"])
        self.assertEqual(source.template.requires[2].name, "TestConcept")
        self.assertEqual(source.template.requires[2].namespaces, [])
        self.assertEqual(source.template.requires[2].concept.body, "true")
        self.assertEqual(len(source.template.parameters), 2)
        self.assertEqual(source.template.parameters[0].specifier, "typename")
        self.assertEqual(source.template.parameters[0].name, "T")
        self.assertEqual(source.template.parameters[0].default_value, None)
        self.assertEqual(source.template.parameters[0].is_variadic, False)

    def test_using_with_concept(self):
        source: Using = self.file.content[10]
        self.assertEqual(source.name, "UsingConcept")
        self.assertEqual(source.type_info.is_generic, False)
        self.assertEqual(source.type_info.modification.is_const, True)
        self.assertEqual(source.type_info.modification.is_pointer, True)
        self.assertEqual(source.type_info.details, self.file.content[6])
        self.assertEqual(len(source.type_info.template_arguments), 2)
        self.assertEqual(source.type_info.template_arguments[0].is_generic, True)
        self.assertEqual(source.type_info.template_arguments[0].details.name, "float")
        self.assertEqual(source.associated_comment, None)
        self.assertNotEqual(source.template, None)
        self.assertEqual(source.template.requires, None)

        self.assertEqual(len(source.template.parameters), 1)
        self.assertEqual(source.template.parameters[0].specifier.name, "TestConcept")
        self.assertEqual(source.template.parameters[0].specifier.namespaces, [])
        self.assertEqual(source.template.parameters[0].specifier.concept.body, "true")
        self.assertEqual(source.template.parameters[0].name, "B")
        self.assertEqual(source.template.parameters[0].default_value, "int")
        self.assertEqual(source.template.parameters[0].is_variadic, False)
