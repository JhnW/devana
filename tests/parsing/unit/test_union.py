import unittest
import clang.cindex
import clang
import os
from tests.helpers import find_by_name
from devana.syntax_abstraction.unioninfo import UnionInfo
from devana.syntax_abstraction.classinfo import ClassInfo


class TestUnion(unittest.TestCase):

    def setUp(self):
        index = clang.cindex.Index.create()
        self.cursor = index.parse(os.path.dirname(__file__) + r"/source_files/union.hpp").cursor

    def test_stand_alone_union(self):
        node = find_by_name(self.cursor, "TestUnion")
        result = UnionInfo.from_cursor(node)
        self.assertEqual(result.name, "TestUnion")
        self.assertEqual(len(result.content), 3)

    def test_class_union(self):
        node = find_by_name(self.cursor, "SimpleClass")
        result = ClassInfo.from_cursor(node)
        self.assertEqual(result.name, "SimpleClass")
        self.assertEqual(len(result.content), 1)
        result: UnionInfo = result.content[0]
        self.assertEqual(result.name, "NamedUnion")
        self.assertTrue(type(result) is UnionInfo)

    def test_class_like_union(self):
        node = find_by_name(self.cursor, "ClassLikeUnion")
        result = ClassInfo.from_cursor(node)
        self.assertEqual(result.name, "ClassLikeUnion")
        self.assertEqual(len(result.content), 1)
        result: UnionInfo = result.content[0]
        self.assertEqual(result.name, None)
        self.assertTrue(type(result) is UnionInfo)
        self.assertEqual(len(result.content), 2)


