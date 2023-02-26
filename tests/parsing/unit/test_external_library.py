import unittest
import os
from devana.syntax_abstraction.organizers.sourcemodule import SourceFile
from devana.syntax_abstraction.classinfo import ClassInfo, FieldInfo, MethodInfo, AccessSpecifier
from devana.syntax_abstraction.typeexpression import BasicType, TypeExpression


class TestParsingStandardLibrary(unittest.TestCase):
    """Tests parsing external source based on std lib."""

    def setUp(self):
        module_path = os.path.dirname(__file__) + r"/source_files/std_lib.hpp"
        self.file = SourceFile(module_path)

    def test_simple_field(self):
        c: ClassInfo = self.file.content[1]
        with self.subTest("string"):
            field: FieldInfo = c.content[0]
            self.assertEqual(field.name, "a")
            self.assertEqual(field.type.name, "string")
            self.assertEqual(field.type.namespaces, ["std"])
            self.assertTrue(field.type.modification.is_no_modification)
        with self.subTest("simple vector"):
            field: FieldInfo = c.content[1]
            self.assertEqual(field.name, "b")
            self.assertEqual(field.type.name, "vector<float>")
            self.assertEqual(field.type.namespaces, ["std"])
            self.assertTrue(field.type.modification.is_no_modification)
            self.assertEqual(len(field.type.template_arguments), 1)
            self.assertEqual(field.type.template_arguments[0].details, BasicType.FLOAT)
        with self.subTest("complex type vector"):
            expected_type = self.file.content[0]
            field: FieldInfo = c.content[2]
            self.assertEqual(field.name, "c")
            self.assertEqual(field.type.name, "vector<TestElement>")
            self.assertEqual(field.type.namespaces, ["std"])
            self.assertTrue(field.type.modification.is_no_modification)
            self.assertEqual(len(field.type.template_arguments), 1)
            self.assertEqual(field.type.template_arguments[0].details, expected_type)
        with self.subTest("nested vector"):
            field: FieldInfo = c.content[3]
            self.assertEqual(field.name, "d")
            self.assertEqual(field.type.name, "const vector<vector<double>>*")
            self.assertEqual(field.type.namespaces, ["std"])
            self.assertTrue(field.type.modification.is_const)
            self.assertTrue(field.type.modification.is_pointer)
            self.assertEqual(len(field.type.template_arguments), 1)
            element: TypeExpression = field.type.template_arguments[0]
            self.assertEqual(element.name, "vector<double>")
            self.assertEqual(len(element.template_arguments), 1)
            self.assertEqual(element.template_arguments[0].details, BasicType.DOUBLE)
        with self.subTest("shared pointer"):
            field: FieldInfo = c.content[4]
            self.assertEqual(field.name, "e")
            self.assertEqual(field.type.name, "shared_ptr<TestElement>")
            self.assertEqual(field.type.namespaces, ["std"])
            self.assertTrue(field.type.modification.is_no_modification)
            self.assertEqual(len(field.type.template_arguments), 1)
            element: TypeExpression = field.type.template_arguments[0]
            self.assertEqual(element.name, "TestElement")

    def test_method_return_type(self):
        method: MethodInfo = self.file.content[1].content[5]
        self.assertEqual(method.name, "foo")
        self.assertEqual(method.namespaces, [])
        return_type = method.return_type
        self.assertEqual(return_type.namespaces, ["std"])
        self.assertEqual(return_type.name, "vector<vector<double>>")
        self.assertEqual(len(return_type.template_arguments), 1)
        vector: TypeExpression = return_type.template_arguments[0]
        self.assertEqual(vector.namespaces, ["std"])
        self.assertEqual(vector.name, "vector<double>")
        self.assertEqual(len(vector.template_arguments), 1)
        nested: TypeExpression = vector.template_arguments[0]
        self.assertEqual(nested.name, "double")

    def test_method_argument(self):
        method: MethodInfo = self.file.content[1].content[6]
        self.assertEqual(method.name, "bar")
        self.assertEqual(method.namespaces, [])
        self.assertEqual(len(method.arguments), 1)
        argument_type = method.arguments[0].type
        self.assertEqual(argument_type.name, "const vector<vector<double>>&")
        self.assertEqual(argument_type.namespaces, ["std"])
        self.assertEqual(len(argument_type.template_arguments), 1)
        vector: TypeExpression = argument_type.template_arguments[0]
        self.assertEqual(vector.namespaces, ["std"])
        self.assertEqual(vector.name, "vector<double>")
        self.assertEqual(len(vector.template_arguments), 1)
        nested: TypeExpression = vector.template_arguments[0]
        self.assertEqual(nested.name, "double")

    def test_generic_argument(self):
        c: ClassInfo = self.file.content[2]
        field: FieldInfo = c.content[1]
        self.assertEqual(field.name, "b")
        self.assertEqual(field.type.name, "vector<T>")
        self.assertEqual(field.type.namespaces, ["std"])
        self.assertEqual(len(field.type.template_arguments), 1)
        element: TypeExpression = field.type.template_arguments[0]
        self.assertTrue(element.is_generic)
        self.assertEqual(element.name, "T")

        # self.assertTrue(field.type.modification.is_no_modification)

    def test_template_argument(self):
        c: ClassInfo = self.file.content[3]
        field: FieldInfo = c.content[0]
        self.assertEqual(field.name, "a")
        self.assertEqual(field.type.name, "TestTemplateElement<const string*>")
        self.assertEqual(len(field.type.template_arguments), 1)
        element: TypeExpression = field.type.template_arguments[0]
        self.assertEqual(element.name, "const string*")
        self.assertTrue(element.modification.is_pointer)
        self.assertTrue(element.modification.is_const)
        self.assertEqual(element.namespaces, ["std"])

    def test_simple_inheritance(self):
        c: ClassInfo = self.file.content[4]
        self.assertEqual(c.name, "TestInheritance")
        self.assertEqual(len(c.inheritance.type_parents), 1)
        self.assertEqual(c.inheritance.type_parents[0].access_specifier, AccessSpecifier.PUBLIC)
        self.assertEqual(c.inheritance.type_parents[0].type.name, "string")
        self.assertEqual(c.inheritance.type_parents[0].namespaces, ["std"])

    def test_template_inheritance(self):
        c: ClassInfo = self.file.content[5]
        self.assertEqual(c.name, "TestTemplateInheritance")
        self.assertEqual(len(c.inheritance.type_parents), 1)
        self.assertEqual(c.inheritance.type_parents[0].access_specifier, AccessSpecifier.PUBLIC)
        self.assertEqual(c.inheritance.type_parents[0].type.name, "enable_shared_from_this")
        self.assertEqual(c.inheritance.type_parents[0].namespaces, ["std"])
        self.assertEqual(len(c.inheritance.type_parents[0].template_arguments), 1)
        self.assertEqual(c.inheritance.type_parents[0].template_arguments[0].name, "TestTemplateInheritance")
        self.assertEqual(c.inheritance.type_parents[0].template_arguments[0].details, c)
