# SPDX-FileCopyrightText: Copyright (C) <2022> Critical TechWorks, SA
#
# SPDX-License-Identifier: LGPL-2.1-only

import os
import clang
import re
from typing import Optional, List
from dataclasses import dataclass
from devana.syntax_abstraction.organizers.sourcefile import SourceFile
from devana.utility.lazy import LazyNotInit, lazy_invoke
from devana.syntax_abstraction.organizers.lexicon import Lexicon


@dataclass
class ModuleFilter:
    """Regular expressions to filter files and paths."""
    allowed_filter: Optional[List[str]] = None
    forbidden_filter: Optional[List[str]] = None


class SourceModule:
    """Logic unit of code as named collection of source files."""

    def __init__(self, name: str, root_path: str, module_filter: Optional[ModuleFilter] = None,
                 parent: Optional[any] = None):
        self._path = root_path
        self._module_filter = module_filter
        self._parent = parent
        self._files = LazyNotInit
        self._name = name
        self._lexicon = Lexicon()

    @property
    def module_filter(self):
        return self._module_filter

    @property
    def path(self) -> str:
        """Absolute base path of module."""
        return self._path

    @property
    def lexicon(self) -> any:
        """Lexicon linked to module."""
        return self._lexicon

    @property
    def name(self) -> str:
        """Name of module."""
        return self._name

    @property
    @lazy_invoke
    def files(self) -> List[SourceFile]:
        """List of SourceFile from module."""
        self._files = []
        allowed = []
        forbidden = []
        if self._module_filter is not None:
            if self._module_filter.allowed_filter is not None:
                for f in self._module_filter.allowed_filter:
                    allowed.append(re.compile(f))
            if self._module_filter.forbidden_filter is not None:
                for f in self._module_filter.forbidden_filter:
                    forbidden.append(re.compile(f))

        def is_in_filter_list(file_path: str, filter_regex: List):
            for regex in filter_regex:
                match = regex.search(file_path)
                if match:
                    return True
            return False

        compile_args = ["-xc++"]
        for d in os.walk(self.path):
            compile_args.append(r"-I"+d[0])

        index = clang.cindex.Index.create()
        for r, d, f in os.walk(self.path):
            for file in f:
                p = os.path.join(r, file)
                if is_in_filter_list(p, forbidden):
                    continue
                if allowed:
                    if not is_in_filter_list(p, allowed):
                        continue
                cursor = index.parse(p, args=compile_args).cursor
                self._files.append(SourceFile(cursor, self))
        return self._files

    @property
    def parent(self):
        return self._parent

    def search_for_class(self,class_name:str):
        """ Searches for class with given name in the SourceModule. Looks into 4 levels of content inside every file present in the SourceModule """
        from devana.syntax_abstraction.namespaceinfo import NamespaceInfo 
        from devana.syntax_abstraction.classinfo import ClassInfo 
        
        for file in self.files:
            for first_lvl in file.content:
                if type(first_lvl) == ClassInfo:
                    if first_lvl.name == class_name:
                        return first_lvl
                if type(first_lvl) == NamespaceInfo:
                    for second_lvl in first_lvl.content:
                        if type(second_lvl) == ClassInfo:
                            if second_lvl.name == class_name:
                                return second_lvl
                        if type(second_lvl) == NamespaceInfo:
                            for third_lvl in second_lvl.content:
                                if type(third_lvl) == ClassInfo:
                                    if third_lvl.name == class_name:
                                        return third_lvl
                                if type(third_lvl) == NamespaceInfo:
                                    for fourth_lvl in third_lvl.content:
                                        if type(fourth_lvl) == ClassInfo: 
                                            if fourth_lvl.name == class_name:
                                                return fourth_lvl

    def search_for_file(self,file_name:str):
        """Searches for file(s) in SourceModule. If more than one match, returns them all and none if no match."""
        for file in self.files:
            matches = [file for extension in SourceFile.extension if file.name == file_name + extension]
        if len(matches) == 1:
            return matches[0]
        elif len(matches) > 1:
            return matches
        else:
            return None