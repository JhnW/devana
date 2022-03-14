# SPDX-FileCopyrightText: Copyright (C) <2022> Critical TechWorks, SA
#
# SPDX-License-Identifier: LGPL-2.1-only

import unittest
import clang.cindex
import clang
import os
import sys
from devana.syntax_abstraction.organizers.sourcefile import SourceFile
from devana.syntax_abstraction.organizers.sourcemodule import SourceModule
from devana.syntax_abstraction.classinfo import *
from pathlib import Path

class TestHeaderGuards(unittest.TestCase):
    @classmethod    
    def setUp(self):
        self.source = SourceModule("core", os.path.dirname(__file__) + r'/source_files/header_guard')

    @classmethod
    def get_file(self, file_name : str):
        for file in self.source.files:
            if file.name == file_name:
                return file

    def test_header_guard_present_first_case(self):
        file = self.get_file("header_guard_first_case.hpp")
        self.assertEqual(len(file.includes), 0)
        self.assertEqual(len(file.content), 3)
        self.assertEqual(file.header_guard, "HEADER_GUARD_H")

    def test_header_guard_present_second_case(self):
        file = self.get_file("header_guard_second_case.hpp")
        self.assertEqual(len(file.includes), 0)
        self.assertEqual(len(file.content), 3)
        self.assertEqual(file.header_guard, "HEADER_GUARD_H")

    def test_header_guard_present_third_case(self):
        file = self.get_file("header_guard_third_case.hpp")
        self.assertEqual(len(file.includes), 0)
        self.assertEqual(len(file.content), 3)
        self.assertEqual(file.header_guard, "HEADER_GUARD_H")
        
    def test_header_guard_present_fourth_case(self):
        file = self.get_file("header_guard_fourth_case.hpp")
        self.assertEqual(len(file.includes), 0)
        self.assertEqual(len(file.content), 3)
        self.assertEqual(file.header_guard, "HEADER_GUARD_H")

    def test_header_guard_no_new_line_eof(self):
        file = self.get_file("header_guard_no_eof.hpp")
        self.assertEqual(len(file.includes), 0)
        self.assertEqual(len(file.content), 3)
        self.assertEqual(file.header_guard, "HEADER_GUARD_H")        

    def test_header_guard_missing(self):
        file = SourceFile(os.path.dirname(__file__) + r"/source_files/header_guard/no_header_guard.hpp")
        self.assertEqual(len(file.includes), 0)
        self.assertEqual(len(file.content), 3)
        self.assertEqual(file.header_guard, None)


    def test_header_g(self):
        file = self.get_file("header_guard_fourth_case.hpp")
        text = file.text_source.text.split("\n")
        import re
        for index, line in enumerate(text):
            match = re.match(r"^#ifndef\s(\S+)", line )
            if not match:
                continue
            if len(match.group()) < 1:
                continue
            def_name = match.group(1)
            match = None
            if index <= len(text) -2 :
                match = re.match(r"^#define\s(\S+)", text[index+1])
            if not match:
                print("did not match")
                continue
            if len(match.group()) < 1:
                print("did not match")
                continue
            if match.group(1) != def_name:
                print("did not match")
                continue

            regex1 = r"#endif([\s]+)?//(.*)"
            regex2 = r"#endif([\s]+)?/\*(.*)\*/([\s]+)?$"
            regex3 = r"#endif([\s]+)?$"
            index = 1
            if not re.search( r"\S$", text[-index]):
                index = index + 1
            if not re.match( regex1 +"|"+ regex2 + "|" + regex3 , text[-index]):
                continue

            _header_guard = def_name
