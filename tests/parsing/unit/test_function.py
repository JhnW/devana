import unittest
import clang.cindex
import clang
import os

from tests.helpers import find_by_name, stub_lexicon
from devana.syntax_abstraction.typeexpression import BasicType, TypeModification
from devana.syntax_abstraction.functioninfo import FunctionInfo, FunctionModification
from devana.syntax_abstraction.organizers.sourcefile import SourceFile
from devana.utility.errors import CodeError
from devana.configuration import Configuration, LanguageStandard


class TestFunctionsSimple(unittest.TestCase):

    def setUp(self):
        index = clang.cindex.Index.create()
        config: Configuration = Configuration()
        config.parsing.language_version = LanguageStandard.CPP_20
        self.cursor = index.parse(os.path.dirname(__file__) + r"/source_files/simple_functions.hpp", args=config.parsing.parsing_options()).cursor

    def test_function_procedure(self):
        node = find_by_name(self.cursor, "procedure_forward")
        result = FunctionInfo.from_cursor(node)
        stub_lexicon(result)
        self.assertEqual(result.name, "procedure_forward")
        self.assertEqual(result.return_type.modification, TypeModification.NONE)
        self.assertEqual(result.return_type.details, BasicType.VOID)
        self.assertEqual(len(result.arguments), 0)
        self.assertEqual(result.modification, FunctionModification.NONE)
        self.assertEqual(result.body, None)
        self.assertEqual(len(result.overloading), 0)
        self.assertEqual(result.template, None)
        self.assertTrue(result.is_declaration)
        self.assertFalse(result.is_definition)

    def test_function_arguments(self):
        node = find_by_name(self.cursor, "num_forward")
        result = FunctionInfo.from_cursor(node)
        stub_lexicon(result)
        self.assertEqual(result.name, "num_forward")
        self.assertTrue(result.return_type.modification.is_pointer)
        self.assertEqual(result.return_type.details, BasicType.FLOAT)
        self.assertEqual(len(result.arguments), 2)
        self.assertEqual(result.arguments[0].name, "x")
        self.assertEqual(result.arguments[0].type.modification, TypeModification.NONE)
        self.assertEqual(result.arguments[0].type.details, BasicType.DOUBLE)
        self.assertEqual(result.arguments[0].default_value, None)
        self.assertEqual(result.arguments[1].name, "b")
        self.assertTrue(result.arguments[1].type.modification.is_pointer)
        self.assertEqual(result.arguments[1].type.details, BasicType.SHORT)
        self.assertEqual(result.arguments[1].default_value, None)
        self.assertEqual(result.modification, FunctionModification.NONE)
        self.assertEqual(result.body, None)
        self.assertEqual(len(result.overloading), 0)
        self.assertEqual(result.template, None)
        self.assertTrue(result.is_declaration)
        self.assertFalse(result.is_definition)

    def test_function_default_values(self):
        node = find_by_name(self.cursor, "num_default_forward")
        result = FunctionInfo.from_cursor(node)
        stub_lexicon(result)
        self.assertEqual(result.name, "num_default_forward")
        self.assertTrue(result.return_type.modification.is_reference)
        self.assertEqual(result.return_type.details, BasicType.FLOAT)
        self.assertEqual(len(result.arguments), 2)
        self.assertEqual(result.arguments[0].name, "test_var")
        self.assertEqual(result.arguments[0].type.modification, TypeModification.NONE)
        self.assertEqual(result.arguments[0].type.details, BasicType.DOUBLE)
        self.assertEqual(result.arguments[0].default_value, "76.0")
        self.assertEqual(result.arguments[1].name, "a")
        self.assertTrue(result.arguments[1].type.modification.is_pointer)
        self.assertEqual(result.arguments[1].type.details, BasicType.DOUBLE)
        self.assertEqual(result.arguments[1].default_value, "nullptr")
        self.assertEqual(result.modification, FunctionModification.NONE)
        self.assertEqual(result.body, None)
        self.assertEqual(len(result.overloading), 0)
        self.assertEqual(result.template, None)
        self.assertTrue(result.is_declaration)
        self.assertFalse(result.is_definition)

    def test_function_body(self):
        node = find_by_name(self.cursor, "procedure_def")
        result = FunctionInfo.from_cursor(node)
        stub_lexicon(result)
        self.assertEqual(result.name, "procedure_def")
        self.assertEqual(result.return_type.modification, TypeModification.NONE)
        self.assertEqual(result.return_type.details, BasicType.VOID)
        self.assertEqual(len(result.arguments), 0)
        self.assertEqual(result.modification, FunctionModification.NONE)
        self.assertEqual(len(result.overloading), 0)

        self.assertEqual(result.template, None)
        self.assertTrue(result.is_definition)
        self.assertFalse(result.is_declaration)
        # to compare platform independent
        self.assertEqual(result.body.replace("\r\n", "\n"),
                         """{
    int a = 6*8;
    int b = 2*a;
    for(int i = 0; i < 5; i++)
    {
        a += b*i;
    }
}""")

    def test_function_modification(self):
        with self.subTest("mod_constexpr_func"):
            node = find_by_name(self.cursor, "mod_constexpr_func")
            result = FunctionInfo.from_cursor(node)
            stub_lexicon(result)
            self.assertEqual(result.name, "mod_constexpr_func")
            self.assertEqual(result.return_type.modification, TypeModification.NONE)
            self.assertEqual(result.return_type.details, BasicType.INT)
            self.assertEqual(len(result.arguments), 1)
            self.assertEqual(result.arguments[0].name, "a")
            self.assertEqual(result.arguments[0].type.details, BasicType.INT)
            self.assertEqual(len(result.overloading), 0)
            self.assertEqual(result.template, None)
            self.assertFalse(result.is_definition)
            self.assertTrue(result.is_declaration)
            self.assertTrue(result.modification.is_constexpr)

        with self.subTest("mod_consteval_func"):
            node = find_by_name(self.cursor, "mod_consteval_func")
            result = FunctionInfo.from_cursor(node)
            stub_lexicon(result)
            self.assertEqual(result.name, "mod_consteval_func")
            self.assertEqual(result.return_type.modification, TypeModification.NONE)
            self.assertEqual(result.return_type.details, BasicType.INT)
            self.assertEqual(len(result.arguments), 1)
            self.assertEqual(result.arguments[0].name, "a")
            self.assertEqual(result.arguments[0].type.details, BasicType.INT)
            self.assertEqual(len(result.overloading), 0)
            self.assertEqual(result.template, None)
            self.assertFalse(result.is_definition)
            self.assertTrue(result.is_declaration)
            self.assertTrue(result.modification.is_consteval)

        with self.subTest("mod_static_func"):
            node = find_by_name(self.cursor, "mod_static_func")
            result = FunctionInfo.from_cursor(node)
            stub_lexicon(result)
            self.assertEqual(result.name, "mod_static_func")
            self.assertEqual(result.return_type.modification, TypeModification.NONE)
            self.assertEqual(result.return_type.details, BasicType.INT)
            self.assertEqual(len(result.arguments), 1)
            self.assertEqual(result.arguments[0].name, "a")
            self.assertEqual(result.arguments[0].type.details, BasicType.INT)
            self.assertEqual(len(result.overloading), 0)
            self.assertEqual(result.template, None)
            self.assertFalse(result.is_definition)
            self.assertTrue(result.is_declaration)
            self.assertTrue(result.modification.is_static)

        with self.subTest("mod_inline_func"):
            node = find_by_name(self.cursor, "mod_inline_func")
            result = FunctionInfo.from_cursor(node)
            stub_lexicon(result)
            self.assertEqual(result.name, "mod_inline_func")
            self.assertEqual(result.return_type.modification, TypeModification.NONE)
            self.assertEqual(result.return_type.details, BasicType.INT)
            self.assertEqual(len(result.arguments), 1)
            self.assertEqual(result.arguments[0].name, "a")
            self.assertEqual(result.arguments[0].type.details, BasicType.INT)
            self.assertEqual(len(result.overloading), 0)
            self.assertEqual(result.template, None)
            self.assertFalse(result.is_definition)
            self.assertTrue(result.is_declaration)
            self.assertTrue(result.modification.is_inline)

        with self.subTest("mod_noexcept_func"):
            node = find_by_name(self.cursor, "mod_noexcept_func")
            result = FunctionInfo.from_cursor(node)
            stub_lexicon(result)
            self.assertEqual(result.name, "mod_noexcept_func")
            self.assertEqual(result.return_type.modification, TypeModification.NONE)
            self.assertEqual(result.return_type.details, BasicType.INT)
            self.assertEqual(len(result.arguments), 1)
            self.assertEqual(result.arguments[0].name, "a")
            self.assertEqual(result.arguments[0].type.details, BasicType.INT)
            self.assertEqual(len(result.overloading), 0)
            self.assertEqual(result.template, None)
            self.assertFalse(result.is_definition)
            self.assertTrue(result.is_declaration)
            self.assertTrue(result.modification.is_noexcept)

    def test_function_namespace_return(self):
        file = SourceFile(os.path.dirname(__file__) + r"/source_files/simple_functions.hpp")
        result: FunctionInfo = file.content[11]
        self.assertEqual(result.name, "namespace_return_func")
        self.assertEqual(result.return_type.modification, TypeModification.NONE)
        self.assertEqual(len(result.arguments), 1)
        self.assertEqual(result.arguments[0].name, "a")
        self.assertEqual(result.arguments[0].type.details, BasicType.INT)
        self.assertEqual(len(result.overloading), 0)
        self.assertEqual(result.template, None)
        self.assertFalse(result.is_definition)
        self.assertTrue(result.is_declaration)
        self.assertEqual(result.modification, FunctionModification.NONE)
        self.assertEqual(result.return_type.name, "typereal")
        self.assertEqual(result.return_type.namespaces, ["test_namespace"])

    def test_function_modification_attribute(self):
        node = find_by_name(self.cursor, "attribute_func_1")
        result = FunctionInfo.from_cursor(node)
        self.assertTrue(result.modification.is_static)
        self.assertEqual(result.modification, FunctionModification.NONE | FunctionModification.STATIC)

        node = find_by_name(self.cursor, "attribute_func_2")
        result = FunctionInfo.from_cursor(node)
        self.assertTrue(result.modification.is_inline)
        self.assertEqual(result.modification, FunctionModification.NONE | FunctionModification.INLINE)

        node = find_by_name(self.cursor, "attribute_func_3")
        result = FunctionInfo.from_cursor(node)
        self.assertTrue(result.modification.is_constexpr)
        self.assertEqual(result.modification, FunctionModification.NONE | FunctionModification.CONSTEXPR)

        node = find_by_name(self.cursor, "attribute_func_4")
        result = FunctionInfo.from_cursor(node)
        self.assertTrue(result.modification.is_static)
        self.assertTrue(result.modification.is_inline)
        self.assertEqual(result.modification, FunctionModification.NONE
                         | FunctionModification.STATIC
                         | FunctionModification.INLINE)

    def test_consteval_body(self):
        node = find_by_name(self.cursor, "mod_consteval_if_func")
        result = FunctionInfo.from_cursor(node)
        self.assertFalse(result.modification.is_consteval)

    def test_noexcept_func(self):
        node = find_by_name(self.cursor, "mod_simple_noexcept_func")
        result = FunctionInfo.from_cursor(node)
        self.assertTrue(result.modification.is_noexcept)

        node = find_by_name(self.cursor, "mod_multiple_noexcept_func")
        result = FunctionInfo.from_cursor(node)
        self.assertTrue(result.modification.is_noexcept)
        self.assertTrue(result.modification.is_static)

        node = find_by_name(self.cursor, "mod_arg_noexcept_func")
        result = FunctionInfo.from_cursor(node)
        self.assertTrue(result.modification.is_noexcept)
        self.assertTrue(result.modification.is_static)
        self.assertEqual(result.modification.noexcept_value, "1==5||(2==2)")


class TestFunctionsTemplate(unittest.TestCase):

    def setUp(self):
        index = clang.cindex.Index.create()
        self.cursor = index.parse(
            os.path.dirname(__file__) + r"/source_files/template_functions.hpp"
        ).cursor

    def test_common_function_template(self):
        node = find_by_name(self.cursor, "simple_function_typename")
        result = FunctionInfo.from_cursor(node)
        stub_lexicon(result)
        self.assertFalse(result.template is None)
        self.assertFalse(result.template.is_empty)
        self.assertEqual(result.name, "simple_function_typename")
        self.assertEqual(len(result.arguments), 2)
        self.assertEqual(result.arguments[0].name, "a")
        self.assertEqual(result.arguments[0].type.details, BasicType.FLOAT)
        self.assertEqual(result.arguments[0].type.modification, TypeModification.NONE)
        self.assertEqual(result.arguments[0].default_value, None)
        self.assertEqual(result.arguments[1].name, "b")
        self.assertEqual(result.arguments[1].type.details, BasicType.BOOL)
        self.assertEqual(result.arguments[1].type.modification, TypeModification.NONE)
        self.assertEqual(result.arguments[1].default_value, "true")
        self.assertEqual(result.return_type.details, BasicType.DOUBLE)
        self.assertEqual(result.body, None)
        self.assertEqual(len(result.template.parameters), 1)
        self.assertEqual(len(result.template.specialisations), 0)
        self.assertEqual(result.template.parameters[0].name, "T")
        self.assertEqual(result.template.parameters[0].specifier, "typename")
        self.assertEqual(result.template.parameters[0].default_value, None)
        self.assertEqual(result.template.requires, None)
        self.assertEqual(result.requires, None)

        node = find_by_name(self.cursor, "simple_function_class")
        result = FunctionInfo.from_cursor(node)
        stub_lexicon(result)
        self.assertFalse(result.template is None)
        self.assertFalse(result.template.is_empty)
        self.assertEqual(result.name, "simple_function_class")
        self.assertEqual(len(result.arguments), 2)
        self.assertEqual(result.arguments[0].name, "a")
        self.assertEqual(result.arguments[0].type.details, BasicType.FLOAT)
        self.assertEqual(result.arguments[0].type.modification, TypeModification.NONE)
        self.assertEqual(result.arguments[0].default_value, None)
        self.assertEqual(result.arguments[1].name, "b")
        self.assertEqual(result.arguments[1].type.details, BasicType.BOOL)
        self.assertEqual(result.arguments[1].type.modification, TypeModification.NONE)
        self.assertEqual(result.arguments[1].default_value, "true")
        self.assertEqual(result.return_type.details, BasicType.DOUBLE)
        self.assertEqual(result.body, None)
        self.assertEqual(len(result.template.parameters), 1)
        self.assertEqual(len(result.template.specialisations), 0)
        self.assertEqual(result.template.parameters[0].name, "T")
        self.assertEqual(result.template.parameters[0].specifier, "class")
        self.assertEqual(result.template.parameters[0].default_value, None)
        self.assertEqual(result.template.requires, None)
        self.assertEqual(result.requires, None)

    def test_complex_function_template(self):
        node = find_by_name(self.cursor, "complex_function")
        result = FunctionInfo.from_cursor(node)
        stub_lexicon(result)
        self.assertFalse(result.template is None)
        self.assertFalse(result.template.is_empty)
        self.assertEqual(result.name, "complex_function")
        self.assertEqual(len(result.arguments), 4)
        self.assertEqual(result.arguments[0].name, "a")
        self.assertEqual(result.arguments[0].type.details, BasicType.FLOAT)
        self.assertEqual(result.arguments[0].type.modification, TypeModification.NONE)
        self.assertEqual(result.arguments[0].default_value, None)
        self.assertEqual(result.arguments[1].name, "b")
        self.assertEqual(result.arguments[1].type.details.name, "T")
        self.assertTrue(result.arguments[1].type.is_generic)
        self.assertEqual(result.arguments[1].type.modification, TypeModification.NONE)
        self.assertEqual(result.arguments[1].default_value, None)
        self.assertEqual(result.arguments[2].name, "c")
        self.assertEqual(result.arguments[2].type.details.name, "P")
        self.assertTrue(result.arguments[2].type.is_generic)
        self.assertTrue(result.arguments[2].type.modification.is_reference)
        self.assertEqual(result.arguments[2].default_value, None)
        self.assertEqual(result.arguments[3].name, "d")
        self.assertEqual(result.arguments[3].type.details, BasicType.CHAR)
        self.assertFalse(result.arguments[3].type.is_generic)
        self.assertEqual(result.arguments[3].type.modification, TypeModification.NONE)
        self.assertEqual(result.arguments[3].default_value, r"'3'")
        self.assertTrue(result.return_type.is_generic)
        self.assertTrue(result.return_type.details.name, "T")
        self.assertEqual(result.body, None)
        self.assertEqual(len(result.template.parameters), 2)
        self.assertEqual(len(result.template.specialisations), 0)
        self.assertEqual(result.template.parameters[0].name, "T")
        self.assertEqual(result.template.parameters[0].specifier, "typename")
        self.assertEqual(result.template.parameters[0].default_value, None)
        self.assertEqual(result.template.parameters[1].name, "P")
        self.assertEqual(result.template.parameters[1].specifier, "typename")
        self.assertEqual(result.template.parameters[1].default_value, "const float")
        self.assertEqual(len(result.template.specialisations), 0)
        self.assertEqual(result.template.requires, None)
        self.assertEqual(result.requires, None)

    def test_specialisation_function_template(self):
        node = find_by_name(self.cursor, "specialisation_function")
        result = FunctionInfo.from_cursor(node)
        stub_lexicon(result)
        self.assertFalse(result.template is None)
        self.assertEqual(result.requires, None)
        self.assertTrue(result.template.is_empty)
        self.assertEqual(result.name, "specialisation_function")
        self.assertEqual(len(result.arguments), 4)
        self.assertEqual(result.arguments[0].name, "a")
        self.assertEqual(result.arguments[0].type.details, BasicType.FLOAT)
        self.assertEqual(result.arguments[0].type.modification, TypeModification.NONE)
        self.assertEqual(result.arguments[0].default_value, None)
        self.assertEqual(result.arguments[1].name, "b")
        self.assertEqual(result.arguments[1].type.details, BasicType.INT)
        self.assertFalse(result.arguments[1].type.is_generic)
        self.assertTrue(result.arguments[1].type.modification.is_pointer)
        self.assertEqual(result.arguments[1].default_value, None)
        self.assertEqual(result.arguments[2].name, "c")
        self.assertEqual(result.arguments[2].type.details, BasicType.FLOAT)
        self.assertFalse(result.arguments[2].type.is_generic)
        self.assertTrue(result.arguments[2].type.modification.is_reference)
        self.assertEqual(result.arguments[2].default_value, None)
        self.assertEqual(result.arguments[3].name, "d")
        self.assertEqual(result.arguments[3].type.details, BasicType.CHAR)
        self.assertFalse(result.arguments[3].type.is_generic)
        self.assertEqual(result.arguments[3].type.modification, TypeModification.NONE)
        self.assertEqual(result.arguments[3].default_value, None)
        self.assertFalse(result.return_type.is_generic)
        self.assertTrue(result.return_type.details, BasicType.INT)
        self.assertTrue(result.return_type.modification.is_pointer)
        self.assertTrue(result.return_type.modification.is_const)
        self.assertEqual(result.body, None)
        self.assertEqual(result.template.requires, None)


class TestFunctionsOverload(unittest.TestCase):
    def setUp(self):
        index = clang.cindex.Index.create()
        self.cursor = index.parse(os.path.dirname(__file__) + r"/source_files/overload.hpp").cursor
        self.file = SourceFile(self.cursor)

    def test_simple_overload(self):
        base: FunctionInfo = self.file.content[4]
        self.assertEqual(len(base.overloading_family), 4)
        self.assertEqual(base.overloading_family[0], base)
        self.assertEqual(base.overloading_family[1], self.file.content[1])
        self.assertEqual(base.overloading_family[2], self.file.content[2])
        self.assertEqual(base.overloading_family[3], self.file.content[3])

        self.assertEqual(len(base.overloading), 3)
        self.assertEqual(base.overloading[0], self.file.content[1])
        self.assertEqual(base.overloading[1], self.file.content[2])
        self.assertEqual(base.overloading[2], self.file.content[3])

    def test_bad_overload(self):
        base: FunctionInfo = self.file.content[5]
        with self.assertRaises(CodeError):
            base.overloading_family # noqa
        base: FunctionInfo = self.file.content[7]
        with self.assertRaises(CodeError):
            base.overloading_family # noqa

    def test_template_overload_and_spec(self):
        base: FunctionInfo = self.file.content[10]
        self.assertEqual(len(base.overloading_family), 4)
        self.assertEqual(base.overloading_family[0], base)
        self.assertEqual(base.overloading_family[1], self.file.content[11])
        self.assertEqual(base.overloading_family[2], self.file.content[12])
        self.assertEqual(base.overloading_family[3], self.file.content[13])
        self.assertEqual(len(base.template.specialisations), 1)
        self.assertEqual(base.template.specialisations[0], self.file.content[14])
        base: FunctionInfo = self.file.content[12]
        self.assertEqual(len(base.template.specialisations), 1)
        self.assertEqual(base.template.specialisations[0], self.file.content[15])

        base: FunctionInfo = self.file.content[11]
        self.assertEqual(len(base.template.specialisations), 0)
