# SPDX-FileCopyrightText: Copyright (C) <2022> Critical TechWorks, SA
#
# SPDX-License-Identifier: LGPL-2.1-only

from distutils.command.build_scripts import first_line_re
import unittest
import clang.cindex
import clang
import os
from tests.helpers import find_by_name
from devana.syntax_abstraction.typeexpression import BasicType, TypeModification
from devana.syntax_abstraction.classinfo import *
from devana.syntax_abstraction.organizers.sourcemodule import SourceModule
from devana.syntax_abstraction.organizers.sourcefile import SourceFile


class TestCommentParsing(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.source = SourceModule("core", os.path.dirname(__file__) + r'/source_files/comments')
        self.file = self.get_file("comments.h")    
    @classmethod
    def tearDownClass(self):
        self.source = None

    @classmethod
    def get_file(self, file_name : str):
        for file in self.source.files:
            if file.name == file_name:
                return file

    def get_method(self, method_name : str):
        for file in self.source.files:
            for content in file.content:
                for cls in content.content:
                    for method in cls.methods:
                            if method.name == method_name:
                                return method

    
    def test_class_documentation(self):
        expected_comment = "This is the documentation for the Example."
        expected_name = "example"
        
        self.assertEqual(1,len(self.file.content))
        self.assertEqual(expected_name, self.file.content[0].name)

        comment = self.file.content[0].content[0].documentation
        self.assertEqual(expected_comment,comment)

    def test_method_documentation(self):
        expected_comment = "Returns 42"
        expected_name = "example"
        
        self.assertEqual(1,len(self.file.content))
        self.assertEqual(expected_name, self.file.content[0].name)

        method = self.get_method("doSomething")
        comment = method.documentation
        self.assertEqual(expected_comment,comment)
