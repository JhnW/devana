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


class TestAdvancedInheritance(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.source = SourceModule("core", os.path.dirname(__file__) + r'/source_files/inheritance')

    @classmethod
    def tearDownClass(self):
        self.source = None
    @classmethod
    def get_file(self, file_name : str):
        for file in self.source.files:
            if file.name == file_name:
                return file

    def test_public_inheritance(self):
        file = self.get_file("child_public.h")
        self.assertEqual(1,len(file.content))
        self.assertEqual(2, len(file.content[0].inheritance.type_parents))

        parent_name = file.content[0].inheritance.type_parents[0].type.name
        self.assertEqual('Parent1',parent_name)

        parent_name = file.content[0].inheritance.type_parents[1].type.name
        self.assertEqual('Parent2',parent_name)

    def test_private_inheritance(self):
        file = self.get_file("child_private.h")
        self.assertEqual(1,len(file.content))
        self.assertEqual(2, len(file.content[0].inheritance.type_parents))

        parent_name = file.content[0].inheritance.type_parents[0].type.name
        self.assertEqual('Parent1', parent_name)

        parent_name = file.content[0].inheritance.type_parents[1].type.name
        self.assertEqual('Parent2', parent_name)

    def test_protected_inheritance(self):
        file = self.get_file("child_protected.h")
        self.assertEqual(1,len(file.content))
        self.assertEqual(2, len(file.content[0].inheritance.type_parents))

        parent_name = file.content[0].inheritance.type_parents[0].type.name
        self.assertEqual('Parent1', parent_name)

        parent_name = file.content[0].inheritance.type_parents[1].type.name
        self.assertEqual('Parent2', parent_name)

    def test_omitted_specifiers(self):
        file = self.get_file("ommited_specifiers.h")
        self.assertEqual(3,len(file.content))
        self.assertEqual(2, len(file.content[2].inheritance.type_parents))

        first_parent_name = file.content[2].inheritance.type_parents[0].type.name
        first_parent_access_spec = file.content[2].inheritance.type_parents[0].access_specifier.value
        self.assertEqual('BaseClass', first_parent_name)
        self.assertEqual('private',first_parent_access_spec)

        second_parent_name = file.content[2].inheritance.type_parents[1].type.name
        second_parent_access_spec = file.content[2].inheritance.type_parents[1].access_specifier.value
        self.assertNotEqual('public',second_parent_access_spec)
        self.assertEqual('BaseStruct',second_parent_name)

    def test_multiple_inheritance(self):
        file = self.get_file("multiple_parents.h")
        self.assertEqual(2,len(file.content))
        self.assertEqual(3,len(file.content[1].inheritance.type_parents))

        first_parent_name = file.content[1].inheritance.type_parents[0].type.name
        first_parent_access_spec = file.content[1].inheritance.type_parents[0].access_specifier.value
        self.assertEqual('Parent1',first_parent_name)
        self.assertEqual('public',first_parent_access_spec)

        second_parent_name = file.content[1].inheritance.type_parents[1].type.name
        second_parent_access_spec = file.content[1].inheritance.type_parents[2].access_specifier.value
        self.assertEqual('Parent2',second_parent_name)
        self.assertEqual('protected',second_parent_access_spec)

        third_parent_access_spec = file.content[1].inheritance.type_parents[1].access_specifier.value
        third_parent_name = file.content[1].inheritance.type_parents[2].type.name
        self.assertEqual('BaseClass',third_parent_name)
        self.assertEqual('private',third_parent_access_spec)
        

    def test_virtual_inheritance(self):
        file = self.get_file("virtual_parent.h")
        self.assertEqual(1,len(file.content))
        self.assertEqual(2,len(file.content[0].inheritance.type_parents))
        
        first_parent = file.content[0].inheritance.type_parents[0]
        self.assertEqual(first_parent.is_virtual, True)
        self.assertEqual(first_parent.access_specifier.value,'public')

        second_parent = file.content[0].inheritance.type_parents[1]
        self.assertEqual(second_parent.is_virtual, True)
        self.assertEqual(second_parent.access_specifier.value,'private')

#
# This test ilustrates that the inheritance feature should not be supported through the source file
# loading. This is because the source_file is not a complete translation unit and does not have any information
# about the parent classes and only the Child class. 
#
class TestInheritanceFromSourceFile(unittest.TestCase):

    def setUp(self):
        arg_compiler=["-xc++", "-std=c++11"]
        index = clang.cindex.Index.create()
        cursor = index.parse(os.path.dirname(__file__) + r"/source_files/inheritance/child_private.h", args=arg_compiler).cursor
        self.src_file = SourceFile(cursor)
        
    def test_advanced_inheritance(self):
        parent_name = self.src_file.content[0].inheritance.type_parents[0].type
        self.assertEqual(None,parent_name)
