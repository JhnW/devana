import unittest
import clang.cindex
import clang
import os
from devana.syntax_abstraction.usingnamespace import UsingNamespace
from devana.syntax_abstraction.organizers.sourcefile import SourceFile


class TestUsingNamespace(unittest.TestCase):

    def setUp(self):
        index = clang.cindex.Index.create()
        self.cursor = index.parse(os.path.dirname(__file__) + r"/source_files/using_namespace.hpp").cursor
        self.file = SourceFile(self.cursor)

    def test_simple_using(self):
        nodes = list(self.cursor.get_children())
        result = UsingNamespace(nodes[1])
        self.assertTrue(result.namespaces, ["foo"])
        self.assertTrue(result.namespace, "foo")

        nodes = list(self.cursor.get_children())
        result = UsingNamespace(nodes[2])
        self.assertTrue(result.namespaces, ["foo", "bar"])
        self.assertTrue(result.namespace, "bar")

    def test_content(self):
        result = self.file.allowed_namespaces
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], self.file.content[0].lexicon)
        self.assertEqual(result[1], self.file.content[0].content[2].lexicon)

