import unittest
import os
from devana.syntax_abstraction.organizers.sourcemodule import SourceModule, ModuleFilter
from devana.syntax_abstraction.classinfo import ClassInfo
from devana.syntax_abstraction.functioninfo import FunctionInfo
from devana.syntax_abstraction.variable import GlobalVariable


class TestSourceModule(unittest.TestCase):

    def setUp(self):
        self.module_path = os.path.dirname(__file__) + r"/source_files/multiple_files/module"

    def test_simple_creation(self):
        module = SourceModule("Test_1", self.module_path)
        self.assertEqual(len(module.files), 5)

    def test_filter_allowed(self):
        f = ModuleFilter()
        f.allowed_filter = [r"\.h", r"\.hpp"]
        module = SourceModule("Test_1", self.module_path, f)
        self.assertEqual(len(module.files), 3)

    def test_filter_forbidden(self):
        f = ModuleFilter()
        f.forbidden_filter = [r"\.h", r"\.hpp"]
        module = SourceModule("Test_1", self.module_path, f)
        self.assertEqual(len(module.files), 2)


class TestSourceModuleSearchingTypes(unittest.TestCase):

    def setUp(self):
        module_path = os.path.dirname(__file__) + r"/source_files/multiple_files/module"
        f = ModuleFilter()
        f.allowed_filter = [r"inc_types\.hpp", r"src_types\.cpp"]
        self.module = SourceModule("Test_1", module_path, f)
        self.assertEqual(len(self.module.files), 2)
        inc_file = next(file for file in self.module.files if file.name == "inc_types.hpp")
        self.src_file = next(file for file in self.module.files if file.name == "src_types.cpp")
        self.expected_type: ClassInfo = inc_file.content[0]
        self.expected_type_namespace: ClassInfo = inc_file.content[1].content[0]
        self.expected_type_namespace_deep: ClassInfo = inc_file.content[1].content[1].content[0]

    def test_variable_type_another_file(self):
        variable: GlobalVariable = self.src_file.content[0]
        self.assertEqual(variable.type.details, self.expected_type)

    def test_variable_type_another_file_namespace(self):
        variable: GlobalVariable = self.src_file.content[1]
        self.assertEqual(variable.type.details, self.expected_type_namespace)

    def test_function_type_another_file(self):
        function: FunctionInfo = self.src_file.content[2]
        self.assertEqual(function.arguments[0].type.details, self.expected_type)
        function: FunctionInfo = self.src_file.content[3]
        self.assertEqual(function.return_type.details, self.expected_type)

    def test_function_type_another_file_namespace(self):
        function: FunctionInfo = self.src_file.content[4]
        self.assertEqual(function.arguments[0].type.details, self.expected_type_namespace)
        function: FunctionInfo = self.src_file.content[5]
        self.assertEqual(function.return_type.details, self.expected_type_namespace)
        function: FunctionInfo = self.src_file.content[6]
        self.assertEqual(function.return_type.details, self.expected_type_namespace_deep)

    def test_class_inheritance_type_another_file(self):
        class_info: ClassInfo = self.src_file.content[7]
        self.assertEqual(class_info.inheritance.type_parents[0].type, self.expected_type)

    def test_class_inheritance_type_another_file_complex(self):
        class_info: ClassInfo = self.src_file.content[8]
        self.assertEqual(class_info.inheritance.type_parents[0].type, self.expected_type_namespace)
        self.assertFalse(class_info.inheritance.type_parents[0].is_virtual)
        class_info: ClassInfo = self.src_file.content[9]
        self.assertEqual(class_info.inheritance.type_parents[0].type, self.expected_type_namespace)
        self.assertTrue(class_info.inheritance.type_parents[0].is_virtual)
