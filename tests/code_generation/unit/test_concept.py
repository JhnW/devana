from devana.code_generation.printers.default.templateparameterprinter import TemplateParameterPrinter
from devana.code_generation.printers.default.conceptprinter import ConceptPrinter, ConceptUsagePrinter
from devana.code_generation.printers.default.classprinter import ClassPrinter, FieldPrinter, MethodPrinter
from devana.code_generation.printers.default.typeexpressionprinter import TypeExpressionPrinter
from devana.code_generation.printers.default.basictypeprinter import BasicTypePrinter
from devana.code_generation.printers.default.functionprinter import FunctionPrinter
from devana.syntax_abstraction.templateinfo import GenericTypeParameter
from devana.syntax_abstraction.conceptinfo import ConceptInfo, ConceptUsage
from devana.syntax_abstraction.functioninfo import FunctionInfo
from devana.syntax_abstraction.classinfo import ClassInfo, FieldInfo, MethodInfo
from devana.syntax_abstraction.templateinfo import TemplateInfo
from devana.syntax_abstraction.typeexpression import TypeExpression, BasicType
from devana.code_generation.printers.codeprinter import CodePrinter
import unittest


class TestConceptAlone(unittest.TestCase):

    def setUp(self):
        self.printer = CodePrinter()
        self.printer.register(ConceptPrinter, ConceptInfo)
        self.printer.register(ConceptUsagePrinter, ConceptUsage)
        self.printer.register(TemplateParameterPrinter, TemplateInfo.TemplateParameter)
        self.printer.register(TypeExpressionPrinter, TypeExpression)
        self.printer.register(BasicTypePrinter, GenericTypeParameter)
        self.printer.register(BasicTypePrinter, BasicType)

    def test_print_simple_concept(self):
        concept = ConceptInfo.from_params(
            name="TestConcept",
            body="T{}"
        )
        result = self.printer.print(concept)
        self.assertEqual(result, "template<typename T>\nconcept TestConcept = T{};\n")

    def test_print_complex_body_concept(self):
        concept = ConceptInfo.from_params(
            name="ComplexConcept",
            body="true or false or && requires(A a) {\n    a++;\n}",
            template=TemplateInfo.from_params(
                parameters=[
                    TemplateInfo.TemplateParameter.from_params(
                        name="A", specifier="class"
                    )
                ]
            )
        )
        result = self.printer.print(concept)
        self.assertEqual(result, """template<class A>
concept ComplexConcept = true or false or && requires(A a) {
    a++;
};
""")
    def test_print_concept_template_params(self):
        concept = ConceptInfo.from_params(
            template=TemplateInfo.from_params(
                parameters=[
                    TemplateInfo.TemplateParameter.from_params(
                        name="A",
                        specifier="class",
                        default_value="10"
                    ),
                    TemplateInfo.TemplateParameter.from_params(
                        name="Args",
                        specifier="typename",
                        is_variadic=True
                    )
                ]
            )
        )
        result = self.printer.print(concept)
        self.assertEqual(result, """template<class A = 10, typename Args...>
concept DefaultConcept = true;
""")
    def test_print_concept_skip_requires(self):
        concept = ConceptInfo.create_default()
        concept.template.requires = ["true"]
        result = self.printer.print(concept)
        self.assertEqual(result, "template<typename T>\nconcept DefaultConcept = true;\n")

    def test_print_concept_usage(self):
        concept = ConceptInfo.from_params(name="Test")
        with self.subTest("No parameters"):
            result = self.printer.print(ConceptUsage.from_params(concept=concept))
            self.assertEqual(result, "Test")
            result = self.printer.print(ConceptUsage.from_params(concept=concept, namespaces=["abc", "test"]))
            self.assertEqual(result, "abc::test::Test")

        with self.subTest("With parameters"):
            parameters = [
                TypeExpression.from_params(details=GenericTypeParameter("T")),
                TypeExpression.create_default()
            ]
            result = self.printer.print(ConceptUsage.from_params(concept=concept, parameters=parameters))
            self.assertEqual(result, "Test<T, int>")
            result = self.printer.print(ConceptUsage.from_params(concept=concept, parameters=parameters, namespaces=["abc"]))
            self.assertEqual(result, "abc::Test<T, int>")

class TestConceptWithClass(unittest.TestCase):

    def setUp(self):
        self.printer = CodePrinter()
        self.printer.register(ConceptPrinter, ConceptInfo)
        self.printer.register(ConceptUsagePrinter, ConceptUsage)
        self.printer.register(TemplateParameterPrinter, TemplateInfo.TemplateParameter)
        self.printer.register(ClassPrinter, ClassInfo)
        self.printer.register(TypeExpressionPrinter, TypeExpression)
        self.printer.register(BasicTypePrinter, BasicType)
        self.printer.register(FieldPrinter, FieldInfo)
        self.printer.register(BasicTypePrinter, GenericTypeParameter)
        self.printer.register(MethodPrinter, MethodInfo)

    def test_print_simple_class_concept(self):
        concept = ConceptInfo.from_params(
            name="TestConcept",
        )
        class_ = ClassInfo.from_params(
            name="ClassConcept",
            is_class=True,
            is_declaration=True,
            template=TemplateInfo.from_params(
                parameters=[
                    TemplateInfo.TemplateParameter.from_params(
                        name="T",
                        specifier=ConceptUsage.from_params(concept=concept)
                    )
                ]
            )
        )
        result = self.printer.print(class_)
        self.assertEqual(result, """template<TestConcept T>
class ClassConcept;
""")
    def test_print_class_requires(self):
        class_ = ClassInfo.from_params(
            name="ClassRequires",
            template=TemplateInfo.from_params(
                requires=["true"],
                parameters=[
                    TemplateInfo.TemplateParameter.create_default()
                ]
            ),
            is_declaration=True
        )
        result = self.printer.print(class_)
        self.assertEqual(result, """template<typename T> requires true
struct ClassRequires;
""")

    def test_print_complex_concept_class(self):
        concept_usage_1 = ConceptUsage.from_params(
            concept=ConceptInfo.create_default(),
            namespaces=["abc"],
            parameters=[TypeExpression.create_default()]
        )
        concept_usage_2 = ConceptUsage.from_params(
            concept=ConceptInfo.from_params(name="Testing"),
            parameters=[TypeExpression.from_params(details=GenericTypeParameter("T"))]
        )
        class_ = ClassInfo.from_params(
            name="ComplexConceptClass",
            is_class=True,
            content=[
                FieldInfo.from_params(
                    name="atr",
                    type=TypeExpression.from_params(
                        details=GenericTypeParameter("T")
                    )
                ),
                MethodInfo.from_params(
                    name="foo",
                    return_type=BasicType.VOID,
                    requires=[concept_usage_2, "and", concept_usage_1]
                )
            ],
            template=TemplateInfo.from_params(
                requires=["true", "&&", concept_usage_2],
                parameters=[
                    TemplateInfo.TemplateParameter.from_params(
                        name="T",
                        specifier=concept_usage_1
                    )
                ]
            )
        )
        result = self.printer.print(class_)
        self.assertEqual(result, """template<abc::DefaultConcept<int> T> requires true && Testing<T>
class ComplexConceptClass
{
    T atr;
    void foo() requires Testing<T> and abc::DefaultConcept<int>;
};
""")

class TestConceptWithFunction(unittest.TestCase):

    def setUp(self):
        self.printer = CodePrinter()
        self.printer.register(ConceptPrinter, ConceptInfo)
        self.printer.register(TemplateParameterPrinter, TemplateInfo.TemplateParameter)
        self.printer.register(ClassPrinter, ClassInfo)
        self.printer.register(TypeExpressionPrinter, TypeExpression)
        self.printer.register(BasicTypePrinter, BasicType)
        self.printer.register(FieldPrinter, FieldInfo)
        self.printer.register(BasicTypePrinter, GenericTypeParameter)
        self.printer.register(FunctionPrinter, FunctionInfo)

    def test_function_requires(self):
        concept_usage = ConceptUsage.from_params(
            concept=ConceptInfo.from_params(name="TestConcept"),
            parameters=[TypeExpression.from_params(details=GenericTypeParameter("T"))]
        )

        source = FunctionInfo.from_params(
            template=TemplateInfo.from_params(
                parameters=[TemplateInfo.TemplateParameter.create_default()],
                requires=[concept_usage, "or", "true"]
            ),
            body=None,
            requires=["true", "||", concept_usage]
        )
        result = self.printer.print(source)
        self.assertEqual(result, "template<typename T> requires TestConcept<T> or true\nvoid foo() requires true || TestConcept<T>;\n")

    def test_function_concept(self):
        source = FunctionInfo.from_params(
            template=TemplateInfo.from_params(
                parameters=[TemplateInfo.TemplateParameter.from_params(
                    name="T",
                    specifier=ConceptUsage.from_params(
                        concept=ConceptInfo.create_default(),
                        namespaces=["test", "abc"],
                        parameters=[TypeExpression.create_default()]
                    ),
                )]
            )
        )
        result = self.printer.print(source)
        self.assertEqual(result, "template<test::abc::DefaultConcept<int> T>\nvoid foo();\n")
