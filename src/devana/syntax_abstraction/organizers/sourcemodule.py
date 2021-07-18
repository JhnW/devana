from typing import Optional, List
from dataclasses import dataclass
from devana.syntax_abstraction.organizers.sourcefile import SourceFile
from devana.utility.lazy import LazyNotInit, lazy_invoke
from devana.syntax_abstraction.organizers.lexicon import Lexicon
import os
import clang
import re


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
