import unittest
from devana.code_generation.printers.default.basictypeprinter import BasicTypePrinter
from devana.code_generation.printers.default.typeexpressionprinter import TypeExpressionPrinter
from devana.code_generation.printers.default.enumprinter import EnumPrinter
from devana.code_generation.printers.default.namespaceprinter import NamespacePrinter
from devana.code_generation.printers.default.commentprinter import CommentPrinter
from devana.syntax_abstraction.namespaceinfo import NamespaceInfo
from devana.syntax_abstraction.enuminfo import EnumInfo
from devana.syntax_abstraction.comment import CommentMarker
from devana.code_generation.printers.default.classprinter import *
from devana.code_generation.printers.codeprinter import CodePrinter
from devana.syntax_abstraction.typeexpression import TypeModification, BasicType
from devana.syntax_abstraction.classinfo import *
from devana.syntax_abstraction.unioninfo import UnionInfo
from devana.code_generation.printers.default.unionprinter import UnionPrinter
from devana.code_generation.printers.default.typedefprinter import TypedefPrinter
from devana.syntax_abstraction.typedefinfo import TypedefInfo
from devana.code_generation.printers.default.variableprinter import VariablePrinter, GlobalVariablePrinter
from devana.syntax_abstraction.variable import Variable, GlobalVariable
from devana.syntax_abstraction.organizers.sourcefile import SourceFile, IncludeInfo
from devana.code_generation.printers.default.fileprinter import FilePrinter, IncludePrinter


class TestComment(unittest.TestCase):

    def setUp(self):
        printer = CodePrinter()
        printer.register(FunctionPrinter, FunctionInfo)
        printer.register(VariablePrinter, Variable)
        printer.register(BasicTypePrinter, BasicType)
        printer.register(TypeExpressionPrinter, TypeExpression)
        printer.register(VariablePrinter, FunctionInfo.Argument)
        printer.register(EnumPrinter, EnumInfo)
        printer.register(NamespacePrinter, NamespaceInfo)
        printer.register(MethodPrinter, MethodInfo)
        printer.register(ConstructorPrinter, ConstructorInfo)
        printer.register(DestructorPrinter, DestructorInfo)
        printer.register(AccessSpecifierPrinter, AccessSpecifier)
        printer.register(ClassPrinter, ClassInfo)
        printer.register(FieldPrinter, FieldInfo)
        printer.register(UnionPrinter, UnionInfo)
        printer.register(TypedefPrinter, TypedefInfo)
        printer.register(GlobalVariablePrinter, GlobalVariable)
        printer.register(FilePrinter, SourceFile)
        printer.register(IncludePrinter, IncludeInfo)
        printer.register(CommentPrinter, Comment)
        self.printer: CodePrinter = printer

    def test_print_simple_one_line_marker_comment(self):
        comment = Comment(CommentMarker.ONE_LINE)
        comment.text = ["test 1", "test 2"]
        result = self.printer.print(comment)
        self.assertEqual(result, "//test 1\n//test 2")

    def test_print_simple_one_line_comment_multiple_marker(self):
        comment = Comment(CommentMarker.MULTI_LINE)
        comment.text = ["test"]
        result = self.printer.print(comment)
        self.assertEqual(result, "/*test*/")

    def test_print_simple__multi_line_marker_comment(self):
        comment = Comment(CommentMarker.MULTI_LINE)
        comment.text = ["test 1", "test 2"]
        result = self.printer.print(comment)
        self.assertEqual(result, "/*\ntest 1\ntest 2\n*/")

    def test_print_associated_comment_function(self):
        comment = Comment()
        comment.text = ["test function"]
        element: FunctionInfo = FunctionInfo()
        element.name = "foo"
        element.associated_comment = comment
        result = self.printer.print(element)
        self.assertEqual(result, "//test function\nvoid foo();\n")

    def test_print_associated_comment_struct(self):
        comment = Comment()
        comment.text = ["test struct"]
        element: ClassInfo = ClassInfo()
        element.name = "Foo"
        element.associated_comment = comment
        result = self.printer.print(element)
        self.assertEqual(result, "//test struct\nstruct Foo\n{\n};\n")

    def test_print_associated_comment_union(self):
        comment = Comment()
        comment.text = ["test union"]
        element: UnionInfo = UnionInfo()
        element.name = "Foo"
        element.associated_comment = comment
        result = self.printer.print(element)
        self.assertEqual(result, "//test union\nunion Foo\n{\n};\n")

    def test_print_associated_comment_typedef(self):
        comment = Comment()
        comment.text = ["test typedef"]
        element: TypedefInfo = TypedefInfo()
        element.name = "TypeFoo"
        element.type_info = TypeExpression()
        element.type_info.details = BasicType.CHAR
        element.associated_comment = comment
        result = self.printer.print(element)
        self.assertEqual(result, "//test typedef\ntypedef char TypeFoo;\n")

    def test_print_associated_comment_enum(self):
        comment = Comment()
        comment.text = ["test enum"]
        element: EnumInfo = EnumInfo()
        element.name = "TestEnum"
        element.values = [EnumInfo.EnumValue(), EnumInfo.EnumValue(), EnumInfo.EnumValue()]
        element.values[0].name = "A"
        element.values[0].is_default = True
        element.values[1].name = "B"
        element.values[1].is_default = True
        value_comment: Comment = Comment()
        value_comment.text = ["test enum value"]
        element.values[1].associated_comment = value_comment
        element.values[2].name = "C"
        element.values[2].is_default = True
        element.associated_comment = comment
        result = self.printer.print(element)
        self.assertEqual(result, "//test enum\nenum TestEnum\n{\n    A,\n    //test enum value\n    B,\n    C\n};\n")

    def test_print_associated_comment_namespace(self):
        comment = Comment()
        comment.text = ["test namespace"]
        element: NamespaceInfo = NamespaceInfo()
        element.name = "Foo"
        element.associated_comment = comment
        result = self.printer.print(element)
        self.assertEqual(result, "//test namespace\nnamespace Foo\n{\n}\n")

    def test_print_associated_comment_global_variable(self):
        comment = Comment()
        comment.text = ["test global variable"]
        element: GlobalVariable = GlobalVariable()
        element.name = "foo"
        element.type = TypeExpression()
        element.type.modification |= TypeModification.CONST
        element.type.details = BasicType.CHAR
        element.associated_comment = comment
        result = self.printer.print(element)
        self.assertEqual(result, "//test global variable\nconst char foo;\n")

    def test_print_associated_comment_file_preamble(self):
        comment = Comment()
        comment.text = ["test preamble 1", "test preamble 2"]
        file: SourceFile = SourceFile()
        file.header_guard = "TEST_H"
        file.preamble = comment
        include = IncludeInfo()
        include.value = "bar.h"
        include.is_standard = False
        file.includes = [include]
        element: FunctionInfo = FunctionInfo()
        element.name = "foo"
        file.content = [element]
        result = self.printer.print(file)
        self.assertEqual(result, '//test preamble 1\n//test preamble 2\n\n#ifndef TEST_H\n#define TEST_H\n\n'
                                 '#include "bar.h"\n\nvoid foo();\n\n#endif //TEST_H\n')

    def test_print_associated_comment_class_elements(self):
        class_info = ClassInfo()
        class_info.name = "TestClass"
        class_info.content = []
        comment = Comment()
        comment.text = ["class comment 1"]
        class_info.associated_comment = comment

        constructor = ConstructorInfo()
        constructor.name = "TestClass"
        comment = Comment()
        comment.text = ["class comment 2"]
        constructor.associated_comment = comment
        class_info.content.append(constructor)

        destructor = DestructorInfo()
        destructor.name = "~TestClass"
        comment = Comment()
        comment.text = ["class comment 3"]
        destructor.associated_comment = comment
        class_info.content.append(destructor)

        method = MethodInfo()
        method.name = "Foo1"
        comment = Comment()
        comment.text = ["class comment 4"]
        method.associated_comment = comment
        class_info.content.append(method)

        field = FieldInfo()
        field.name = "a"
        field.type = TypeExpression()
        field.type.modification = TypeModification.POINTER
        field.type.details = BasicType.FLOAT
        comment = Comment()
        comment.text = ["class comment 5"]
        field.associated_comment = comment
        class_info.content.append(field)

        result = self.printer.print(class_info)
        self.assertEqual(result, "//class comment 1\nstruct TestClass\n"
                                 "{\n"
                                 "    //class comment 2\n"
                                 "    TestClass();\n"
                                 "    //class comment 3\n"
                                 "    ~TestClass();\n"
                                 "    //class comment 4\n"
                                 "    void Foo1();\n"
                                 "    //class comment 5\n"
                                 "    float* a;\n"
                                 "};\n")
