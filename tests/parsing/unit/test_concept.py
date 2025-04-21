import unittest
import os

from devana.configuration import ParsingConfiguration, LanguageStandard
from devana.syntax_abstraction.organizers.sourcefile import SourceFile
from devana.syntax_abstraction.conceptinfo import ConceptUsage
from devana.syntax_abstraction.classinfo import *


class TestConceptDefinition(unittest.TestCase):

    def setUp(self):
        self.file = SourceFile.from_path(
            source=os.path.dirname(__file__) + r"/source_files/concepts.hpp",
            configuration=Configuration(ParsingConfiguration(language_version=LanguageStandard.CPP_20))
        )

    def test_concept_requires_expr(self):
        result = self.file.content[0]
        self.assertEqual(result.name, "ConceptRequiresExpr")
        self.assertEqual(
            result.body.replace("\r\n", "\n"),
            "requires(T a, T b) {\n    { a + b };\n    { a-- };\n}"
        )
        self.assertEqual(len(result.template.parameters), 1)
        self.assertEqual(result.template.parameters[0].name, "T")
        self.assertEqual(result.template.parameters[0].specifier, "typename")

    def test_concept_multiple_requires(self):
        result = self.file.content[1]
        self.assertEqual(result.name, "ConceptMultipleRequires")
        self.assertEqual(
            result.body.replace("\r\n", "\n"),
    "requires(A a, T b) {\n    a = b;\n} || requires(A a, T b) {\n    b = a;\n}"
        )
        self.assertEqual(len(result.template.parameters), 2)
        self.assertEqual(result.template.parameters[0].name, "A")
        self.assertEqual(result.template.parameters[0].specifier, "typename")
        self.assertEqual(result.template.parameters[1].name, "T")
        self.assertEqual(result.template.parameters[1].specifier, "class")

    def test_concept_requires_alone(self):
        result = self.file.content[2]
        self.assertEqual(result.name, "ConceptRequiresAlone")
        self.assertEqual(result.body.replace("\r\n", "\n"), "requires {\n    T{};\n}")
        self.assertEqual(len(result.template.parameters), 1)
        self.assertEqual(result.template.parameters[0].name, "T")
        self.assertEqual(result.template.parameters[0].specifier, "typename")

    def test_concept_ref_and_requires(self):
        result = self.file.content[3]
        self.assertEqual(result.name, "ConceptRefAndRequires")
        self.assertEqual(
            result.body.replace("\r\n", "\n"),
            "ConceptRequiresAlone<T> && requires(T t) {\n    *t;\n}"
        )
        self.assertEqual(len(result.template.parameters), 1)
        self.assertEqual(result.template.parameters[0].name, "T")
        self.assertEqual(result.template.parameters[0].specifier, "typename")

    def test_concept_paren_expr(self):
        result = self.file.content[4]
        self.assertEqual(result.name, "ConceptParenExpr")
        self.assertEqual(result.body, "(T{} > 0)")
        self.assertEqual(len(result.template.parameters), 1)
        self.assertEqual(result.template.parameters[0].name, "T")
        self.assertEqual(result.template.parameters[0].specifier, "typename")

    def test_concept_ref_to_concept(self):
        result = self.file.content[5]
        self.assertEqual(result.name, "ConceptRefToConcept")
        self.assertEqual(result.body, "ConceptParenExpr<T>")
        self.assertEqual(len(result.template.parameters), 1)
        self.assertEqual(result.template.parameters[0].name, "T")
        self.assertEqual(result.template.parameters[0].specifier, "typename")

    def test_concept_multiple_refs(self):
        result = self.file.content[6]
        self.assertEqual(result.name, "ConceptMultipleRefs")
        self.assertEqual(result.body, "ConceptRequiresAlone<T> && ConceptRefToConcept<T>")
        self.assertEqual(len(result.template.parameters), 1)
        self.assertEqual(result.template.parameters[0].name, "T")
        self.assertEqual(result.template.parameters[0].specifier, "class")

    def test_concept_in_namespace(self):
        namespace = self.file.content[7]
        self.assertEqual(namespace.name, "ConceptNamespace")
        self.assertEqual(len(namespace.content), 1)

        result = namespace.content[0]
        self.assertEqual(result.name, "ConceptInNamespace")
        self.assertEqual(result.body, "true")
        self.assertEqual(len(result.template.parameters), 1)
        self.assertEqual(result.template.parameters[0].name, "T")
        self.assertEqual(result.template.parameters[0].specifier, "class")

    def test_concept_static_value(self):
        result = self.file.content[8]
        self.assertEqual(result.name, "ConceptStaticValue")
        self.assertEqual(result.body, "T::value || true")
        self.assertEqual(len(result.template.parameters), 1)
        self.assertEqual(result.template.parameters[0].name, "T")
        self.assertEqual(result.template.parameters[0].specifier, "typename")

    def test_concept_namespace_ref(self):
        result = self.file.content[9]
        self.assertEqual(result.name, "ConceptNamespaceRef")
        self.assertEqual(result.body, "ConceptNamespace::ConceptInNamespace<U*>")
        self.assertEqual(len(result.template.parameters), 1)
        self.assertEqual(result.template.parameters[0].name, "U")
        self.assertEqual(result.template.parameters[0].specifier, "typename")

    def test_concept_template(self):
        result = self.file.content[10]
        self.assertEqual(result.name, "ConceptTemplate")
        self.assertEqual(result.body, "true")
        self.assertEqual(result.template.parent, None)
        self.assertEqual(result.template.is_empty, False)
        self.assertEqual(result.template.requires, None)

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


class TestConceptUsage(unittest.TestCase):

    def setUp(self):
        self.file = SourceFile.from_path(
            source=os.path.dirname(__file__) + r"/source_files/concepts.hpp",
            configuration=Configuration(ParsingConfiguration(language_version=LanguageStandard.CPP_20))
        )

    def test_concept_is_linked_to_definition(self):
        result = self.file.content[11]
        self.assertEqual(result.template.parameters[0].specifier.name, "ConceptStaticValue")
        self.assertEqual(type(result.template.parameters[0].specifier), ConceptUsage)
        self.assertEqual(result.template.parameters[0].specifier.concept, self.file.content[8])


    def test_basic_concept_class(self):
        result = self.file.content[11]
        self.assertTrue(result.is_class)
        self.assertFalse(result.is_definition)
        self.assertEqual(result.name, "ClassBasicConcept")
        self.assertIsNone(result.template.requires)
        self.assertEqual(len(result.template.parameters), 2)
        self.assertEqual(result.template.parameters[0].name, "T")
        self.assertEqual(result.template.parameters[0].specifier.name, "ConceptStaticValue")
        self.assertEqual(result.template.parameters[0].specifier.namespaces, [])
        self.assertEqual(result.template.parameters[0].specifier.concept.body, "T::value || true")
        self.assertEqual(result.template.parameters[0].default_value, "bool")
        self.assertFalse(result.template.parameters[0].is_variadic)
        self.assertEqual(result.template.parameters[1].name, "Args")
        self.assertEqual(result.template.parameters[1].specifier.name, "ConceptInNamespace")
        self.assertEqual(result.template.parameters[1].specifier.namespaces, ["ConceptNamespace"])
        self.assertEqual(result.template.parameters[1].specifier.concept.body, "true")
        self.assertIsNone(result.template.parameters[1].default_value)
        self.assertTrue(result.template.parameters[1].is_variadic)

    def test_class_methods_concept(self):
        result = self.file.content[12]
        self.assertTrue(result.is_class)
        self.assertEqual(result.name, "ClassMethodsConcept")
        self.assertIsNone(result.template.requires)
        self.assertEqual(len(result.template.parameters), 1)
        self.assertEqual(result.template.parameters[0].name, "T")
        self.assertEqual(result.template.parameters[0].specifier.name, "ConceptStaticValue")
        self.assertEqual(result.template.parameters[0].specifier.namespaces, [])
        self.assertEqual(result.template.parameters[0].specifier.concept.body, "T::value || true")
        self.assertEqual(result.template.parameters[0].default_value, None)
        self.assertEqual(result.template.parameters[0].is_variadic, False)

        method = cast(MethodInfo, result.public[0])
        self.assertEqual(method.name, "process")
        self.assertEqual(method.type, MethodType.STANDARD)
        self.assertTrue(method.return_type.is_generic)
        self.assertEqual(method.return_type.details.name, "T")
        self.assertEqual(method.body, None)
        self.assertTrue(method.arguments[0].type.is_generic)
        self.assertTrue(method.arguments[0].type.modification.is_const)
        self.assertEqual(method.arguments[0].type.details.name, "T")
        self.assertIsNone(method.requires)

        method = cast(MethodInfo, result.public[1])
        self.assertEqual(method.name, "pair")
        self.assertEqual(method.type, MethodType.STANDARD)
        self.assertFalse(method.return_type.is_generic)
        self.assertEqual(method.return_type.details, BasicType.VOID)
        self.assertEqual(method.body, None)
        self.assertEqual(len(method.arguments), 2)
        self.assertTrue(method.arguments[0].type.is_generic)
        self.assertTrue(method.arguments[0].type.modification.is_const)
        self.assertEqual(method.arguments[0].type.details.name, "T")
        self.assertEqual(method.arguments[0].name, "arg1")
        self.assertTrue(method.arguments[1].type.is_generic)
        self.assertTrue(method.arguments[1].type.modification.is_const)
        self.assertEqual(method.arguments[1].type.details.name, "B")
        self.assertEqual(method.arguments[1].name, "arg2")
        self.assertIsNone(method.requires)
        self.assertIsNotNone(method.template)
        self.assertIsNone(method.template.requires)
        self.assertEqual(len(method.template.parameters), 1)
        self.assertEqual(method.template.parameters[0].name, "B")
        self.assertEqual(method.template.parameters[0].specifier.name, "ConceptStaticValue")
        self.assertEqual(method.template.parameters[0].specifier.concept.body, "T::value || true")
        self.assertEqual(method.template.parameters[0].specifier.namespaces, [])

        method = cast(MethodInfo, result.private[0])
        self.assertEqual(method.name, "secret_stuff_")
        self.assertEqual(method.type, MethodType.STANDARD)
        self.assertTrue(method.modification.is_inline)
        self.assertTrue(method.modification.is_noexcept)
        self.assertTrue(method.return_type.is_generic)
        self.assertEqual(method.return_type.details.name, "T")
        self.assertTrue(method.return_type.modification.is_pointer)
        self.assertEqual(len(method.arguments), 1)
        self.assertTrue(method.arguments[0].type.is_generic)
        self.assertTrue(method.arguments[0].type.modification.is_pointer)
        self.assertEqual(method.arguments[0].type.details.name, "T")
        self.assertEqual(method.arguments[0].name, "p")

    def test_struct_requires(self):
        result = self.file.content[13]
        self.assertTrue(result.is_struct)
        self.assertEqual(result.name, "StructRequires")
        self.assertIsNotNone(result.template)
        self.assertEqual(len(result.template.parameters), 1)
        self.assertEqual(result.template.parameters[0].name, "T")
        self.assertEqual(result.template.parameters[0].specifier, "typename")
        self.assertEqual(len(result.template.requires), 5)
        requires_concept = cast(ConceptUsage, result.template.requires.pop(3))
        self.assertEqual(result.template.requires, ["(", "true", "and", ")"])
        self.assertEqual(requires_concept.name, "ConceptStaticValue")
        self.assertEqual(requires_concept.namespaces, [])
        self.assertEqual(requires_concept.concept.body, "T::value || true")

        field = cast(FieldInfo, result.public[0])
        self.assertEqual(field.name, "abc")
        self.assertTrue(field.type.is_generic)
        self.assertEqual(field.type.details.name, "T")
        self.assertTrue(field.type.modification.is_const)
        self.assertIsNone(field.default_value)

        method = cast(MethodInfo, result.public[1])
        self.assertEqual(method.name, "foo")
        self.assertEqual(len(method.arguments), 0)
        self.assertTrue(method.is_declaration)
        self.assertTrue(method.return_type.is_generic)
        self.assertEqual(method.return_type.details.name, "B")
        self.assertEqual(len(method.template.parameters), 1)
        self.assertEqual(method.template.parameters[0].name, "B")
        self.assertEqual(method.template.parameters[0].specifier, "class")
        self.assertEqual(len(method.template.requires), 1)
        self.assertEqual(method.template.requires[0].name, "ConceptInNamespace")
        self.assertEqual(method.template.requires[0].namespaces, ["ConceptNamespace"])
        self.assertEqual(method.template.requires[0].concept.body, "true")
        self.assertTrue(len(method.requires), 3)
        self.assertEqual(method.requires[0].name, "ConceptStaticValue")
        self.assertEqual(method.requires[0].namespaces, [])
        self.assertEqual(method.requires[0].concept.body, "T::value || true")
        self.assertTrue(method.requires[1:2], ["||", "false"])

        method = cast(MethodInfo, result.public[2])
        self.assertEqual(method.name, "calc")
        self.assertEqual(len(method.arguments), 0)
        self.assertTrue(method.is_declaration)
        self.assertFalse(method.return_type.is_generic)
        self.assertEqual(method.return_type.details, BasicType.VOID)
        self.assertEqual(method.requires, ["(", "true", "or", "false", ")"])

    def test_function_with_concept(self):
        result: FunctionInfo = self.file.content[14]
        self.assertEqual(result.name, "function_with_concept")
        self.assertEqual(result.body, None)
        self.assertEqual(result.return_type.is_generic, True)
        self.assertEqual(result.return_type.details.name, "T")
        self.assertEqual(result.requires, None)
        self.assertEqual(result.template.requires, None)
        self.assertEqual(len(result.template.parameters), 2)

        self.assertEqual(result.template.parameters[0].name, "T")
        self.assertEqual(result.template.parameters[0].specifier.name, "ConceptParenExpr")
        self.assertEqual(result.template.parameters[0].specifier.namespaces, [])
        self.assertEqual(result.template.parameters[0].specifier.concept.body, "(T{} > 0)")
        self.assertEqual(result.template.parameters[0].default_value, "int")
        self.assertEqual(result.template.parameters[0].is_variadic, False)

        self.assertEqual(result.template.parameters[1].name, "Args")
        self.assertEqual(result.template.parameters[1].specifier.name, "ConceptParenExpr")
        self.assertEqual(result.template.parameters[1].specifier.namespaces, [])
        self.assertEqual(result.template.parameters[1].specifier.concept.body, "(T{} > 0)")
        self.assertEqual(result.template.parameters[1].default_value, None)
        self.assertEqual(result.template.parameters[1].is_variadic, True)

    def test_function_with_requires_1(self):
        result: FunctionInfo = self.file.content[15]
        self.assertEqual(result.name, "function_with_requires_1")
        self.assertEqual(result.body, None)
        self.assertEqual(result.return_type.details, BasicType.VOID)
        self.assertEqual(result.requires, ["true", "or", "false"])

        self.assertEqual(len(result.arguments), 1)
        self.assertEqual(result.arguments[0].name, "a")
        self.assertEqual(result.arguments[0].type.is_generic, True)
        self.assertEqual(result.arguments[0].type.details.name, "T")
        self.assertEqual(result.template.parameters[0].name, "T")
        self.assertEqual(result.template.parameters[0].specifier, "typename")

        self.assertEqual(len(result.template.requires), 1)
        self.assertEqual(result.template.requires[0].name, "ConceptParenExpr")
        self.assertEqual(result.template.requires[0].namespaces, [])
        self.assertEqual(result.template.requires[0].concept.body, "(T{} > 0)")

    def test_function_with_requires_2(self):
        result: FunctionInfo = self.file.content[16]
        self.assertEqual(result.name, "function_with_requires_2")
        self.assertEqual(result.body, None)
        self.assertEqual(result.return_type.details, BasicType.INT)

        self.assertEqual(len(result.arguments), 1)
        self.assertEqual(result.arguments[0].name, "a")
        self.assertEqual(result.arguments[0].default_value, "1")
        self.assertEqual(result.arguments[0].type.is_generic, True)
        self.assertEqual(result.arguments[0].type.details.name, "T")

        self.assertEqual(len(result.requires), 5)
        self.assertEqual(result.requires[0].name, "ConceptParenExpr")
        self.assertEqual(result.requires[0].concept.body, "(T{} > 0)")
        self.assertEqual(result.requires[1:5], ["and", "(", "true", ")"])
        self.assertEqual(result.template.parameters[0].name, "T")
        self.assertEqual(result.template.parameters[0].specifier.name, "ConceptStaticValue")
        self.assertEqual(result.template.parameters[0].specifier.namespaces, [])
        self.assertEqual(result.template.parameters[0].specifier.concept.body, "T::value || true")

        self.assertEqual(len(result.template.requires), 3)
        self.assertEqual(result.template.requires[0], "true")
        self.assertEqual(result.template.requires[1], "or")
        self.assertEqual(result.template.requires[2].name, "ConceptParenExpr")
        self.assertEqual(result.template.requires[2].namespaces, [])
        self.assertEqual(result.template.requires[2].concept.body, "(T{} > 0)")

    def test_namespace_concept_function(self):
        result: FunctionInfo = self.file.content[17]
        self.assertEqual(result.name, "function_with_concept_namespace")
        self.assertEqual(result.body, None)
        self.assertEqual(result.requires, None)
        self.assertEqual(len(result.arguments), 0)
        self.assertTrue(result.return_type.is_generic)
        self.assertEqual(result.return_type.details.name, "T")
        self.assertEqual(result.template.requires, None)

        param = result.template.parameters[0]
        self.assertEqual(param.name, "T")
        self.assertEqual(param.specifier.name, "ConceptInNamespace")
        self.assertEqual(param.specifier.namespaces, ["ConceptNamespace"])

    def test_std_argument_concept(self):
        result: ClassInfo = self.file.content[18]
        self.assertEqual(result.name, "UsedStdInTemplate")
        self.assertEqual(result.template.requires, None)
        self.assertEqual(result.template.parameters[0].specifier.name, "integral")
        self.assertEqual(result.template.parameters[0].specifier.namespaces, ["std"])

    def test_concept_parameters(self):
        result: FunctionInfo = self.file.content[19]
        self.assertEqual(result.name, "foo_function_with_concept")
        self.assertEqual(len(result.template.requires), 1)
        require = result.template.requires[0]
        self.assertEqual(require.name, "ConceptRequiresExpr")
        self.assertEqual(len(require.parameters), 1)
        self.assertEqual(require.parameters[0], "T")

