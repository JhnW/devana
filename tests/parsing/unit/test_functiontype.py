import unittest
import clang.cindex
import clang
import os
from tests.helpers import find_by_name, stub_lexicon
from devana.syntax_abstraction.typeexpression import BasicType
from devana.syntax_abstraction.organizers.sourcefile import SourceFile
from devana.syntax_abstraction.functiontype import FunctionType
from devana.syntax_abstraction.variable import GlobalVariable
from devana.syntax_abstraction.classinfo import *
from devana.syntax_abstraction.templateinfo import GenericTypeParameter


class TestFunctionPointerBasic(unittest.TestCase):

    def setUp(self):
        index = clang.cindex.Index.create()
        self.cursor = index.parse(os.path.dirname(__file__) + r"/source_files/function_ptr.hpp").cursor

    def test_function_pointer_empty(self):
        node = find_by_name(self.cursor, "empty_func")
        fnc_node = node.type.get_pointee()
        result = FunctionType.from_cursor(fnc_node)
        stub_lexicon(result)
        self.assertEqual(len(result.arguments), 0)
        self.assertEqual(result.return_type.details, BasicType.VOID)

    def test_core_function_pointer_standard(self):
        node = find_by_name(self.cursor, "standard_func")
        fnc_node = node.type.get_pointee()
        result = FunctionType.from_cursor(fnc_node)
        stub_lexicon(result)
        self.assertEqual(len(result.arguments), 2)
        self.assertEqual(result.arguments[0].details, BasicType.DOUBLE)
        self.assertEqual(result.arguments[1].details, BasicType.CHAR)
        self.assertEqual(result.return_type.details, BasicType.FLOAT)

    def test_core_function_pointer_return_attributes(self):
        node = find_by_name(self.cursor, "return_attributes_func")
        fnc_node = node.type.get_pointee()
        result = FunctionType.from_cursor(fnc_node)
        stub_lexicon(result)
        self.assertEqual(len(result.arguments), 0)
        self.assertEqual(result.return_type.details, BasicType.FLOAT)
        self.assertTrue(result.return_type.modification.is_const)
        self.assertTrue(result.return_type.modification.is_reference)

    def test_core_function_pointer_arguments_attributes(self):
        node = find_by_name(self.cursor, "arguments_attributes_func")
        fnc_node = node.type.get_pointee()
        result = FunctionType.from_cursor(fnc_node)
        stub_lexicon(result)
        self.assertEqual(len(result.arguments), 2)
        self.assertEqual(result.arguments[0].details, BasicType.FLOAT)
        self.assertTrue(result.arguments[0].modification.is_const)
        self.assertTrue(result.arguments[0].modification.is_reference)
        self.assertEqual(result.arguments[1].details, BasicType.INT)
        self.assertTrue(result.arguments[1].modification.is_pointer)
        self.assertFalse(result.arguments[1].modification.is_reference)
        self.assertFalse(result.arguments[1].modification.is_const)
        self.assertEqual(result.return_type.details, BasicType.VOID)


class TestFunctionPointerAdvanced(unittest.TestCase):

    def setUp(self):
        index = clang.cindex.Index.create()
        self.cursor = index.parse(os.path.dirname(__file__) + r"/source_files/function_ptr.hpp").cursor
        self.file = SourceFile(self.cursor)

    def test_function_pointer_in_type_expression(self):
        element: GlobalVariable = self.file.content[1]
        self.assertEqual(element.name, "standard_func")
        self.assertTrue(element.type.modification.is_pointer)
        result: FunctionType = element.type.details
        self.assertEqual(len(result.arguments), 2)
        self.assertEqual(result.arguments[0].details, BasicType.DOUBLE)
        self.assertEqual(result.arguments[1].details, BasicType.CHAR)
        self.assertEqual(result.return_type.details, BasicType.FLOAT)

    def test_function_pointer_nested(self):
        element_1: GlobalVariable = self.file.content[4]
        element_2: GlobalVariable = self.file.content[5]
        self.assertEqual(element_1 .name, "nested_1")
        self.assertEqual(element_2 .name, "nested_2")
        self.assertEqual(element_1.type.details.return_type.details, BasicType.VOID)
        self.assertEqual(element_2.type.details.return_type.details, BasicType.VOID)
        self.assertEqual(len(element_1.type.details.arguments), 2)
        self.assertEqual(len(element_2.type.details.arguments), 2)
        self.assertEqual(element_1.type.details.arguments[0].details, BasicType.INT)
        self.assertEqual(element_2.type.details.arguments[0].details, BasicType.INT)
        self.assertTrue(element_1.type.details.arguments[1].modification.is_pointer)
        self.assertTrue(element_2.type.details.arguments[1].modification.is_pointer)
        fnc_1: FunctionType = element_1.type.details.arguments[1].details
        fnc_2: FunctionType = element_2.type.details.arguments[1].details
        self.assertTrue(type(fnc_1) is FunctionType)
        self.assertTrue(type(fnc_2) is FunctionType)
        self.assertEqual(len(fnc_1.arguments), 1)
        self.assertEqual(len(fnc_2.arguments), 1)
        self.assertTrue(fnc_1.arguments[0].modification.is_const)
        self.assertTrue(fnc_2.arguments[0].modification.is_const)
        self.assertEqual(fnc_1.return_type.details, BasicType.FLOAT)
        self.assertEqual(fnc_2.return_type.details, BasicType.FLOAT)
        self.assertEqual(fnc_1.arguments[0].details, BasicType.DOUBLE)
        self.assertEqual(fnc_2.arguments[0].details, BasicType.DOUBLE)

    def test_function_pointer_class_types(self):
        element: GlobalVariable = self.file.content[7]
        class_type = self.file.content[6]
        self.assertEqual(element.name, "with_class_fnc")
        self.assertTrue(element.type.modification.is_pointer)
        fnc: FunctionType = element.type.details
        self.assertTrue(fnc.return_type.modification.is_reference)
        self.assertEqual(fnc.return_type.details, class_type)
        self.assertEqual(len(fnc.arguments), 2)
        self.assertEqual(fnc.arguments[0].details, class_type)
        self.assertTrue(fnc.arguments[0].modification.is_pointer)
        self.assertTrue(fnc.arguments[0].modification.is_const)

    def test_function_pointer_template_types(self):
        element: FieldInfo = self.file.content[8].content[0]
        self.assertTrue(element.type.modification.is_pointer)
        self.assertTrue(element.type.details.return_type.modification.is_pointer)
        self.assertTrue(type(element.type.details.return_type.details) is GenericTypeParameter)
        self.assertTrue(element.type.details.arguments[0].modification.is_const)
        self.assertTrue(type(element.type.details.arguments[0].details) is GenericTypeParameter)

    def test_function_pointer_name(self):
        element: GlobalVariable = self.file.content[3]
        self.assertEqual(element.type.details.name, "void ()(const float&, int*)")
        self.assertEqual(element.type.name, "void (*)(const float&, int*)")
