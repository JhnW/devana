import unittest
import clang.cindex
import clang
import os
from devana.syntax_abstraction.using import Using
from devana.syntax_abstraction.organizers.sourcefile import SourceFile
from devana.syntax_abstraction.functioninfo import FunctionInfo
from devana.syntax_abstraction.typeexpression import BasicType


class TestUsing(unittest.TestCase):

    def setUp(self):
        index = clang.cindex.Index.create()
        self.cursor = index.parse(os.path.dirname(__file__) + r"/source_files/using.hpp").cursor
        self.file = SourceFile(self.cursor)

    def test_using_as_simple_alias(self):
        source: Using = self.file.content[1]
        self.assertEqual(source.name, "B")
        self.assertTrue(source.type_info.modification.is_const)
        self.assertTrue(source.type_info.modification.is_pointer)
        x = source.type_info.details
        self.assertEqual(source.type_info.details, self.file.content[0].content[0])
        fnc: FunctionInfo = self.file.content[2]
        self.assertEqual(fnc.arguments[0].type.details, source)

    def test_using_as_template_alias(self):
        source: Using = self.file.content[4]
        self.assertEqual(source.name, "AT")
        self.assertTrue(source.type_info.modification.is_const)
        self.assertEqual(source.type_info.details, self.file.content[3])
        self.assertEqual(len(source.type_info.template_arguments), 1)
        self.assertEqual(source.type_info.template_arguments[0].details, BasicType.DOUBLE)
