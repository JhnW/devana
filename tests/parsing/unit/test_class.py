import unittest
import clang.cindex
import clang
import os
from tests.helpers import find_by_name
from devana.syntax_abstraction.typeexpression import BasicType, TypeModification
from devana.syntax_abstraction.classinfo import *
from devana.syntax_abstraction.functioninfo import FunctionModification
from devana.syntax_abstraction.organizers.sourcefile import SourceFile


class TestClassBasic(unittest.TestCase):

    def setUp(self):
        index = clang.cindex.Index.create()
        self.cursor = index.parse(os.path.dirname(__file__) + r"/source_files/core_class.hpp").cursor

    def test_struct_simple_def(self):
        node = find_by_name(self.cursor, "SimpleStructTest")
        result = ClassInfo.from_cursor(node)
        self.assertEqual(result.name, "SimpleStructTest")
        self.assertTrue(result.is_struct)
        self.assertFalse(result.is_class)
        self.assertTrue(result.is_definition)
        self.assertFalse(result.is_declaration)
        self.assertEqual(result.namespace, "SimpleStructTest")
        self.assertEqual(result.inheritance, None)
        self.assertEqual(len(result.content), 5)
        self.assertEqual(len(result.constructors), 0)
        self.assertEqual(result.destructor, None)
        self.assertEqual(len(result.operators), 0)
        self.assertEqual(len(result.fields), 4)
        self.assertEqual(len(result.methods), 1)
        self.assertEqual(len(result.public), 5)
        self.assertEqual(len(result.private), 0)
        self.assertEqual(len(result.protected), 0)
        self.assertEqual(result.template, None)

        element: FieldInfo = result.content[0]
        self.assertEqual(element.name, "a")
        self.assertEqual(element.access_specifier, AccessSpecifier.PUBLIC)
        self.assertEqual(element.type.details, BasicType.DOUBLE)
        self.assertEqual(element.type.modification, TypeModification.NONE)
        element: FieldInfo = result.content[1]
        self.assertEqual(element.name, "b")
        self.assertEqual(element.access_specifier, AccessSpecifier.PUBLIC)
        self.assertEqual(element.type.details, BasicType.INT)
        self.assertTrue(element.type.modification.is_const)
        element: FieldInfo = result.content[2]
        self.assertEqual(element.name, "c")
        self.assertEqual(element.access_specifier, AccessSpecifier.PUBLIC)
        self.assertEqual(element.type.details, BasicType.VOID)
        self.assertTrue(element.type.modification.is_pointer)
        element: FieldInfo = result.content[3]
        self.assertEqual(element.name, "d")
        self.assertEqual(element.access_specifier, AccessSpecifier.PUBLIC)
        self.assertEqual(element.type.details, BasicType.BOOL)
        self.assertTrue(element.type.modification.is_static)
        element: MethodInfo = result.content[4]
        self.assertEqual(element.name, "foo")
        self.assertEqual(element.access_specifier, AccessSpecifier.PUBLIC)
        self.assertEqual(len(element.arguments), 1)
        self.assertEqual(element.arguments[0].name, "a")
        self.assertEqual(element.return_type.modification, TypeModification.NONE)
        self.assertEqual(element.return_type.details, BasicType.FLOAT)
        self.assertTrue(element.modification, FunctionModification.NONE)

    def test_class_simple_def(self):
        node = find_by_name(self.cursor, "SimpleClassTest")
        result = ClassInfo.from_cursor(node)
        self.assertEqual(result.name, "SimpleClassTest")
        self.assertFalse(result.is_struct)
        self.assertTrue(result.is_class)
        self.assertTrue(result.is_definition)
        self.assertFalse(result.is_declaration)
        self.assertEqual(result.namespace, "SimpleClassTest")
        self.assertEqual(result.inheritance, None)
        self.assertEqual(len(result.content), 6)
        self.assertEqual(len(result.constructors), 0)
        self.assertEqual(result.destructor, None)
        self.assertEqual(len(result.operators), 0)
        self.assertEqual(len(result.fields), 5)
        self.assertEqual(len(result.methods), 1)
        self.assertEqual(len(result.public), 0)
        self.assertEqual(len(result.private), 6)
        self.assertEqual(len(result.protected), 0)
        self.assertEqual(result.template, None)

        element: FieldInfo = result.content[0]
        self.assertEqual(element.name, "a")
        self.assertEqual(element.access_specifier, AccessSpecifier.PRIVATE)
        self.assertEqual(element.type.details, BasicType.DOUBLE)
        self.assertEqual(element.type.modification, TypeModification.NONE)
        element: FieldInfo = result.content[1]
        self.assertEqual(element.name, "b")
        self.assertEqual(element.access_specifier, AccessSpecifier.PRIVATE)
        self.assertEqual(element.type.details, BasicType.INT)
        self.assertTrue(element.type.modification.is_const)
        element: FieldInfo = result.content[2]
        self.assertEqual(element.name, "c")
        self.assertEqual(element.access_specifier, AccessSpecifier.PRIVATE)
        self.assertEqual(element.type.details, BasicType.VOID)
        self.assertTrue(element.type.modification.is_pointer)
        element: FieldInfo = result.content[3]
        self.assertEqual(element.name, "d")
        self.assertEqual(element.access_specifier, AccessSpecifier.PRIVATE)
        self.assertEqual(element.type.details, BasicType.BOOL)
        self.assertTrue(element.type.modification.is_static)
        element: MethodInfo = result.content[4]
        self.assertEqual(element.name, "foo")
        self.assertEqual(element.access_specifier, AccessSpecifier.PRIVATE)
        self.assertEqual(len(element.arguments), 1)
        self.assertEqual(element.arguments[0].name, "a")
        self.assertEqual(element.return_type.modification, TypeModification.NONE)
        self.assertEqual(element.return_type.details, BasicType.FLOAT)
        self.assertTrue(element.modification, FunctionModification.NONE)
        element: FieldInfo = result.content[5]
        self.assertEqual(element.name, "e")
        self.assertEqual(element.access_specifier, AccessSpecifier.PRIVATE)
        self.assertEqual(element.type.details, BasicType.FLOAT)
        self.assertTrue(element.type.modification.is_mutable)

    def test_final_class(self):
        node = find_by_name(self.cursor, "FinalClass")
        result = ClassInfo.from_cursor(node)
        self.assertTrue(result.is_final)

    def test_class_sections(self):
        node = find_by_name(self.cursor, "ClassSections")
        result = ClassInfo.from_cursor(node)
        self.assertEqual(len(result.sections), 5)

        section = result.sections[0]
        with self.subTest(section):
            self.assertEqual(len(section.content), 2)
            self.assertEqual(section.type, AccessSpecifier.PRIVATE)
            self.assertTrue(section.is_unnamed)
            self.assertEqual(section.content[0].access_specifier, AccessSpecifier.PRIVATE)
            self.assertEqual(section.content[0].name, "foo1")
            self.assertEqual(section.content[1].access_specifier, AccessSpecifier.PRIVATE)
            self.assertEqual(section.content[1].name, "a")

        section = result.sections[1]
        with self.subTest(section):
            self.assertEqual(len(section.content), 2)
            self.assertEqual(section.type, AccessSpecifier.PRIVATE)
            self.assertFalse(section.is_unnamed)
            self.assertEqual(section.content[0].access_specifier, AccessSpecifier.PRIVATE)
            self.assertEqual(section.content[0].name, "foo2")
            self.assertEqual(section.content[1].access_specifier, AccessSpecifier.PRIVATE)
            self.assertEqual(section.content[1].name, "b")

        section = result.sections[2]
        with self.subTest(section):
            self.assertEqual(len(section.content), 2)
            self.assertEqual(section.type, AccessSpecifier.PUBLIC)
            self.assertFalse(section.is_unnamed)
            self.assertEqual(section.content[0].access_specifier, AccessSpecifier.PUBLIC)
            self.assertEqual(section.content[0].name, "foo3")
            self.assertEqual(section.content[1].access_specifier, AccessSpecifier.PUBLIC)
            self.assertEqual(section.content[1].name, "c")

        section = result.sections[3]
        with self.subTest(section):
            self.assertEqual(len(section.content), 2)
            self.assertEqual(section.type, AccessSpecifier.PROTECTED)
            self.assertFalse(section.is_unnamed)
            self.assertEqual(section.content[0].access_specifier, AccessSpecifier.PROTECTED)
            self.assertEqual(section.content[0].name, "foo4")
            self.assertEqual(section.content[1].access_specifier, AccessSpecifier.PROTECTED)
            self.assertEqual(section.content[1].name, "d")

        section = result.sections[4]
        with self.subTest(section):
            self.assertEqual(len(section.content), 2)
            self.assertEqual(section.type, AccessSpecifier.PUBLIC)
            self.assertFalse(section.is_unnamed)
            self.assertEqual(section.content[0].access_specifier, AccessSpecifier.PUBLIC)
            self.assertEqual(section.content[0].name, "foo5")
            self.assertEqual(section.content[1].access_specifier, AccessSpecifier.PUBLIC)
            self.assertEqual(section.content[1].name, "e")

    def test_class_operators(self):
        node = find_by_name(self.cursor, "ClassOperators")
        result = ClassInfo.from_cursor(node)
        self.assertEqual(len(result.content), 45)
        for op in result.content:
            self.assertTrue(op.type.is_operator, f"{op}")

    def test_class_constructors(self):
        node = find_by_name(self.cursor, "ClassContructors")
        result = ClassInfo.from_cursor(node)
        self.assertEqual(len(result.content), 11)

        c: ConstructorInfo = result.content[0]
        with self.subTest(c):
            self.assertEqual(c.type, MethodType.CONSTRUCTOR)
            self.assertEqual(c.name, "ClassContructors")
            self.assertEqual(len(c.arguments), 1)
            self.assertEqual(c.arguments[0].name, "b")
            self.assertEqual(c.arguments[0].type.details, BasicType.FLOAT)
            self.assertEqual(len(c.initializer_list), 4)
            self.assertEqual(c.initializer_list[0].name, "a")
            self.assertEqual(c.initializer_list[0].value, "0.5+1")
            self.assertEqual(c.initializer_list[1].name, "b")
            self.assertEqual(c.initializer_list[1].value, "7+b")
            self.assertEqual(c.initializer_list[2].name, "c")
            self.assertEqual(c.initializer_list[2].value, r'":)"')
            self.assertEqual(c.initializer_list[3].name, "d")
            self.assertEqual(c.initializer_list[3].value, "{1,2,3,4,9.5}")
            self.assertEqual(c.access_specifier, AccessSpecifier.PUBLIC)

        c = result.content[1]
        with self.subTest(c):
            self.assertEqual(c.name, "ClassContructors")
            self.assertEqual(c.type, MethodType.COPY_CONSTRUCTOR)
            self.assertEqual(len(c.initializer_list), 0)
            self.assertEqual(len(c.arguments), 1)
            self.assertEqual(c.arguments[0].name, "src")
            self.assertTrue(c.arguments[0].type.modification.is_const)
            self.assertTrue(c.arguments[0].type.modification.is_reference)
            self.assertTrue(c.arguments[0].type.name, "ClassContructors")

        c = result.content[2]
        with self.subTest(c):
            self.assertEqual(c.name, "ClassContructors")
            self.assertEqual(c.type, MethodType.MOVE_CONSTRUCTOR)
            self.assertEqual(len(c.initializer_list), 0)
            self.assertEqual(len(c.arguments), 1)
            self.assertEqual(c.arguments[0].name, "src")
            self.assertFalse(c.arguments[0].type.modification.is_reference)
            self.assertTrue(c.arguments[0].type.modification.is_rvalue_ref)
            self.assertTrue(c.arguments[0].type.modification.is_const)
            self.assertTrue(c.arguments[0].type.name, "ClassContructors")

        c = result.content[3]
        with self.subTest(c):
            self.assertEqual(c.name, "ClassContructors")
            self.assertEqual(c.type, MethodType.CONSTRUCTOR)
            self.assertEqual(len(c.initializer_list), 0)
            self.assertEqual(len(c.arguments), 1)
            self.assertEqual(c.arguments[0].name, "a")
            self.assertEqual(c.arguments[0].type.details, BasicType.DOUBLE)
            self.assertTrue(c.modification.is_explicit)

        c: MethodInfo = result.content[4]
        with self.subTest(c):
            self.assertEqual(c.name, "operator=")
            self.assertEqual(c.type, MethodType.COPY_ASSIGNMENT)
            self.assertEqual(len(c.arguments), 1)
            self.assertEqual(c.arguments[0].name, "src")
            self.assertTrue(c.arguments[0].type.modification.is_const)
            self.assertTrue(c.arguments[0].type.modification.is_reference)
            self.assertEqual(c.modification.is_const, False)
            self.assertTrue(c.arguments[0].type.name, "ClassContructors")
            self.assertEqual(c.return_type.name, "ClassContructors&")

        c: MethodInfo = result.content[5]
        with self.subTest(c):
            self.assertEqual(c.name, "operator=")
            self.assertEqual(c.type, MethodType.MOVE_ASSIGNMENT)
            self.assertEqual(len(c.arguments), 1)
            self.assertEqual(c.arguments[0].name, "src")
            self.assertTrue(c.arguments[0].type.modification.is_const)
            self.assertTrue(c.arguments[0].type.modification.is_rvalue_ref)
            self.assertTrue(c.arguments[0].type.name, "ClassContructors")
            self.assertEqual(c.return_type.name, "ClassContructors&")

        c: DestructorInfo = result.content[6]
        with self.subTest(c):
            self.assertEqual(c.name, "~ClassContructors")
            self.assertEqual(c.type, MethodType.DESTRUCTOR)
            self.assertEqual(len(c.arguments), 0)
            self.assertTrue(c.modification.is_virtual)

    def test_method_modification(self):
        index = clang.cindex.Index.create()
        cursor = index.parse(os.path.dirname(__file__) + r"/source_files/core_class.hpp").cursor
        file = SourceFile(cursor)
        result: ClassInfo = file.content[14]
        self.assertEqual(result.name, "MethodMods")

        method: MethodInfo = result.content[1]
        self.assertEqual(method.modification, FunctionModification.NONE | FunctionModification.DEFAULT)
        method: MethodInfo = result.content[2]
        self.assertEqual(method.modification, FunctionModification.NONE | FunctionModification.DELETE)
        method: MethodInfo = result.content[3]
        self.assertEqual(method.modification, FunctionModification.NONE | FunctionModification.VIRTUAL)
        method: MethodInfo = result.content[4]
        self.assertEqual(method.modification, FunctionModification.NONE | FunctionModification.PURE_VIRTUAL
                         | FunctionModification.VIRTUAL)
        method: MethodInfo = result.content[5]
        self.assertEqual(method.modification, FunctionModification.NONE | FunctionModification.OVERRIDE)
        method: MethodInfo = result.content[6]
        self.assertEqual(method.modification, FunctionModification.NONE | FunctionModification.FINAL)
        method: MethodInfo = result.content[7]
        self.assertEqual(method.modification, FunctionModification.NONE | FunctionModification.STATIC)
        method: MethodInfo = result.content[8]
        self.assertEqual(method.modification, FunctionModification.NONE | FunctionModification.VOLATILE)
        method: MethodInfo = result.content[9]
        self.assertEqual(method.modification, FunctionModification.NONE | FunctionModification.CONST)

    def test_default_field_value(self):
        node = find_by_name(self.cursor, "DefaultFieldsValue")
        result = ClassInfo.from_cursor(node)
        field: FieldInfo = result.content[0]
        with self.subTest(field.name):
            self.assertEqual(field.name, "default_value")
            self.assertEqual(field.type.details, BasicType.DOUBLE)
            self.assertEqual(field.type.modification, TypeModification.NONE | TypeModification.CONST)
            self.assertEqual(field.default_value, "(1.0+0.7)/4.25")
        field: FieldInfo = result.content[1]
        with self.subTest(field.name):
            self.assertEqual(field.name, "default_constexpr_value")
            self.assertEqual(field.type.details, BasicType.FLOAT)
            self.assertEqual(field.type.modification, TypeModification.NONE
                             | TypeModification.STATIC
                             | TypeModification.CONSTEXPR)
            self.assertEqual(field.default_value, "15.75f")


class TestInheritance(unittest.TestCase):

    def setUp(self):
        index = clang.cindex.Index.create()
        self.cursor = index.parse(os.path.dirname(__file__) + r"/source_files/core_class.hpp").cursor
        self.file = SourceFile(self.cursor)

    def test_simple_child(self):
        result: ClassInfo = self.file.content[8]
        self.assertEqual(result.name, "SimpleChild")
        self.assertTrue(result.is_class)
        self.assertEqual(len(result.content), 1)
        self.assertEqual(result.content[0].name, "SimpleChild")
        self.assertEqual(result.content[0].type, MethodType.CONSTRUCTOR)
        self.assertEqual(len(result.inheritance.type_parents), 1)
        self.assertEqual(result.inheritance.type_parents[0].type, self.file.content[6])
        self.assertEqual(result.inheritance.type_parents[0].type.name, "Parent1")
        self.assertEqual(result.inheritance.type_parents[0].access_specifier, AccessSpecifier.PUBLIC)
        self.assertFalse(result.inheritance.type_parents[0].is_virtual)

    def test_init_child(self):
        result: ClassInfo = self.file.content[9]
        self.assertEqual(result.name, "InitChild")
        self.assertTrue(result.is_class)
        self.assertEqual(len(result.content), 1)
        self.assertEqual(result.content[0].name, "InitChild")
        self.assertEqual(result.content[0].type, MethodType.CONSTRUCTOR)
        self.assertEqual(len(result.inheritance.type_parents), 1)
        self.assertEqual(result.inheritance.type_parents[0].type, self.file.content[7])
        self.assertEqual(result.inheritance.type_parents[0].type.name, "Parent2")
        self.assertEqual(result.inheritance.type_parents[0].access_specifier, AccessSpecifier.PUBLIC)
        self.assertFalse(result.inheritance.type_parents[0].is_virtual)
        constructor: ConstructorInfo = result.content[0]
        self.assertEqual(len(constructor.initializer_list), 1)
        self.assertEqual(constructor.initializer_list[0].name, "Parent2")
        self.assertEqual(constructor.initializer_list[0].value, "6")

    def test_multi_child(self):
        result: ClassInfo = self.file.content[11]
        self.assertEqual(result.name, "MultiChild")
        self.assertTrue(result.is_class)
        self.assertEqual(len(result.inheritance.type_parents), 2)
        self.assertEqual(result.inheritance.type_parents[0].type, self.file.content[6])
        self.assertEqual(result.inheritance.type_parents[0].type.name, "Parent1")
        self.assertEqual(result.inheritance.type_parents[0].access_specifier, AccessSpecifier.PRIVATE)
        self.assertFalse(result.inheritance.type_parents[0].is_virtual)
        self.assertEqual(result.inheritance.type_parents[1].type, self.file.content[7])
        self.assertEqual(result.inheritance.type_parents[1].type.name, "Parent2")
        self.assertEqual(result.inheritance.type_parents[1].access_specifier, AccessSpecifier.PUBLIC)
        self.assertFalse(result.inheritance.type_parents[1].is_virtual)
        self.assertEqual(len(result.content), 2)
        constructor: ConstructorInfo = result.content[0]
        self.assertEqual(constructor.name, "MultiChild")
        self.assertEqual(len(constructor.arguments), 1)
        self.assertEqual(constructor.arguments[0].name, "a")
        self.assertEqual(constructor.arguments[0].type.details, BasicType.INT)
        self.assertEqual(len(constructor.initializer_list), 3)
        self.assertEqual(constructor.initializer_list[0].name, "Parent1")
        self.assertEqual(constructor.initializer_list[0].value, "")
        self.assertEqual(constructor.initializer_list[1].name, "Parent2")
        self.assertEqual(constructor.initializer_list[1].value, "a")
        self.assertEqual(constructor.initializer_list[2].name, "c")
        self.assertEqual(constructor.initializer_list[2].value, "a+7")

    def test_virtual_child(self):
        result: ClassInfo = self.file.content[12]
        self.assertEqual(result.name, "VirtualChild")
        self.assertTrue(result.is_class)
        self.assertEqual(len(result.inheritance.type_parents), 1)
        self.assertEqual(result.inheritance.type_parents[0].type, self.file.content[7])
        self.assertEqual(result.inheritance.type_parents[0].type.name, "Parent2")
        self.assertEqual(result.inheritance.type_parents[0].access_specifier, AccessSpecifier.PUBLIC)
        self.assertTrue(result.inheritance.type_parents[0].is_virtual)
        self.assertEqual(len(result.content), 1)
        constructor: ConstructorInfo = result.content[0]
        self.assertEqual(constructor.name, "VirtualChild")
        self.assertEqual(len(constructor.arguments), 0)

    def test_no_spec_child(self):
        result: ClassInfo = self.file.content[10]
        self.assertEqual(result.name, "NoSpecChild")
        self.assertTrue(result.is_class)
        self.assertEqual(len(result.inheritance.type_parents), 1)
        self.assertEqual(result.inheritance.type_parents[0].type, self.file.content[6])
        self.assertEqual(result.inheritance.type_parents[0].type.name, "Parent1")
        self.assertEqual(result.inheritance.type_parents[0].access_specifier, AccessSpecifier.PRIVATE)
        self.assertFalse(result.inheritance.type_parents[0].is_virtual)

    def test_no_spec_virtual_child(self):
        result: ClassInfo = self.file.content[13]
        self.assertEqual(result.name, "NoSpecVirtualChild")
        self.assertTrue(result.is_class)
        self.assertEqual(len(result.inheritance.type_parents), 1)
        self.assertEqual(result.inheritance.type_parents[0].type, self.file.content[7])
        self.assertEqual(result.inheritance.type_parents[0].type.name, "Parent2")
        self.assertEqual(result.inheritance.type_parents[0].access_specifier, AccessSpecifier.PRIVATE)
        self.assertTrue(result.inheritance.type_parents[0].is_virtual)


class TestClassTemplate(unittest.TestCase):

    def setUp(self):
        index = clang.cindex.Index.create()
        self.cursor = index.parse(os.path.dirname(__file__) + r"/source_files/template_class.hpp").cursor

    def test_simple_template_class(self):
        node = find_by_name(self.cursor, "simple_template_struct_1")
        result = ClassInfo.from_cursor(node)
        self.assertEqual(result.name, "simple_template_struct_1")
        self.assertTrue(result.is_struct)
        self.assertFalse(result.template is None)
        self.assertEqual(len(result.template.parameters), 1)
        self.assertEqual(result.template.parameters[0].name, "T")
        self.assertEqual(result.template.parameters[0].specifier, "typename")
        self.assertEqual(result.template.parameters[0].default_value, None)
        self.assertEqual(len(result.content), 1)
        self.assertEqual(result.content[0].name, "template_field")
        self.assertEqual(result.content[0].access_specifier, AccessSpecifier.PUBLIC)
        self.assertEqual(result.content[0].type.details.name, "T")
        self.assertEqual(result.content[0].type.modification, TypeModification.NONE)
        self.assertTrue(result.content[0].type.is_generic)

        node = find_by_name(self.cursor, "simple_template_struct_2")
        result = ClassInfo.from_cursor(node)
        self.assertEqual(result.name, "simple_template_struct_2")
        self.assertTrue(result.is_struct)
        self.assertFalse(result.template is None)
        self.assertEqual(len(result.template.parameters), 1)
        self.assertEqual(result.template.parameters[0].name, "T")
        self.assertEqual(result.template.parameters[0].specifier, "class")
        self.assertEqual(result.template.parameters[0].default_value, None)
        self.assertEqual(len(result.content), 1)
        self.assertEqual(result.content[0].name, "template_field")
        self.assertEqual(result.content[0].access_specifier, AccessSpecifier.PUBLIC)
        self.assertEqual(result.content[0].type.details.name, "T")
        self.assertEqual(result.content[0].type.modification, TypeModification.NONE)
        self.assertTrue(result.content[0].type.is_generic)

        node = find_by_name(self.cursor, "simple_template_class_1")
        result = ClassInfo.from_cursor(node)
        self.assertEqual(result.name, "simple_template_class_1")
        self.assertTrue(result.is_class)
        self.assertFalse(result.template is None)
        self.assertEqual(len(result.template.parameters), 1)
        self.assertEqual(result.template.parameters[0].name, "T")
        self.assertEqual(result.template.parameters[0].specifier, "typename")
        self.assertEqual(result.template.parameters[0].default_value, None)
        self.assertEqual(len(result.content), 1)
        self.assertEqual(result.content[0].name, "template_field")
        self.assertEqual(result.content[0].access_specifier, AccessSpecifier.PRIVATE)
        self.assertEqual(result.content[0].type.details.name, "T")
        self.assertEqual(result.content[0].type.modification, TypeModification.NONE)
        self.assertTrue(result.content[0].type.is_generic)

        node = find_by_name(self.cursor, "simple_template_class_2")
        result = ClassInfo.from_cursor(node)
        self.assertEqual(result.name, "simple_template_class_2")
        self.assertTrue(result.is_class)
        self.assertFalse(result.template is None)
        self.assertEqual(len(result.template.parameters), 1)
        self.assertEqual(result.template.parameters[0].name, "T")
        self.assertEqual(result.template.parameters[0].specifier, "class")
        self.assertEqual(result.template.parameters[0].default_value, None)
        self.assertEqual(len(result.content), 1)
        self.assertEqual(result.content[0].name, "template_field")
        self.assertEqual(result.content[0].access_specifier, AccessSpecifier.PRIVATE)
        self.assertEqual(result.content[0].type.details.name, "T")
        self.assertEqual(result.content[0].type.modification, TypeModification.NONE)
        self.assertTrue(result.content[0].type.is_generic)

    def test_complex_template_class(self):
        node = find_by_name(self.cursor, "template_class_complex")
        result = ClassInfo.from_cursor(node)

        self.assertTrue(result.is_class)
        self.assertFalse(result.template is None)
        self.assertEqual(result.name, "template_class_complex")
        self.assertEqual(len(result.template.parameters), 2)
        self.assertEqual(result.template.parameters[0].name, "T")
        self.assertEqual(result.template.parameters[0].specifier, "typename")
        self.assertEqual(result.template.parameters[0].default_value, None)
        self.assertEqual(result.template.parameters[1].name, "P")
        self.assertEqual(result.template.parameters[1].specifier, "typename")
        self.assertEqual(result.template.parameters[1].default_value, "const float")
        self.assertEqual(len(result.content), 16)

        content: ConstructorInfo = result.content[1]
        with self.subTest(content):
            self.assertEqual(content.template, None)
            self.assertEqual(content.access_specifier, AccessSpecifier.PUBLIC)
            self.assertEqual(content.name, "template_class_complex")
            self.assertEqual(len(content.initializer_list), 0)
            self.assertEqual(len(content.arguments), 2)
            self.assertEqual(content.arguments[0].name, "a")
            self.assertTrue(content.arguments[0].type.modification.is_pointer)
            self.assertTrue(content.arguments[0].type.is_generic)
            self.assertEqual(content.arguments[0].type.name, "T*")
            self.assertEqual(content.arguments[1].name, "b")
            self.assertEqual(content.arguments[1].type.modification, TypeModification.NONE)
            self.assertFalse(content.arguments[1].type.is_generic)
            self.assertEqual(content.arguments[1].type.details, BasicType.CHAR)

        content: DestructorInfo = result.content[2]
        with self.subTest(content):
            self.assertEqual(content.template, None)
            self.assertEqual(content.access_specifier, AccessSpecifier.PUBLIC)
            self.assertEqual(content.name, "~template_class_complex")

        content: FieldInfo = result.content[3]
        with self.subTest(content):
            self.assertEqual(content.name, "parm_1")
            self.assertEqual(content.access_specifier, AccessSpecifier.PUBLIC)
            self.assertTrue(content.type.modification.is_const)
            self.assertTrue(content.type.is_generic)
            self.assertEqual(content.type.details.name, "T")

        content: FieldInfo = result.content[4]
        with self.subTest(content):
            self.assertEqual(content.name, "parm_2")
            self.assertEqual(content.access_specifier, AccessSpecifier.PUBLIC)
            self.assertTrue(content.type.modification.is_reference)
            self.assertTrue(content.type.is_generic)
            self.assertEqual(content.type.details.name, "T")

        content: FieldInfo = result.content[5]
        with self.subTest(content):
            self.assertEqual(content.name, "parm_3")
            self.assertEqual(content.access_specifier, AccessSpecifier.PUBLIC)
            self.assertTrue(content.type.modification.is_pointer)
            self.assertFalse(content.type.is_generic)
            self.assertEqual(content.type.details, BasicType.FLOAT)

        content: FieldInfo = result.content[6]
        with self.subTest(content):
            self.assertEqual(content.name, "parm_4")
            self.assertEqual(content.access_specifier, AccessSpecifier.PUBLIC)
            self.assertTrue(content.type.modification.is_pointer)
            self.assertTrue(content.type.is_generic)
            self.assertEqual(content.type.details.name, "T")

        content: FieldInfo = result.content[7]
        with self.subTest(content):
            self.assertEqual(content.name, "parm_5")
            self.assertEqual(content.access_specifier, AccessSpecifier.PUBLIC)
            self.assertTrue(content.type.modification.is_const)
            self.assertTrue(content.type.modification.is_reference)
            self.assertTrue(content.type.is_generic)
            self.assertEqual(content.type.details.name, "T")

        content: FieldInfo = result.content[8]
        with self.subTest(content):
            self.assertEqual(content.name, "parm_6")
            self.assertEqual(content.access_specifier, AccessSpecifier.PUBLIC)
            self.assertTrue(content.type.modification.is_const)
            self.assertTrue(content.type.modification.is_pointer)
            self.assertTrue(content.type.is_generic)
            self.assertEqual(content.type.details.name, "T")

        content: FieldInfo = result.content[9]
        with self.subTest(content):
            self.assertEqual(content.name, "parm_7")
            self.assertEqual(content.access_specifier, AccessSpecifier.PUBLIC)
            self.assertTrue(content.type.modification.is_static)
            self.assertTrue(content.type.is_generic)
            self.assertEqual(content.type.details.name, "T")

        content: FieldInfo = result.content[10]
        with self.subTest(content):
            self.assertEqual(content.name, "parm_8")
            self.assertEqual(content.access_specifier, AccessSpecifier.PUBLIC)
            self.assertTrue(content.type.modification.is_static)
            self.assertTrue(content.type.modification.is_reference)
            self.assertTrue(content.type.is_generic)
            self.assertEqual(content.type.details.name, "T")

        content: FieldInfo = result.content[11]
        with self.subTest(content):
            self.assertEqual(content.name, "parm_9")
            self.assertEqual(content.access_specifier, AccessSpecifier.PUBLIC)
            self.assertTrue(content.type.modification.is_static)
            self.assertTrue(content.type.modification.is_pointer)
            self.assertTrue(content.type.is_generic)
            self.assertEqual(content.type.details.name, "T")

        content: MethodInfo = result.content[12]
        with self.subTest(content):
            self.assertEqual(content.name, "method_1")
            self.assertEqual(content.access_specifier, AccessSpecifier.PUBLIC)
            self.assertTrue(content.template is None)
            self.assertEqual(len(content.arguments), 1)
            self.assertEqual(content.arguments[0].name, "a")
            self.assertEqual(content.arguments[0].type.details, BasicType.FLOAT)
            self.assertTrue(content.arguments[0].type.modification.is_no_modification)
            self.assertEqual(content.return_type.details.name, "P")
            self.assertTrue(content.return_type.modification.is_pointer)

        content: MethodInfo = result.content[14]
        with self.subTest(content):
            self.assertEqual(content.name, "method_2")
            self.assertEqual(content.access_specifier, AccessSpecifier.PRIVATE)
            self.assertTrue(content.template is None)
            self.assertEqual(len(content.arguments), 2)
            self.assertEqual(content.arguments[0].name, "a")
            self.assertEqual(content.arguments[0].type.details.name, "T")
            self.assertTrue(content.arguments[0].type.modification.is_const)
            self.assertEqual(content.arguments[1].name, "b")
            self.assertEqual(content.arguments[1].type.details.name, "P")
            self.assertTrue(content.arguments[1].type.modification.is_const)
            self.assertTrue(content.arguments[1].type.modification.is_reference)
            self.assertEqual(content.return_type.details, BasicType.INT)
            self.assertTrue(content.return_type.modification.is_no_modification)

        content: MethodInfo = result.content[15]
        with self.subTest(content):
            self.assertEqual(content.name, "method_3")
            self.assertEqual(content.access_specifier, AccessSpecifier.PRIVATE)
            self.assertEqual(len(content.arguments), 2)
            self.assertEqual(content.arguments[0].name, "a")
            self.assertEqual(content.arguments[0].type.details.name, "T")
            self.assertTrue(content.arguments[0].type.modification.is_const)
            self.assertEqual(content.arguments[1].name, "b")
            self.assertEqual(content.arguments[1].type.details.name, "D")
            self.assertTrue(content.arguments[1].type.modification.is_pointer)
            self.assertEqual(content.return_type.details.name, "D")
            self.assertTrue(content.return_type.modification.is_pointer)
            self.assertNotEqual(content.template, None)
            self.assertEqual(len(content.template.parameters), 1)
            self.assertEqual(content.template.parameters[0].name, "D")
            self.assertEqual(content.template.parameters[0].default_value, None)

    def test_struct_varidaic_template(self):
        node = find_by_name(self.cursor, "struct_varidaic_template")
        result = ClassInfo.from_cursor(node)
        self.assertTrue(result.is_struct)
        self.assertFalse(result.template is None)
        self.assertEqual(result.name, "struct_varidaic_template")
        self.assertEqual(len(result.template.parameters), 3)
        self.assertEqual(result.template.parameters[0].name, "T")
        self.assertEqual(result.template.parameters[0].specifier, "typename")
        self.assertEqual(result.template.parameters[0].default_value, None)
        self.assertFalse(result.template.parameters[0].is_variadic)
        self.assertEqual(result.template.parameters[1].name, "P")
        self.assertEqual(result.template.parameters[1].specifier, "typename")
        self.assertEqual(result.template.parameters[1].default_value, None)
        self.assertFalse(result.template.parameters[1].is_variadic)
        self.assertEqual(result.template.parameters[2].name, "Ts")
        self.assertEqual(result.template.parameters[2].specifier, "typename")
        self.assertEqual(result.template.parameters[2].default_value, None)
        self.assertTrue(result.template.parameters[2].is_variadic)

    def test_multiple_pointer_type_template(self):
        node = find_by_name(self.cursor, "multiple_pointer_struct")
        result = ClassInfo.from_cursor(node)
        self.assertTrue(result.is_struct)
        self.assertFalse(result.template is None)
        self.assertEqual(result.name, "multiple_pointer_struct")
        self.assertEqual(len(result.template.parameters), 1)
        self.assertEqual(result.template.parameters[0].name, "T")
        self.assertEqual(len(result.content), 1)
        content = result.content[0]
        self.assertEqual(content.access_specifier, AccessSpecifier.PUBLIC)
        self.assertTrue(content.type.modification.is_pointer)
        self.assertTrue(content.type.is_generic)
        self.assertEqual(content.type.modification.pointer_order, 2)
        self.assertEqual(content.type.details.name, "T")


class TestClassTemplatePartial(unittest.TestCase):

    def setUp(self):
        index = clang.cindex.Index.create()
        self.cursor = index.parse(os.path.dirname(__file__) + r"/source_files/template_class.hpp").cursor
        self.nodes = []
        for c in self.cursor.get_children():
            if c.spelling == "template_struct" or c.spelling == "multiple_types":
                self.nodes.append(c)

    def test_base_template(self):
        node = self.nodes[0]
        result = ClassInfo.from_cursor(node)
        self.assertEqual(result.name, "template_struct")
        self.assertTrue(result.is_struct)
        self.assertFalse(result.template is None)
        self.assertEqual(len(result.template.parameters), 2)
        self.assertEqual(result.template.parameters[0].name, "T")
        self.assertEqual(result.template.parameters[0].specifier, "typename")
        self.assertEqual(result.template.parameters[0].default_value, None)
        self.assertEqual(result.template.parameters[1].name, "P")
        self.assertEqual(result.template.parameters[1].specifier, "typename")
        self.assertEqual(result.template.parameters[1].default_value, None)
        self.assertEqual(len(result.content), 2)
        self.assertEqual(result.content[0].name, "a")
        self.assertTrue(result.content[0].type.is_generic)
        self.assertEqual(result.content[0].type.name, "T")
        self.assertTrue(result.content[0].type.modification.is_no_modification)
        self.assertEqual(result.content[1].name, "b")
        self.assertTrue(result.content[1].type.is_generic)
        self.assertEqual(result.content[1].type.name, "P*")
        self.assertTrue(result.content[1].type.modification.is_pointer)
        self.assertEqual(len(result.template.specialisations), 0)

    def test_simple_partial_template(self):
        node = self.nodes[1]
        result = ClassInfo.from_cursor(node)
        self.assertEqual(result.name, "template_struct")
        self.assertTrue(result.is_struct)
        self.assertFalse(result.template is None)
        self.assertEqual(len(result.template.parameters), 1)
        self.assertEqual(result.template.parameters[0].name, "P")
        self.assertEqual(result.template.parameters[0].specifier, "typename")
        self.assertEqual(result.template.parameters[0].default_value, None)
        self.assertEqual(len(result.content), 2)
        self.assertEqual(result.content[0].name, "a")
        self.assertFalse(result.content[0].type.is_generic)
        self.assertEqual(result.content[0].type.details, BasicType.DOUBLE)
        self.assertTrue(result.content[0].type.modification.is_const)
        self.assertTrue(result.content[0].type.modification.is_reference)
        self.assertEqual(result.content[1].name, "b")
        self.assertTrue(result.content[1].type.is_generic)
        self.assertEqual(result.content[1].type.name, "P*")
        self.assertTrue(result.content[1].type.modification.is_pointer)

        self.assertEqual(len(result.template.specialisation_values), 2)
        self.assertEqual(result.template.specialisation_values[0].name, "const double&")
        self.assertEqual(result.template.specialisation_values[0].details, BasicType.DOUBLE)
        self.assertTrue(result.template.specialisation_values[0].modification.is_const)
        self.assertTrue(result.template.specialisation_values[0].modification.is_reference)
        self.assertFalse(result.template.specialisation_values[0].is_generic)
        self.assertEqual(result.template.specialisation_values[1].name, "P")
        self.assertTrue(result.template.specialisation_values[1].modification.is_no_modification)
        self.assertTrue(result.template.specialisation_values[1].is_generic)

    def test_generic_type_modification_template(self):
        node = self.nodes[2]
        result = ClassInfo.from_cursor(node)
        self.assertEqual(result.name, "template_struct")
        self.assertTrue(result.is_struct)
        self.assertFalse(result.template is None)
        self.assertEqual(len(result.template.parameters), 1)
        self.assertEqual(result.template.parameters[0].name, "P")
        self.assertEqual(result.template.parameters[0].specifier, "typename")
        self.assertEqual(result.template.parameters[0].default_value, None)
        self.assertEqual(len(result.content), 2)
        self.assertEqual(result.content[0].name, "a")
        self.assertTrue(result.content[0].type.is_generic)
        self.assertEqual(result.content[0].type.details.name, "P")
        self.assertTrue(result.content[0].type.modification.is_pointer)
        self.assertEqual(result.content[1].name, "b")
        self.assertTrue(result.content[1].type.is_generic)
        self.assertEqual(result.content[1].type.name, "P*")
        self.assertTrue(result.content[1].type.modification.is_pointer)

        self.assertEqual(len(result.template.specialisation_values), 2)
        self.assertEqual(result.template.specialisation_values[0].name, "P")
        self.assertTrue(result.template.specialisation_values[0].is_generic)
        self.assertTrue(result.template.specialisation_values[0].modification.is_pointer)
        self.assertEqual(result.template.specialisation_values[1].name, "P")
        self.assertTrue(result.template.specialisation_values[1].is_generic)
        self.assertFalse(result.template.specialisation_values[1].modification.is_pointer)

    def test_generic_type_empty_template(self):
        node = self.nodes[3]
        result = ClassInfo.from_cursor(node)
        self.assertEqual(result.name, "template_struct")
        self.assertTrue(result.is_struct)
        self.assertFalse(result.template is None)
        self.assertEqual(len(result.template.parameters), 0)
        self.assertEqual(len(result.content), 2)
        self.assertEqual(result.content[0].name, "a")
        self.assertFalse(result.content[0].type.is_generic)
        self.assertEqual(result.content[0].type.details, BasicType.DOUBLE)
        self.assertTrue(result.content[0].type.modification.is_no_modification)
        self.assertEqual(result.content[1].name, "b")
        self.assertFalse(result.content[1].type.is_generic)
        self.assertEqual(result.content[1].type.details, BasicType.CHAR)
        self.assertTrue(result.content[1].type.modification.is_pointer)

        self.assertEqual(len(result.template.specialisation_values), 2)
        self.assertEqual(result.template.specialisation_values[0].details, BasicType.DOUBLE)
        self.assertFalse(result.template.specialisation_values[0].is_generic)
        self.assertTrue(result.template.specialisation_values[0].modification.is_no_modification)
        self.assertEqual(result.template.specialisation_values[1].details, BasicType.CHAR)
        self.assertFalse(result.template.specialisation_values[1].is_generic)
        self.assertTrue(result.template.specialisation_values[1].modification.is_no_modification)

    def test_multiple_types_sec_template(self):
        node = self.nodes[5]
        result = ClassInfo.from_cursor(node)
        self.assertEqual(result.name, "multiple_types")
        self.assertTrue(result.is_struct)
        self.assertFalse(result.template is None)
        self.assertEqual(len(result.template.parameters), 2)

        self.assertEqual(len(result.template.specialisation_values), 3)
        self.assertEqual(result.template.specialisation_values[0].details.name, "P")
        self.assertTrue(result.template.specialisation_values[0].is_generic)
        self.assertTrue(result.template.specialisation_values[0].modification.is_no_modification)
        self.assertEqual(result.template.specialisation_values[1].details.name, "T")
        self.assertTrue(result.template.specialisation_values[1].is_generic)
        self.assertTrue(result.template.specialisation_values[1].modification.is_no_modification)
        self.assertEqual(result.template.specialisation_values[2].details.name, "P")
        self.assertTrue(result.template.specialisation_values[2].is_generic)
        self.assertTrue(result.template.specialisation_values[2].modification.is_pointer)


class TestClassLexicon(unittest.TestCase):

    def setUp(self):
        index = clang.cindex.Index.create()
        self.cursor = index.parse(os.path.dirname(__file__) + r"/source_files/advanced_class.hpp").cursor
        self.file = SourceFile.from_cursor(self.cursor)
        self.assertEqual(len(self.file.content), 4)

    def test_class_function(self):
        result: FunctionInfo = self.file.content[1]
        with self.subTest(result.name):
            self.assertEqual(result.name, "functionClassArg")
            self.assertEqual(result.return_type.details, BasicType.VOID)
            self.assertEqual(result.return_type.modification, TypeModification.NONE)
            self.assertEqual(len(result.arguments), 1)
            self.assertEqual(result.arguments[0].name, "a")
            self.assertTrue(result.arguments[0].type.modification.is_const)
            self.assertTrue(result.arguments[0].type.modification.is_reference)
            self.assertEqual(result.arguments[0].type.details, self.file.content[0])

        result: FunctionInfo = self.file.content[2]
        with self.subTest(result.name):
            self.assertEqual(result.name, "functionClassReturn")
            self.assertEqual(result.return_type.details, self.file.content[0])
            self.assertTrue(result.return_type.modification.is_pointer)
            self.assertEqual(len(result.arguments), 0)

    def test_class_field(self):
        result: ClassInfo = self.file.content[3]
        self.assertEqual(result.name, "StorageClass")
        self.assertEqual(result.content[0].type.details, self.file.content[0])
