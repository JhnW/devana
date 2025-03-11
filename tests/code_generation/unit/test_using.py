import unittest
from devana.code_generation.printers.default.basictypeprinter import BasicTypePrinter
from devana.code_generation.printers.default.typeexpressionprinter import TypeExpressionPrinter
from devana.code_generation.printers.default.templateparameterprinter import TemplateParameterPrinter
from devana.code_generation.printers.default.conceptprinter import ConceptPrinter
from devana.code_generation.printers.default.usingprinter import UsingPrinter
from devana.code_generation.printers.codeprinter import CodePrinter
from devana.syntax_abstraction.using import Using
from devana.syntax_abstraction.conceptinfo import ConceptInfo
from devana.syntax_abstraction.templateinfo import TemplateInfo, GenericTypeParameter
from devana.syntax_abstraction.typeexpression import BasicType, TypeExpression, TypeModification


class TestUsing(unittest.TestCase):

    def setUp(self):
        printer = CodePrinter()
        printer.register(BasicTypePrinter, BasicType)
        printer.register(TypeExpressionPrinter, TypeExpression)
        printer.register(UsingPrinter, Using)
        printer.register(TemplateParameterPrinter, TemplateInfo.TemplateParameter)
        printer.register(BasicTypePrinter, GenericTypeParameter)
        printer.register(ConceptPrinter, ConceptInfo)
        self.printer: CodePrinter = printer

    def test_definition_basic(self):
        source = Using()
        source.name = "const_ptr_t"
        source.type_info = TypeExpression()
        source.type_info.details = BasicType.CHAR
        source.type_info.modification |= TypeModification.POINTER | TypeModification.CONST
        result = self.printer.print(source)
        self.assertEqual(result, "using const_ptr_t = const char*;\n")

    def test_using_template(self):
        source = Using.from_params(
            name="constType",
            type_info=TypeExpression.from_params(
                details=GenericTypeParameter("T"),
                modification=TypeModification.CONST
            ),
            template=TemplateInfo.from_params(
                parameters=[
                    TemplateInfo.TemplateParameter.from_params(
                    specifier="typename",
                    name="T"
                )]
            )
        )
        result = self.printer.print(source)
        self.assertEqual(result, "template<typename T>\nusing constType = const T;\n")

    def test_using_template_with_requires(self):
        source = Using.from_params(
            name="constexprType",
            type_info=TypeExpression.from_params(
                details=GenericTypeParameter("B"),
                modification=TypeModification.CONSTEXPR
            ),
            template=TemplateInfo.from_params(
                parameters=[
                    TemplateInfo.TemplateParameter.from_params(
                    specifier="typename",
                    name="B"
                )],
                requires=["true"]
            )
        )
        result = self.printer.print(source)
        self.assertEqual(result, "template<typename B> requires true\nusing constexprType = constexpr B;\n")

    def test_using_template_with_concept(self):
        source = Using.from_params(
            name="ConceptPtr",
            type_info=TypeExpression.from_params(
                details=GenericTypeParameter("C"),
                modification=TypeModification.POINTER
            ),
            template=TemplateInfo.from_params(
                parameters=[
                    TemplateInfo.TemplateParameter.from_params(
                    specifier=ConceptInfo.from_params(name="Concept", is_requirement=True),
                    name="C"
                )]
            )
        )
        result = self.printer.print(source)
        self.assertEqual(result, "template<Concept C>\nusing ConceptPtr = C*;\n")
