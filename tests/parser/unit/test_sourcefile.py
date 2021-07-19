import unittest
import clang.cindex
import clang
import sys
from devana.syntax_abstraction.organizers.sourcefile import SourceFile, SourceFileType
from devana.syntax_abstraction.classinfo import *
from pathlib import Path


class TestSourceFile(unittest.TestCase):

    def test_creation(self):

        with self.subTest("Create from cursor"):
            index = clang.cindex.Index.create()
            cursor: cindex.Cursor = index.parse(sys.path[0] + r"/source_files/multiple_files/file_1.hpp").cursor
            file = SourceFile(cursor)
            self.assertEqual(file.name, "file_1.hpp")
            self.assertEqual(file.parent, None)
            self.assertEqual(str(file.path.as_posix()), str(Path(sys.path[0] + r"/source_files/multiple_files/file_1.hpp").as_posix()))
            self.assertEqual(file.namespace, None)
            self.assertEqual(file.type, SourceFileType.HEADER)
            self.assertEqual(file.text_source.text, """class A
{
    int *data;
};""")
            self.assertEqual(file.extension, "hpp")
            self.assertEqual(len(file.content), 1)
            self.assertTrue(file.content[0].name, "A")

        with self.subTest("Create from path"):
            file = SourceFile(sys.path[0] + r"/source_files/multiple_files/file_1.hpp")
            self.assertEqual(file.name, "file_1.hpp")
            self.assertEqual(file.parent, None)
            self.assertEqual(str(file.path.as_posix()),
                             str(Path(sys.path[0] + r"/source_files/multiple_files/file_1.hpp").as_posix()))
            self.assertEqual(file.namespace, None)
            self.assertEqual(file.type, SourceFileType.HEADER)
            self.assertEqual(file.text_source.text, """class A
{
    int *data;
};""")
            self.assertEqual(file.extension, "hpp")
            self.assertEqual(len(file.content), 1)
            self.assertTrue(file.content[0].name, "A")

    def test_extensions(self):
        base_path = sys.path[0] + r"/source_files/multiple_files/extensions/file_extension."
        extensions = (
            ("h", SourceFileType.HEADER),
            ("hxx", SourceFileType.HEADER),
            ("hpp", SourceFileType.HEADER),
            ("c", SourceFileType.IMPLEMENTATION),
            ("cc", SourceFileType.IMPLEMENTATION),
            ("cpp", SourceFileType.IMPLEMENTATION),
            ("cxx", SourceFileType.IMPLEMENTATION)
        )

        for ex in extensions:
            with self.subTest(ex[0]):
                file = SourceFile(base_path+ex[0])
                self.assertEqual(file.name, "file_extension."+ex[0])
                self.assertEqual(file.parent, None)
                self.assertEqual(str(file.path.as_posix()), str(Path(base_path+ex[0]).as_posix()))
                self.assertEqual(file.namespace, None)
                self.assertEqual(file.type, ex[1])
                self.assertEqual(file.extension, ex[0])
                self.assertEqual(len(file.content), 1)
                self.assertTrue(file.content[0].name, "A")

    @unittest.skipUnless(sys.platform.startswith("linux"), "requires STD lib")
    def test_simple_include(self):
        file = SourceFile(sys.path[0] + r"/source_files/multiple_files/file_2.hpp")
        self.assertEqual(len(file.includes), 3)
        self.assertEqual(file.includes[0].value, "file_1.hpp")
        self.assertEqual(file.includes[0].path, sys.path[0] + r"/source_files/multiple_files/file_1.hpp")
        self.assertFalse(file.includes[0].is_standard)
        self.assertEqual(file.includes[1].value, "math.h")
        self.assertTrue(file.includes[1].is_standard)
        self.assertEqual(file.includes[2].value, "cmath")
        self.assertTrue(file.includes[2].is_standard)
        self.assertEqual(len(file.content), 1)
        self.assertEqual(file.content[0].name, "DataA")

    @unittest.skipUnless(sys.platform.startswith("linux"), "requires STD lib")
    def test_include_stand_alone_file(self):
        file = SourceFile(sys.path[0] + r"/source_files/multiple_files/file_2.hpp")
        self.assertEqual(len(file.includes), 3)
        self.assertTrue(file.includes[0].source_file is not None)
        self.assertEqual(file.includes[0].source_file.parent, None)
        self.assertEqual(file.includes[0].source_file.text_source.text, """class A
{
    int *data;
};""")

