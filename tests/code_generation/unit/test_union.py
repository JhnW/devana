import unittest
from devana.code_generation.printers.default.basictypeprinter import BasicTypePrinter
from devana.code_generation.printers.default.typeexpressionprinter import TypeExpressionPrinter
from devana.code_generation.printers.default.unionprinter import UnionPrinter
from devana.code_generation.printers.default.classprinter import FieldPrinter
from devana.code_generation.printers.codeprinter import CodePrinter
from devana.syntax_abstraction.typeexpression import TypeModification, BasicType
from devana.syntax_abstraction.classinfo import FieldInfo
from devana.syntax_abstraction.unioninfo import UnionInfo
from devana.syntax_abstraction.typeexpression import TypeExpression


class TestCoreUnion(unittest.TestCase):

    def setUp(self):
        printer = CodePrinter()
        printer.register(BasicTypePrinter, BasicType)
        printer.register(TypeExpressionPrinter, TypeExpression)
        printer.register(UnionPrinter, UnionInfo)
        printer.register(FieldPrinter, FieldInfo)
        self.printer: CodePrinter = printer

    def test_print_simple_union_dec(self):
        source = UnionInfo()
        source.is_declaration = True
        source.name = "TestUnion"
        result = self.printer.print(source)
        self.assertEqual("union TestUnion;\n", result)

    def test_print_simple_union_def(self):
        source = UnionInfo()
        source.name = "TestUnion"
        source.content.append(FieldInfo())
        source.content[0].name = "a"
        source.content[0].type = TypeExpression()
        source.content[0].type.details = BasicType.FLOAT
        source.content.append(FieldInfo())
        source.content[1].name = "b"
        source.content[1].type = TypeExpression()
        source.content[1].type.details = BasicType.U_INT
        source.content.append(FieldInfo())
        source.content[2].name = "c"
        source.content[2].type = TypeExpression()
        source.content[2].type.details = BasicType.BOOL
        result = self.printer.print(source)
        self.assertEqual("union TestUnion\n{\n    float a;\n    unsigned int b;\n    bool c;\n};\n", result)

    def test_print_union_nested(self):
        source = UnionInfo()
        source.name = "TestUnion"
        source.content.append(FieldInfo())
        source.content[0].name = "a"
        source.content[0].type = TypeExpression()
        source.content[0].type.details = source
        source.content[0].type.modification = TypeModification.POINTER
        source.content.append(FieldInfo())
        source.content[1].name = "b"
        source.content[1].type = TypeExpression()
        source.content[1].type.details = BasicType.INT
        source.content.append(FieldInfo())
        source.content[2].name = "c"
        source.content[2].type = TypeExpression()
        source.content[2].type.details = BasicType.BOOL
        result = self.printer.print(source)
        self.assertEqual("union TestUnion\n{\n    TestUnion* a;\n    int b;\n    bool c;\n};\n", result)
