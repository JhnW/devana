import unittest
import clang.cindex
import clang
import os
from devana.syntax_abstraction.organizers.sourcefile import SourceFile
from devana.syntax_abstraction.typeexpression import TypeModification
from devana.syntax_abstraction.classinfo import *
from devana.syntax_abstraction.typedefinfo import TypedefInfo


class TestTemplateAdvanced(unittest.TestCase):

    def setUp(self):
        index = clang.cindex.Index.create()
        self.cursor = index.parse(
            os.path.dirname(__file__) + r"/source_files/advanced_template.hpp"
        ).cursor
        self.file = SourceFile.from_cursor(self.cursor)
        self.assertEqual(len(self.file.content), 32)

    def test_functions_arguments(self):
        result: FunctionInfo = self.file.content[2]
        with self.subTest(result.name):
            self.assertEqual(result.name, "functionTemplateArg_1")
            self.assertEqual(result.return_type.details, BasicType.VOID)
            self.assertEqual(result.return_type.modification, TypeModification.NONE)
            self.assertEqual(len(result.arguments), 1)
            self.assertEqual(result.arguments[0].name, "a")
            self.assertTrue(result.arguments[0].type.modification.is_const)
            self.assertTrue(result.arguments[0].type.modification.is_reference)
            self.assertEqual(result.arguments[0].type.details, self.file.content[0])
            self.assertEqual(len(result.arguments[0].type.template_arguments), 1)
            self.assertEqual(result.arguments[0].type.template_arguments[0].modification, TypeModification.NONE)
            self.assertEqual(result.arguments[0].type.template_arguments[0].details, BasicType.FLOAT)
            self.assertEqual(result.arguments[0].type.template_arguments[0].template_arguments, None)

        result: FunctionInfo = self.file.content[3]
        with self.subTest(result.name):
            self.assertEqual(result.name, "functionTemplateArg_2")
            self.assertEqual(result.return_type.details, BasicType.VOID)
            self.assertEqual(result.return_type.modification, TypeModification.NONE)
            self.assertEqual(len(result.arguments), 1)
            self.assertEqual(result.arguments[0].name, "a")
            self.assertTrue(result.arguments[0].type.modification.is_const)
            self.assertTrue(result.arguments[0].type.modification.is_reference)
            self.assertEqual(result.arguments[0].type.details, self.file.content[0])
            self.assertEqual(len(result.arguments[0].type.template_arguments), 1)
            self.assertEqual(result.arguments[0].type.template_arguments[0].modification, TypeModification.NONE)
            self.assertEqual(result.arguments[0].type.template_arguments[0].details, self.file.content[0])
            self.assertEqual(len(result.arguments[0].type.template_arguments[0].template_arguments), 1)
            self.assertEqual(result.arguments[0].type.template_arguments[0].template_arguments[0].modification,
                             TypeModification.NONE)
            self.assertEqual(result.arguments[0].type.template_arguments[0].template_arguments[0].details,
                             BasicType.FLOAT)

            result: FunctionInfo = self.file.content[4]
            with self.subTest(result.name):
                self.assertEqual(result.name, "functionTemplateArg_3")
                self.assertEqual(result.return_type.details, BasicType.VOID)
                self.assertEqual(result.return_type.modification, TypeModification.NONE)
                self.assertEqual(len(result.arguments), 1)
                self.assertEqual(result.arguments[0].name, "a")
                self.assertTrue(result.arguments[0].type.modification.is_const)
                self.assertTrue(result.arguments[0].type.modification.is_reference)
                self.assertEqual(result.arguments[0].type.details, self.file.content[1])
                self.assertEqual(len(result.arguments[0].type.template_arguments), 2)
                self.assertEqual(result.arguments[0].type.template_arguments[0].modification, TypeModification.NONE)
                self.assertEqual(result.arguments[0].type.template_arguments[0].details, BasicType.FLOAT)
                self.assertTrue(result.arguments[0].type.template_arguments[1].modification.is_pointer)
                self.assertEqual(result.arguments[0].type.template_arguments[1].details, BasicType.INT)

            result: FunctionInfo = self.file.content[5]
            with self.subTest(result.name):
                self.assertEqual(result.name, "functionTemplateArg_4")
                self.assertEqual(result.return_type.details, BasicType.VOID)
                self.assertEqual(result.return_type.modification, TypeModification.NONE)
                self.assertEqual(len(result.arguments), 1)
                self.assertEqual(result.arguments[0].name, "a")
                self.assertTrue(result.arguments[0].type.modification.is_const)
                self.assertTrue(result.arguments[0].type.modification.is_reference)
                self.assertEqual(result.arguments[0].type.details, self.file.content[1])
                self.assertEqual(len(result.arguments[0].type.template_arguments), 2)
                self.assertEqual(result.arguments[0].type.template_arguments[0].modification, TypeModification.NONE)
                self.assertEqual(result.arguments[0].type.template_arguments[0].details, self.file.content[1])
                self.assertEqual(len(result.arguments[0].type.template_arguments[0].template_arguments), 2)
                self.assertEqual(result.arguments[0].type.template_arguments[0].template_arguments[0].modification,
                                 TypeModification.NONE)
                self.assertEqual(result.arguments[0].type.template_arguments[0].template_arguments[1].modification,
                                 TypeModification.NONE)
                self.assertEqual(result.arguments[0].type.template_arguments[0].template_arguments[0].details,
                                 BasicType.DOUBLE)
                self.assertEqual(result.arguments[0].type.template_arguments[0].template_arguments[1].details,
                                 BasicType.INT)

            result: FunctionInfo = self.file.content[6]
            with self.subTest(result.name):
                self.assertEqual(result.name, "functionTemplateArg_5")
                self.assertNotEqual(result.template, None)
                self.assertEqual(result.return_type.details, BasicType.VOID)
                self.assertEqual(result.return_type.modification, TypeModification.NONE)
                self.assertEqual(len(result.arguments), 1)
                self.assertEqual(result.arguments[0].name, "a")
                self.assertTrue(result.arguments[0].type.modification.is_const)
                self.assertTrue(result.arguments[0].type.modification.is_reference)
                self.assertEqual(result.arguments[0].type.details, self.file.content[0])
                self.assertEqual(len(result.arguments[0].type.template_arguments), 1)
                self.assertEqual(result.arguments[0].type.template_arguments[0].modification, TypeModification.NONE)
                self.assertEqual(result.arguments[0].type.template_arguments[0].details.name, "T")
                self.assertTrue(result.arguments[0].type.template_arguments[0].is_generic)
                self.assertEqual(result.arguments[0].type.template_arguments[0].template_arguments, None)

            result: FunctionInfo = self.file.content[7]
            with self.subTest(result.name):
                self.assertEqual(result.name, "functionTemplateArg_6")
                self.assertNotEqual(result.template, None)
                self.assertEqual(result.return_type.details, BasicType.VOID)
                self.assertEqual(result.return_type.modification, TypeModification.NONE)
                self.assertEqual(len(result.arguments), 1)
                self.assertEqual(result.arguments[0].name, "a")
                self.assertTrue(result.arguments[0].type.modification.is_const)
                self.assertTrue(result.arguments[0].type.modification.is_reference)
                self.assertEqual(result.arguments[0].type.details, self.file.content[0])
                self.assertEqual(len(result.arguments[0].type.template_arguments), 1)
                self.assertTrue(result.arguments[0].type.template_arguments[0].modification.is_const)
                self.assertEqual(result.arguments[0].type.template_arguments[0].details, self.file.content[0])
                self.assertFalse(result.arguments[0].type.template_arguments[0].is_generic)
                self.assertEqual(len(result.arguments[0].type.template_arguments[0].template_arguments), 1)

            result: FunctionInfo = self.file.content[8]
            with self.subTest(result.name):
                self.assertEqual(result.name, "functionTemplateArg_7")
                self.assertNotEqual(result.template, None)
                self.assertEqual(result.return_type.details, BasicType.VOID)
                self.assertEqual(result.return_type.modification, TypeModification.NONE)
                self.assertEqual(len(result.arguments), 1)
                self.assertEqual(result.arguments[0].name, "a")
                self.assertTrue(result.arguments[0].type.modification.is_const)
                self.assertTrue(result.arguments[0].type.modification.is_reference)
                self.assertEqual(result.arguments[0].type.details, self.file.content[0])
                self.assertEqual(len(result.arguments[0].type.template_arguments), 1)
                self.assertTrue(result.arguments[0].type.template_arguments[0].modification.is_const)
                self.assertTrue(result.arguments[0].type.template_arguments[0].modification.is_pointer)
                self.assertEqual(result.arguments[0].type.template_arguments[0].details.name, "T")
                self.assertTrue(result.arguments[0].type.template_arguments[0].is_generic)
                self.assertEqual(result.arguments[0].type.template_arguments[0].template_arguments, None)

            result: FunctionInfo = self.file.content[9]
            with self.subTest(result.name):
                self.assertEqual(result.name, "functionTemplateArg_8")
                self.assertNotEqual(result.template, None)
                self.assertEqual(result.return_type.details, BasicType.VOID)
                self.assertEqual(result.return_type.modification, TypeModification.NONE)
                self.assertEqual(len(result.arguments), 1)
                self.assertEqual(result.arguments[0].name, "a")
                self.assertTrue(result.arguments[0].type.modification.is_const)
                self.assertTrue(result.arguments[0].type.modification.is_reference)
                self.assertEqual(result.arguments[0].type.details, self.file.content[1])
                self.assertEqual(len(result.arguments[0].type.template_arguments), 2)
                self.assertEqual(result.arguments[0].type.template_arguments[0].modification, TypeModification.NONE)
                self.assertEqual(result.arguments[0].type.template_arguments[0].details, BasicType.DOUBLE)
                self.assertFalse(result.arguments[0].type.template_arguments[0].is_generic)
                self.assertEqual(result.arguments[0].type.template_arguments[0].template_arguments, None)
                self.assertEqual(result.arguments[0].type.template_arguments[1].modification, TypeModification.NONE)
                self.assertEqual(result.arguments[0].type.template_arguments[1].details.name, "T")
                self.assertTrue(result.arguments[0].type.template_arguments[1].is_generic)
                self.assertEqual(result.arguments[0].type.template_arguments[1].template_arguments, None)

    def test_functions_return(self):
        result: FunctionInfo = self.file.content[10]
        with self.subTest(result.name):
            self.assertEqual(result.name, "functionTemplateReturn_1")
            self.assertEqual(len(result.arguments), 0)
            self.assertEqual(result.return_type.details, self.file.content[0])
            self.assertEqual(len(result.return_type.template_arguments), 1)
            self.assertEqual(result.return_type.template_arguments[0].modification, TypeModification.NONE)
            self.assertEqual(result.return_type.template_arguments[0].details, BasicType.FLOAT)

        result: FunctionInfo = self.file.content[11]
        with self.subTest(result.name):
            self.assertEqual(result.name, "functionTemplateReturn_2")
            self.assertEqual(len(result.arguments), 0)
            self.assertEqual(result.return_type.details, self.file.content[0])
            self.assertEqual(len(result.return_type.template_arguments), 1)
            self.assertTrue(result.return_type.template_arguments[0].modification.is_pointer)
            self.assertEqual(result.return_type.template_arguments[0].details, BasicType.FLOAT)

        result: FunctionInfo = self.file.content[12]
        with self.subTest(result.name):
            self.assertEqual(result.name, "functionTemplateReturn_3")
            self.assertEqual(len(result.arguments), 0)
            self.assertEqual(result.return_type.details, self.file.content[0])
            self.assertTrue(result.return_type.modification.is_const)
            self.assertTrue(result.return_type.modification.is_pointer)
            self.assertEqual(len(result.return_type.template_arguments), 1)
            self.assertEqual(result.return_type.template_arguments[0].modification, TypeModification.NONE)
            self.assertEqual(result.return_type.template_arguments[0].details, BasicType.FLOAT)

        result: FunctionInfo = self.file.content[13]
        with self.subTest(result.name):
            self.assertEqual(result.name, "functionTemplateReturn_4")
            self.assertEqual(len(result.arguments), 0)
            self.assertEqual(result.return_type.details, self.file.content[0])
            self.assertEqual(len(result.return_type.template_arguments), 1)
            self.assertEqual(result.return_type.template_arguments[0].modification, TypeModification.NONE)
            self.assertEqual(result.return_type.template_arguments[0].details, self.file.content[0])
            self.assertEqual(len(result.return_type.template_arguments[0].template_arguments), 1)
            self.assertEqual(result.return_type.template_arguments[0].template_arguments[0].details, BasicType.FLOAT)

        result: FunctionInfo = self.file.content[14]
        with self.subTest(result.name):
            self.assertEqual(result.name, "functionTemplateReturn_5")
            self.assertEqual(len(result.arguments), 0)
            self.assertEqual(result.return_type.details, self.file.content[0])
            self.assertEqual(len(result.return_type.template_arguments), 1)
            self.assertEqual(result.return_type.details, self.file.content[0])
            self.assertEqual(result.return_type.template_arguments[0].modification, TypeModification.NONE)
            self.assertEqual(result.return_type.template_arguments[0].details.name, "T")

        result: FunctionInfo = self.file.content[15]
        with self.subTest(result.name):
            self.assertEqual(result.name, "functionTemplateReturn_6")
            self.assertEqual(len(result.arguments), 0)
            self.assertEqual(result.return_type.details, self.file.content[0])
            self.assertEqual(len(result.return_type.template_arguments), 1)
            self.assertEqual(result.return_type.details, self.file.content[0])
            self.assertTrue(result.return_type.template_arguments[0].modification.is_pointer)
            self.assertEqual(result.return_type.template_arguments[0].details.name, "T")

        result: FunctionInfo = self.file.content[16]
        with self.subTest(result.name):
            self.assertEqual(result.name, "functionTemplateReturn_7")
            self.assertEqual(len(result.arguments), 0)
            self.assertEqual(result.return_type.details, self.file.content[0])
            self.assertTrue(result.return_type.modification.is_const)
            self.assertTrue(result.return_type.modification.is_pointer)
            self.assertEqual(len(result.return_type.template_arguments), 1)
            self.assertEqual(result.return_type.details, self.file.content[0])
            self.assertEqual(result.return_type.template_arguments[0].modification, TypeModification.NONE)
            self.assertEqual(result.return_type.template_arguments[0].details, BasicType.FLOAT)

        result: FunctionInfo = self.file.content[17]
        with self.subTest(result.name):
            self.assertEqual(result.name, "functionTemplateReturn_8")
            self.assertEqual(len(result.arguments), 0)
            self.assertEqual(result.return_type.details, self.file.content[0])
            self.assertEqual(len(result.return_type.template_arguments), 1)
            self.assertEqual(result.return_type.template_arguments[0].details, self.file.content[0])
            self.assertEqual(len(result.return_type.template_arguments[0].template_arguments), 1)
            self.assertEqual(result.return_type.template_arguments[0].template_arguments[0].details.name, "T")

    def test_typedef(self):
        result: TypedefInfo = self.file.content[18]
        with self.subTest(result.name):
            self.assertEqual(result.name, "typedefCharArray")
            self.assertEqual(result.type_info.details, self.file.content[0])
            self.assertEqual(len(result.type_info.template_arguments), 1)
            self.assertEqual(result.type_info.template_arguments[0].details, BasicType.CHAR)
            self.assertTrue(result.type_info.template_arguments[0].modification.is_pointer)

        result: TypedefInfo = self.file.content[19]
        with self.subTest(result.name):
            self.assertEqual(result.name, "typedefCharArrayArray")
            self.assertEqual(result.type_info.details, self.file.content[0])
            self.assertEqual(len(result.type_info.template_arguments), 1)
            self.assertEqual(result.type_info.template_arguments[0].details, self.file.content[0])
            self.assertEqual(result.type_info.template_arguments[0].template_arguments[0].details, BasicType.CHAR)
            self.assertTrue(result.type_info.template_arguments[0].template_arguments[0].modification.is_pointer)

        result: FunctionInfo = self.file.content[20]
        with self.subTest(result.name):
            self.assertEqual(result.name, "typedefFunction_1")
            self.assertEqual(len(result.arguments), 1)
            self.assertEqual(result.arguments[0].type.details, self.file.content[19])
            self.assertEqual(result.arguments[0].type.modification, TypeModification.NONE)
            self.assertEqual(result.return_type.details, self.file.content[18])
            self.assertTrue(result.return_type.modification.is_pointer)

        result: FunctionInfo = self.file.content[21]
        with self.subTest(result.name):
            self.assertEqual(result.name, "typedefFunction_2")
            self.assertEqual(len(result.arguments), 1)
            self.assertEqual(result.arguments[0].type.details, self.file.content[0])
            self.assertEqual(len(result.arguments[0].type.template_arguments), 1)
            self.assertEqual(result.arguments[0].type.template_arguments[0].details, self.file.content[19])
            self.assertEqual(result.return_type.details, self.file.content[0])
            self.assertEqual(len(result.return_type.template_arguments), 1)
            self.assertEqual(result.return_type.template_arguments[0].details, self.file.content[18])

    def test_field(self):
        result: ClassInfo = self.file.content[22]
        with self.subTest(result.name):
            self.assertEqual(result.name, "FieldHolder")
            self.assertEqual(len(result.content), 1)
            self.assertEqual(result.content[0].type.details, self.file.content[0])
            self.assertEqual(len(result.content[0].type.template_arguments), 1)
            self.assertEqual(result.content[0].type.template_arguments[0].details, BasicType.FLOAT)

        result: ClassInfo = self.file.content[23]
        with self.subTest(result.name):
            self.assertEqual(result.name, "FieldHolderTemplate")
            self.assertEqual(len(result.content), 1)
            self.assertEqual(result.content[0].type.details, self.file.content[0])
            self.assertEqual(len(result.content[0].type.template_arguments), 1)
            self.assertEqual(result.content[0].type.template_arguments[0].details.name, "T")

    def test_names(self):
        result: FunctionInfo = self.file.content[3]
        self.assertEqual(result.arguments[0].type.name, "const TemplateArray<TemplateArray<float>>&")

    def test_template_pattern(self):
        result: ClassInfo = self.file.content[24]
        with self.subTest(result.name):
            self.assertEqual(result.inheritance.type_parents[0].type, self.file.content[23])
            self.assertEqual(len(result.inheritance.type_parents[0].template_arguments), 1)
            self.assertEqual(result.inheritance.type_parents[0].template_arguments[0].modification,
                             TypeModification.NONE)
            self.assertEqual(result.inheritance.type_parents[0].template_arguments[0].details, BasicType.FLOAT)
            self.assertEqual(result.inheritance.type_parents[0].template_arguments[0].template_arguments, None)
        result: ClassInfo = self.file.content[25]
        with self.subTest(result.name):
            self.assertEqual(result.inheritance.type_parents[0].type, self.file.content[23])
            self.assertEqual(len(result.inheritance.type_parents[0].template_arguments), 1)
            self.assertTrue(result.inheritance.type_parents[0].template_arguments[0].modification.is_const)
            self.assertEqual(result.inheritance.type_parents[0].template_arguments[0].template_arguments, None)
            self.assertTrue(result.inheritance.type_parents[0].template_arguments[0].is_generic)
            self.assertEqual(result.inheritance.type_parents[0].template_arguments[0].details.name, "T")

    def test_template_function_spec(self):
        result: FunctionInfo = self.file.content[27]
        self.assertEqual(result.name, "templateFunctionSpec_1")
        self.assertEqual(len(result.template.specialisation_values), 1)
        self.assertEqual(len(result.template.parameters), 0)
        self.assertEqual(result.template.specialisation_values[0].name, "FieldHolderTemplate<char>*")
        self.assertTrue(result.template.specialisation_values[0].modification.is_pointer)
        self.assertEqual(result.template.specialisation_values[0].details, self.file.content[23])
        self.assertEqual(len(result.template.specialisation_values[0].template_arguments), 1)
        self.assertEqual(result.template.specialisation_values[0].template_arguments[0].details, BasicType.CHAR)

    def test_template_method_in_no_template(self):
        result: MethodInfo = self.file.content[28].content[0]
        self.assertEqual(result.name, "templateMethodSpec_1")
        self.assertEqual(len(result.template.specialisation_values), 0)
        self.assertEqual(len(result.template.parameters), 1)

    def test_template_method_spec_outside(self):
        result: MethodInfo = self.file.content[29]
        self.assertEqual(result.name, "templateMethodSpec_1")
        self.assertEqual(len(result.template.specialisation_values), 1)
        self.assertEqual(len(result.template.parameters), 0)
        self.assertEqual(result.template.specialisation_values[0].name, "FieldHolderTemplate<char>*")
        self.assertTrue(result.template.specialisation_values[0].modification.is_pointer)
        self.assertEqual(result.template.specialisation_values[0].details, self.file.content[23])
        self.assertEqual(len(result.template.specialisation_values[0].template_arguments), 1)
        self.assertEqual(result.template.specialisation_values[0].template_arguments[0].details, BasicType.CHAR)
