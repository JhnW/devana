import unittest
from devana.code_generation.printers.default.defaultprinter import create_default_printer
from devana.code_generation.printers.configuration import AttributesCriteria, AttributeFilter
from devana.code_generation.printers.default.functionprinter import FunctionPrinter
from devana.code_generation.printers.default.variableprinter import VariablePrinter
from devana.code_generation.printers.default.basictypeprinter import BasicTypePrinter
from devana.code_generation.printers.default.typeexpressionprinter import TypeExpressionPrinter
from devana.code_generation.printers.codeprinter import CodePrinter
from devana.syntax_abstraction.functioninfo import FunctionInfo
from devana.syntax_abstraction.classinfo import ClassInfo, FieldInfo, ConstructorInfo, MethodInfo
from devana.syntax_abstraction.enuminfo import EnumInfo
from devana.syntax_abstraction.namespaceinfo import NamespaceInfo
from devana.syntax_abstraction.typeexpression import TypeExpression, BasicType
from devana.syntax_abstraction.variable import Variable
from devana.syntax_abstraction.attribute import AttributeDeclaration, Attribute
from devana.code_generation.printers.default.attributeprinter import AttributePrinter, AttributeDeclarationPrinter


class TestAttributeCriteria(unittest.TestCase):

    @staticmethod
    def attribute_eq(attr_1: Attribute, attr_2: Attribute) -> bool:
        return attr_1.parent == attr_2.parent and attr_1.name == attr_2.name \
               and attr_1.namespace == attr_2.namespace and attr_1.arguments == attr_2.arguments

    @staticmethod
    def attribute_decl_eq(attr_1: AttributeDeclaration, attr_2: AttributeDeclaration) -> bool:
        decl_eq: bool = attr_1.parent == attr_2.parent and attr_1.using_namespace == attr_2.using_namespace
        if len(attr_1.attributes) != len(attr_2.attributes):
            return False
        attr_eq: bool = True
        for i in range(len(attr_1.attributes)):
            attr_eq &= TestAttributeCriteria.attribute_eq(attr_1.attributes[i], attr_2.attributes[i])

        return attr_eq and decl_eq

    def test_attribute_criteria_using_namespace_positive(self):
        criteria = AttributesCriteria(names=None, namespaces=AttributeFilter(["nn1"]))
        attributes = [AttributeDeclaration([Attribute("test_1")], "nn1"),
                      AttributeDeclaration([Attribute("test_2")]),
                      AttributeDeclaration([Attribute("test_3")], "nn2")]
        result = criteria.filter(attributes)
        self.assertEqual(2, len(result))
        self.assertTrue(self.attribute_decl_eq(attributes[0], result[0]))
        self.assertTrue(self.attribute_decl_eq(attributes[1], result[1]))

    def test_attribute_criteria_using_namespace_negative(self):
        criteria = AttributesCriteria(names=None, namespaces=AttributeFilter(["nn1"], True))
        attributes = [AttributeDeclaration([Attribute("test_1")], "nn1"),
                      AttributeDeclaration([Attribute("test_2")]),
                      AttributeDeclaration([Attribute("test_3")], "nn2")]
        result = criteria.filter(attributes)
        self.assertEqual(2, len(result))
        self.assertTrue(self.attribute_decl_eq(attributes[1], result[0]))
        self.assertTrue(self.attribute_decl_eq(attributes[2], result[1]))

    def test_attribute_criteria_namespace_positive(self):
        criteria = AttributesCriteria(names=None, namespaces=AttributeFilter(["nn1"]))
        attributes = [AttributeDeclaration([Attribute("test_1", "nn1")]),
                      AttributeDeclaration([Attribute("test_2")]),
                      AttributeDeclaration([Attribute("test_3", "nn2")])]
        result = criteria.filter(attributes)
        self.assertEqual(2, len(result))
        self.assertTrue(self.attribute_decl_eq(attributes[0], result[0]))
        self.assertTrue(self.attribute_decl_eq(attributes[1], result[1]))

    def test_attribute_criteria_namespace_negative(self):
        criteria = AttributesCriteria(names=None, namespaces=AttributeFilter(["nn1"], True))
        attributes = [AttributeDeclaration([Attribute("test_1", "nn1")]),
                      AttributeDeclaration([Attribute("test_2")]),
                      AttributeDeclaration([Attribute("test_3", "nn2")])]
        result = criteria.filter(attributes)
        self.assertEqual(2, len(result))
        self.assertTrue(self.attribute_decl_eq(attributes[1], result[0]))
        self.assertTrue(self.attribute_decl_eq(attributes[2], result[1]))

    def test_attribute_criteria_name_positive(self):
        criteria = AttributesCriteria(names=AttributeFilter(["test_1"]), namespaces=None)
        attributes = [AttributeDeclaration([Attribute("test_1")]),
                      AttributeDeclaration([Attribute("test_2")]),
                      AttributeDeclaration([Attribute("test_3")])]
        result = criteria.filter(attributes)
        self.assertEqual(1, len(result))
        self.assertTrue(self.attribute_decl_eq(attributes[0], result[0]))

    def test_attribute_criteria_name_negative(self):
        criteria = AttributesCriteria(names=AttributeFilter(["test_1"], True), namespaces=None)
        attributes = [AttributeDeclaration([Attribute("test_1")]),
                      AttributeDeclaration([Attribute("test_2")]),
                      AttributeDeclaration([Attribute("test_3")])]
        result = criteria.filter(attributes)
        self.assertEqual(2, len(result))
        self.assertTrue(self.attribute_decl_eq(attributes[1], result[0]))
        self.assertTrue(self.attribute_decl_eq(attributes[2], result[1]))


class TestAttributePrinting(unittest.TestCase):

    def setUp(self):
        printer = CodePrinter()
        printer.register(FunctionPrinter, FunctionInfo)
        printer.register(VariablePrinter, Variable)
        printer.register(BasicTypePrinter, BasicType)
        printer.register(TypeExpressionPrinter, TypeExpression)
        printer.register(VariablePrinter, FunctionInfo.Argument)
        printer.register(AttributeDeclarationPrinter, AttributeDeclaration)
        printer.register(AttributePrinter, Attribute)
        self.printer: CodePrinter = create_default_printer()

    @staticmethod
    def create_base_function() -> FunctionInfo:
        source = FunctionInfo.create_default()
        source.name = "foo"
        source.return_type = TypeExpression.create_default()
        source.return_type.details = BasicType.INT
        arg1 = FunctionInfo.Argument()
        arg1.type = TypeExpression.create_default()
        arg1.type.details = BasicType.FLOAT
        arg1.name = "a"
        arg2 = FunctionInfo.Argument()
        arg2.type = TypeExpression.create_default()
        arg2.type.details = BasicType.INT
        arg2.name = "b"
        source.arguments = [arg1, arg2]
        return source

    def test_print_attribute(self):
        source = self.create_base_function()
        source.attributes = [AttributeDeclaration([Attribute("deprecated")])]
        result = self.printer.print(source)
        self.assertEqual("[[deprecated]]\nint foo(float a, int b);\n", result)

    def test_print_attribute_using_namespace(self):
        source = self.create_base_function()
        source.attributes = [AttributeDeclaration([Attribute("test_1")], "gnu")]
        result = self.printer.print(source)
        self.assertEqual("[[using gnu : test_1]]\nint foo(float a, int b);\n", result)

    def test_print_attribute_namespace(self):
        source = self.create_base_function()
        source.attributes = [AttributeDeclaration([Attribute("test_1", "gnu")])]
        result = self.printer.print(source)
        self.assertEqual("[[gnu::test_1]]\nint foo(float a, int b);\n", result)

    def test_print_attribute_params(self):
        source = self.create_base_function()
        source.attributes = [AttributeDeclaration([Attribute("deprecated", None, ['"str"', "7", "test_arg"])])]
        result = self.printer.print(source)
        self.assertEqual('[[deprecated("str",7,test_arg)]]\nint foo(float a, int b);\n', result)

    def test_print_attribute_empty_params(self):
        source = self.create_base_function()
        source.attributes = [AttributeDeclaration([Attribute("deprecated", None, [])])]
        result = self.printer.print(source)
        self.assertEqual('[[deprecated()]]\nint foo(float a, int b);\n', result)

    def test_print_attribute_multiple(self):
        source = self.create_base_function()
        source.attributes = [AttributeDeclaration([Attribute("deprecated"),
                                                   Attribute("nodiscard"),
                                                   Attribute("no_unique_address")])]
        result = self.printer.print(source)
        self.assertEqual('[[deprecated, nodiscard, no_unique_address]]\nint foo(float a, int b);\n', result)

    def test_print_attribute_multiple_declaration(self):
        source = self.create_base_function()
        source.attributes = [AttributeDeclaration([Attribute("deprecated")]),
                             AttributeDeclaration([Attribute("nodiscard")]),
                             AttributeDeclaration([Attribute("no_unique_address")])]
        result = self.printer.print(source)
        self.assertEqual('[[deprecated]]\n[[nodiscard]]\n[[no_unique_address]]\nint foo(float a, int b);\n', result)

    def test_print_attribute_for_function(self):
        source = FunctionInfo.create_default()
        source.name = "foo"
        source.attributes = [AttributeDeclaration([Attribute("deprecated")])]
        result = self.printer.print(source)
        self.assertEqual("[[deprecated]]\nvoid foo();\n", result)

    def test_print_attribute_for_function_argument(self):
        source = FunctionInfo.create_default()
        source.name = "foo"
        arg = FunctionInfo.Argument()
        arg.type = TypeExpression.create_default()
        arg.type.details = BasicType.FLOAT
        arg.name = "a"
        arg.attributes = [AttributeDeclaration([Attribute("deprecated")])]
        source.arguments = [arg]
        result = self.printer.print(source)
        self.assertEqual("void foo([[deprecated]] float a);\n", result)

    def test_print_attribute_for_class(self):
        source = ClassInfo.create_default()
        source.name = "foo"
        source.attributes = [AttributeDeclaration([Attribute("deprecated")])]
        result = self.printer.print(source)
        self.assertEqual("[[deprecated]]\nstruct foo\n{\n};\n", result)

    def test_print_attribute_for_class_field(self):
        source = ClassInfo.create_default()
        source.name = "foo"
        field = FieldInfo.create_default()
        field.name = "a"
        field.attributes = [AttributeDeclaration([Attribute("deprecated")])]
        source.content = [field]
        result = self.printer.print(source)
        self.assertEqual("struct foo\n{\n    [[deprecated]]\n    int a;\n};\n", result)

    def test_print_attribute_for_class_constructor(self):
        source = ClassInfo.create_default()
        source.name = "foo"
        field = ConstructorInfo.create_default()
        field.name = "foo"
        field.attributes = [AttributeDeclaration([Attribute("deprecated")])]
        source.content = [field]
        result = self.printer.print(source)
        self.assertEqual("struct foo\n{\n    [[deprecated]]\n    foo();\n};\n", result)

    def test_print_attribute_for_class_method(self):
        source = ClassInfo.create_default()
        source.name = "foo"
        field = MethodInfo.create_default()
        field.name = "ter"
        field.attributes = [AttributeDeclaration([Attribute("deprecated")])]
        source.content = [field]
        result = self.printer.print(source)
        self.assertEqual("struct foo\n{\n    [[deprecated]]\n    void ter();\n};\n", result)

    def test_print_attribute_for_enum(self):
        source = EnumInfo.create_default()
        source.attributes = [AttributeDeclaration([Attribute("deprecated")])]
        result = self.printer.print(source)
        self.assertEqual("[[deprecated]]\nenum TestEnum\n{\n};\n", result)

    def test_print_attribute_for_namespace(self):
        source = NamespaceInfo.create_default()
        source.attributes = [AttributeDeclaration([Attribute("deprecated")])]
        result = self.printer.print(source)
        self.assertEqual("[[deprecated]]\nnamespace TestNamespace\n{\n}\n", result)
