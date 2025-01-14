import unittest
import os
from typing import List
from devana.syntax_abstraction.organizers.sourcefile import SourceFile
from devana.syntax_abstraction.attribute import Attribute
from devana.syntax_abstraction.functioninfo import FunctionInfo
from devana.syntax_abstraction.classinfo import ClassInfo, FieldInfo, MethodInfo
from devana.syntax_abstraction.namespaceinfo import NamespaceInfo
from devana.syntax_abstraction.enuminfo import EnumInfo



class TestAttributesParser(unittest.TestCase):

    def test_parse_attribute(self):
        result: List[Attribute] = Attribute.from_whole_declaration_text("nodiscard")
        self.assertEqual(1, len(result))
        self.assertEqual("nodiscard", result[0].name)
        self.assertEqual(None, result[0].namespace)
        self.assertEqual(None, result[0].arguments)

    def test_parse_namespace_attribute(self):
        result: List[Attribute] = Attribute.from_whole_declaration_text("gnu::nodiscard")
        self.assertEqual(1, len(result))
        self.assertEqual("nodiscard", result[0].name)
        self.assertEqual("gnu", result[0].namespace)
        self.assertEqual(None, result[0].arguments)

    def test_parse_attribute_function_no_args(self):
        result: List[Attribute] = Attribute.from_whole_declaration_text("nodiscard()")
        self.assertEqual(1, len(result))
        self.assertEqual("nodiscard", result[0].name)
        self.assertEqual(None, result[0].namespace)
        self.assertEqual([], result[0].arguments)

    def test_parse_attribute_function_args(self):
        result: List[Attribute] = Attribute.from_whole_declaration_text('nodiscard("arg1",arg2, 7)')
        self.assertEqual(1, len(result))
        self.assertEqual("nodiscard", result[0].name)
        self.assertEqual(None, result[0].namespace)
        self.assertEqual(3, len(result[0].arguments))
        self.assertEqual(['"arg1"', "arg2", "7"], result[0].arguments)

    def test_parse_attribute_namespace_function_args(self):
        result: List[Attribute] = Attribute.from_whole_declaration_text('gnu::nodiscard("arg1",arg2, 7)')
        self.assertEqual(1, len(result))
        self.assertEqual("nodiscard", result[0].name)
        self.assertEqual("gnu", result[0].namespace)
        self.assertEqual(3, len(result[0].arguments))
        self.assertEqual(['"arg1"', "arg2", "7"], result[0].arguments)

    def test_parse_simple_multiple_attribute(self):
        result: List[Attribute] = Attribute.from_whole_declaration_text('gnu::always_inline,gnu::hot, nodiscard, '
                                                                        'deprecated("because", '
                                                                        '12), gnu::deprecated("because", 7), '
                                                                        'no_arg_fnc()')
        self.assertEqual(6, len(result))
        self.assertEqual("always_inline", result[0].name)
        self.assertEqual("gnu", result[0].namespace)
        self.assertEqual(None, result[0].arguments)
        self.assertEqual("hot", result[1].name)
        self.assertEqual("gnu", result[1].namespace)
        self.assertEqual(None, result[1].arguments)
        self.assertEqual("nodiscard", result[2].name)
        self.assertEqual(None, result[2].namespace)
        self.assertEqual(None, result[2].arguments)
        self.assertEqual("deprecated", result[3].name)
        self.assertEqual(None, result[3].namespace)
        self.assertEqual(['"because"', "12"], result[3].arguments)
        self.assertEqual("deprecated", result[4].name)
        self.assertEqual("gnu", result[4].namespace)
        self.assertEqual(['"because"', "7"], result[4].arguments)
        self.assertEqual("no_arg_fnc", result[5].name)
        self.assertEqual(None, result[5].namespace)
        self.assertEqual([], result[5].arguments)

    def test_parse_attribute_using_namespace(self):
        result: List[Attribute] = Attribute.from_whole_declaration_text('using gnu : nodiscard, lol')
        self.assertEqual(2, len(result))
        self.assertEqual("nodiscard", result[0].name)
        self.assertEqual("gnu", result[0].namespace)
        self.assertEqual(None, result[0].arguments)
        self.assertEqual("lol", result[1].name)
        self.assertEqual("gnu", result[0].namespace)
        self.assertEqual(None, result[0].arguments)

    def test_attribute_argument_string_with_comma(self):
        result: List[Attribute] = Attribute.from_whole_declaration_text('text("Text, but with extra comma", "Another '
                                                        'argument", 7)')
        self.assertEqual(1, len(result))
        self.assertEqual(3, len(result[0].arguments))
        self.assertEqual("\"Text, but with extra comma\"", result[0].arguments[0])
        self.assertEqual("\"Another argument\"", result[0].arguments[1])
        self.assertEqual("7", result[0].arguments[2])


class TestAttributesDeclarationParser(unittest.TestCase):

    def setUp(self):
        self.file = SourceFile.from_path(os.path.dirname(__file__) + r"/source_files/attributes.hpp")

    def test_parse_attribute_using_namespace(self):
        result: List[Attribute] = Attribute.from_whole_declaration_text('using gnu : nodiscard, lol')
        self.assertEqual(2, len(result))
        self.assertEqual("nodiscard", result[0].name)
        self.assertEqual("gnu", result[0].namespace)
        self.assertEqual(None, result[0].arguments)
        self.assertEqual("lol", result[1].name)
        self.assertEqual("gnu", result[1].namespace)
        self.assertEqual(None, result[1].arguments)

    def test_parse_attribute_using_namespace_function(self):
        result: List[Attribute] = Attribute.from_whole_declaration_text('using gnu : nodiscard, lol(a)')
        self.assertEqual(2, len(result))
        self.assertEqual("nodiscard", result[0].name)
        self.assertEqual("gnu", result[0].namespace)
        self.assertEqual(None, result[0].arguments)
        self.assertEqual("lol", result[1].name)
        self.assertEqual("gnu", result[1].namespace)
        self.assertEqual(["a"], result[1].arguments)

    def test_parse_single_attribute_declaration(self):
        element: FunctionInfo = self.file.content[0]
        attrs = element.attributes
        self.assertEqual(1, len(attrs))
        attr = attrs[0]
        self.assertEqual(None, attr.using_namespace)
        self.assertEqual(1, len(attr.attributes))
        self.assertEqual(None, attr.attributes[0].arguments)
        self.assertEqual(None, attr.attributes[0].namespace)
        self.assertEqual("nodiscard", attr.attributes[0].name)

    def test_multiple_attribute_declaration(self):
        element: FunctionInfo = self.file.content[1]
        attrs = element.attributes
        self.assertEqual(3, len(attrs))

        attr = attrs[0]
        self.assertEqual(None, attr.using_namespace)
        self.assertEqual(1, len(attr.attributes))
        self.assertEqual(None, attr.attributes[0].arguments)
        self.assertEqual(None, attr.attributes[0].namespace)
        self.assertEqual("nodiscard", attr.attributes[0].name)

        attr = attrs[1]
        self.assertEqual(None, attr.using_namespace)
        self.assertEqual(1, len(attr.attributes))
        self.assertEqual(None, attr.attributes[0].arguments)
        self.assertEqual(None, attr.attributes[0].namespace)
        self.assertEqual("test_foo2", attr.attributes[0].name)

        attr = attrs[2]
        self.assertEqual(None, attr.using_namespace)
        self.assertEqual(1, len(attr.attributes))
        self.assertEqual(None, attr.attributes[0].arguments)
        self.assertEqual(None, attr.attributes[0].namespace)
        self.assertEqual("test_foo2_2", attr.attributes[0].name)

    def test_attribute_function(self):
        element: FunctionInfo = self.file.content[2]
        self.assertEqual(1, len(element.attributes))

        self.assertEqual(None, element.attributes[0].using_namespace)
        self.assertEqual(1, len(element.attributes[0].attributes))
        self.assertEqual(None, element.attributes[0].attributes[0].arguments)
        self.assertEqual(None, element.attributes[0].attributes[0].namespace)
        self.assertEqual("nodiscard", element.attributes[0].attributes[0].name)

    def test_attribute_function_args(self):
        element: FunctionInfo = self.file.content[2]
        self.assertEqual(3, len(element.arguments))

        self.assertEqual(1, len(element.arguments[0].attributes))
        self.assertEqual("maybe_unused", element.arguments[0].attributes[0].attributes[0].name)
        self.assertEqual(None, element.arguments[0].attributes[0].attributes[0].namespace)
        self.assertEqual(None, element.arguments[0].attributes[0].attributes[0].arguments)

        self.assertEqual(0, len(element.arguments[1].attributes))
        self.assertEqual(2, len(element.arguments[2].attributes))

        self.assertEqual("test_1", element.arguments[2].attributes[0].attributes[0].name)
        self.assertEqual(None, element.arguments[2].attributes[0].attributes[0].namespace)
        self.assertEqual(None, element.arguments[2].attributes[0].attributes[0].arguments)
        self.assertEqual("test_2", element.arguments[2].attributes[0].attributes[1].name)
        self.assertEqual(None, element.arguments[2].attributes[0].attributes[1].namespace)
        self.assertEqual(None, element.arguments[2].attributes[0].attributes[1].arguments)
        self.assertEqual("test_3", element.arguments[2].attributes[1].attributes[0].name)
        self.assertEqual(None, element.arguments[2].attributes[1].attributes[0].namespace)
        self.assertEqual(None, element.arguments[2].attributes[1].attributes[0].arguments)

    def test_attribute_struct(self):
        element: ClassInfo = self.file.content[3]
        self.assertEqual(1, len(element.attributes))
        self.assertEqual(1, len(element.attributes[0].attributes))
        self.assertEqual("deprecated", element.attributes[0].attributes[0].name)
        self.assertEqual(None, element.attributes[0].attributes[0].arguments)
        self.assertEqual(None, element.attributes[0].attributes[0].namespace)

    def test_attribute_struct_field(self):
        element: ClassInfo = self.file.content[3]

        field: FieldInfo = element.content[0]
        self.assertEqual(0, len(field.attributes))
        field: FieldInfo = element.content[1]
        self.assertEqual(0, len(field.attributes))
        field: FieldInfo = element.content[2]
        self.assertEqual(2, len(field.attributes))
        self.assertEqual(1, len(field.attributes[0].attributes))
        self.assertEqual("test_c1", field.attributes[0].attributes[0].name)
        self.assertEqual(1, len(field.attributes[1].attributes))
        self.assertEqual("test_c2", field.attributes[1].attributes[0].name)

    def test_attribute_struct_method(self):
        element: ClassInfo = self.file.content[3]
        method: MethodInfo = element.content[4]
        self.assertEqual(1, len(method.attributes))
        self.assertEqual(1, len(method.attributes[0].attributes))
        self.assertEqual("test_fnc", method.attributes[0].attributes[0].name)
        self.assertEqual(None, method.attributes[0].attributes[0].arguments)
        self.assertEqual(None, method.attributes[0].attributes[0].namespace)

        self.assertEqual(0, len(method.arguments[0].flatten_attributes))
        self.assertEqual(1, len(method.arguments[1].flatten_attributes))

    def test_attribute_namespace_declaration(self):
        namespace: NamespaceInfo = self.file.content[4]
        self.assertEqual(1, len(namespace.flatten_attributes))
        self.assertEqual("atr_namespace", namespace.flatten_attributes[0].name)
        self.assertEqual(None, namespace.flatten_attributes[0].namespace)
        self.assertEqual(None, namespace.flatten_attributes[0].arguments)

    def test_attribute_enum(self):
        enum_info: EnumInfo = self.file.content[5]
        self.assertEqual(1, len(enum_info.flatten_attributes))
        self.assertEqual("test_enum", enum_info.flatten_attributes[0].name)
        self.assertEqual(None, enum_info.flatten_attributes[0].namespace)
        self.assertEqual(None, enum_info.flatten_attributes[0].arguments)
