import os
import sys
import unittest
from pathlib import Path
import clang.cindex
import clang
from devana.syntax_abstraction.organizers.sourcefile import SourceFile, SourceFileType
from devana.syntax_abstraction.classinfo import *


class TestSourceFile(unittest.TestCase):

    def test_creation(self):
        with self.subTest("Create from cursor"):
            index = clang.cindex.Index.create()
            cursor: cindex.Cursor = index.parse(os.path.dirname(__file__)
                                                + r"/source_files/multiple_files/file_1.hpp").cursor
            file = SourceFile.from_cursor(cursor)
            self.assertEqual(file.name, "file_1.hpp")
            self.assertEqual(file.parent, None)
            self.assertEqual(str(file.path.as_posix()),
                             str(Path(os.path.dirname(__file__)
                                      + r"/source_files/multiple_files/file_1.hpp").as_posix()))
            self.assertEqual(file.namespace, None)
            self.assertEqual(file.type, SourceFileType.HEADER)
            self.assertEqual(file.text_source.text.replace("\r\n", "\n"), """class A
{
    int *data;
};""")
            self.assertEqual(file.extension, "hpp")
            self.assertEqual(len(file.content), 1)
            self.assertTrue(file.content[0].name, "A")

        with self.subTest("Create from path"):
            file = SourceFile(os.path.dirname(__file__) + r"/source_files/multiple_files/file_1.hpp")
            self.assertEqual(file.name, "file_1.hpp")
            self.assertEqual(file.parent, None)
            self.assertEqual(str(file.path.as_posix()),
                             str(Path(os.path.dirname(__file__) + r"/source_files/multiple_files/file_1.hpp").
                                 as_posix()))
            self.assertEqual(file.namespace, None)
            self.assertEqual(file.type, SourceFileType.HEADER)
            self.assertEqual(file.text_source.text.replace("\r\n", "\n"), """class A
{
    int *data;
};""")
            self.assertEqual(file.extension, "hpp")
            self.assertEqual(len(file.content), 1)
            self.assertTrue(file.content[0].name, "A")

    def test_extensions(self):
        base_path = os.path.dirname(__file__) + r"/source_files/multiple_files/extensions/file_extension."
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
                file = SourceFile(base_path + ex[0])
                self.assertEqual(file.name, "file_extension." + ex[0])
                self.assertEqual(file.parent, None)
                self.assertEqual(str(file.path.as_posix()), str(Path(base_path + ex[0]).as_posix()))
                self.assertEqual(file.namespace, None)
                self.assertEqual(file.type, ex[1])
                self.assertEqual(file.extension, ex[0])
                self.assertEqual(len(file.content), 1)
                self.assertTrue(file.content[0].name, "A")

    @unittest.skipUnless(sys.platform.startswith("linux"), "requires STD lib")
    def test_simple_include(self):
        file = SourceFile(os.path.dirname(__file__) + r"/source_files/multiple_files/file_2.hpp")
        self.assertEqual(len(file.includes), 3)
        self.assertEqual(file.includes[0].value, "file_1.hpp")
        self.assertEqual(file.includes[0].path, os.path.dirname(__file__) + r"/source_files/multiple_files/file_1.hpp")
        self.assertFalse(file.includes[0].is_standard)
        self.assertEqual(file.includes[1].value, "math.h")
        self.assertTrue(file.includes[1].is_standard)
        self.assertEqual(file.includes[2].value, "cmath")
        self.assertTrue(file.includes[2].is_standard)
        self.assertEqual(len(file.content), 1)
        self.assertEqual(file.content[0].name, "DataA")

    @unittest.skipUnless(sys.platform.startswith("linux"), "requires STD lib")
    def test_include_stand_alone_file(self):
        file = SourceFile(os.path.dirname(__file__) + r"/source_files/multiple_files/file_2.hpp")
        self.assertEqual(len(file.includes), 3)
        self.assertTrue(file.includes[0].source_file is not None)
        self.assertEqual(file.includes[0].source_file.parent, None)
        self.assertEqual(file.includes[0].source_file.text_source.text, """class A
{
    int *data;
};""")

    def test_header_guard_present(self):
        file = SourceFile(os.path.dirname(__file__) + r"/source_files/header_guard/header_guard.hpp")
        self.assertEqual(len(file.includes), 0)
        self.assertEqual(len(file.content), 3)
        self.assertEqual(file.header_guard, "HEADER_GUARD_H")

    def test_header_guard_present_text_before(self):
        file = SourceFile(os.path.dirname(__file__) + r"/source_files/header_guard/header_guard_text_before.hpp")
        self.assertEqual(len(file.includes), 0)
        self.assertEqual(len(file.content), 3)
        self.assertEqual(file.header_guard, "HEADER_GUARD_H")

    def test_header_guard_present_text_after(self):
        file = SourceFile(os.path.dirname(__file__) + r"/source_files/header_guard/header_guard_text_after.hpp")
        self.assertEqual(len(file.includes), 0)
        self.assertEqual(len(file.content), 3)
        self.assertEqual(file.header_guard, "HEADER_GUARD_H")

    def test_header_guard_present_comment(self):
        file = SourceFile(os.path.dirname(__file__) + r"/source_files/header_guard/header_guard_comment.hpp")
        self.assertEqual(len(file.includes), 0)
        self.assertEqual(len(file.content), 3)
        self.assertEqual(file.header_guard, "HEADER_GUARD_H")

    def test_header_guard_missing(self):
        file = SourceFile(os.path.dirname(__file__) + r"/source_files/header_guard/no_header_guard.hpp")
        self.assertEqual(len(file.includes), 0)
        self.assertEqual(len(file.content), 3)
        self.assertEqual(file.header_guard, None)

    def test_header_guard_missing_internal_define(self):
        file = SourceFile(os.path.dirname(__file__) + r"/source_files/header_guard/no_header_guard_internal_ifdef.hpp")
        self.assertEqual(len(file.includes), 0)
        self.assertEqual(len(file.content), 3)
        self.assertEqual(file.header_guard, None)

    def test_headers_already_included_in_other_header(self):
        file = SourceFile(os.path.dirname(__file__) + r"/source_files/complex_includes/include_3.hpp")
        self.assertEqual(len(file.includes), 2)
        self.assertEqual(file.includes[0].value, "include_2.hpp")
        self.assertEqual(file.includes[1].value, "include_1.hpp")

    def test_headers_directory_in_folder(self):
        file = SourceFile(os.path.dirname(__file__) + r"/source_files/complex_includes/include_4.hpp")
        self.assertEqual(len(file.includes), 1)
        self.assertEqual(file.includes[0].value, "subdir/subinc.hpp")
