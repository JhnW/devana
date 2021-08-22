import unittest
from devana.code_generation.printers.default.basictypeprinter import BasicTypePrinter
from devana.code_generation.printers.default.typeexpressionprinter import TypeExpressionPrinter
from devana.syntax_abstraction.typeexpression import BasicType, TypeExpression, TypeModification


class TestTypeExpressionCore(unittest.TestCase):

    def test_print_basic_type(self):
        cases = (
            ("int", BasicType.INT),
            ("unsigned int", BasicType.U_INT),
            ("short", BasicType.SHORT),
            ("unsigned short", BasicType.U_SHORT),
            ("char", BasicType.CHAR),
            ("unsigned char", BasicType.U_CHAR),
            ("long", BasicType.LONG),
            ("unsigned long", BasicType.U_LONG),
            ("long long", BasicType.LONG_LONG),
            ("unsigned long long", BasicType.U_LONG_LONG),
            ("bool", BasicType.BOOL),
            ("float", BasicType.FLOAT),
            ("double", BasicType.DOUBLE),
            ("long double", BasicType.LONG_DOUBLE),
            ("void", BasicType.VOID),
        )

        printer = BasicTypePrinter()
        for c in cases:
            with self.subTest(c[0]):
                result = printer.print(c[1])
                self.assertEqual(c[0], result)

    def test_print_type_expression_basic_mods_stand_alone(self):
        mods = (
            (TypeModification.CONST, "const double"),
            (TypeModification.REFERENCE, "double&"),
            (TypeModification.POINTER, "double*"),
            (TypeModification.STATIC, "static double"),
            (TypeModification.TEMPLATE, "template double"),
            (TypeModification.CONSTEXPR, "constexpr double"),
            (TypeModification.RESTRICT, "restrict double"),
            (TypeModification.VOLATILE, "volatile double"),
            (TypeModification.RVALUE_REF, "double&&"),
            (TypeModification.ARRAY, "double")
        )

        for m in mods:
            with self.subTest(m[0]):
                source = TypeExpression()
                source.details = BasicType.DOUBLE
                source.modification |= m[0]
                printer = TypeExpressionPrinter(BasicTypePrinter())
                result = printer.print(source)
                self.assertEqual(result, m[1])

    def test_print_type_expression_basic_mods_ptr_order(self):
        source = TypeExpression()
        source.details = BasicType.FLOAT
        source.modification |= TypeModification.POINTER(3)
        printer = TypeExpressionPrinter(BasicTypePrinter())
        result = printer.print(source)
        self.assertEqual(result, "float***")









