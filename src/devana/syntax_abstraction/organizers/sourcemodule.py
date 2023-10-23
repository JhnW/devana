import os
import re
from typing import Optional, List, Iterable, Any
from dataclasses import dataclass
from devana.syntax_abstraction.organizers.sourcefile import SourceFile
from devana.syntax_abstraction.organizers.lexicon import Lexicon
from devana.utility.lazy import LazyNotInit
from devana.configuration import Configuration


@dataclass
class ModuleFilter:
    """Regular expressions to filter files and paths."""
    allowed_filter: Optional[List[str]] = None
    forbidden_filter: Optional[List[str]] = None


class SourceModule:
    """Logic unit of code as named collection of source files."""

    def __init__(self, name: str, root_path: str, module_filter: Optional[ModuleFilter] = None,
                 parent: Optional[Any] = None, configuration: Optional[Configuration] = None):
        self._path = root_path
        self._module_filter = module_filter
        self._parent = parent
        self._files = LazyNotInit
        self._name = name
        self._lexicon = Lexicon()
        self._configuration: Configuration = Configuration() if configuration is None else configuration
        self._configuration.validate()

    @property
    def module_filter(self):
        return self._module_filter

    @property
    def path(self) -> str:
        """Absolute base path of module."""
        return self._path

    @property
    def lexicon(self) -> Any:
        """Lexicon linked to module."""
        return self._lexicon

    @property
    def name(self) -> str:
        """Name of module."""
        return self._name

    @property
    def files(self) -> Iterable[SourceFile]:
        """List of SourceFile from module."""
        if not self._configuration.parsing.file_by_file_parsing and self._files is not LazyNotInit:
            for file in self._files: # noqa
                yield file

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

        for r, _, f in os.walk(self.path):
            for file in f:
                p = os.path.join(r, file)
                if is_in_filter_list(p, forbidden):
                    continue
                if allowed:
                    if not is_in_filter_list(p, allowed):
                        continue
                if self._configuration.parsing.file_by_file_parsing:
                    module = SourceModule(self._name, self._path)
                    yield SourceFile(p, module, self._configuration)
                else:
                    self._files.append(SourceFile(p, self, self._configuration))

        if not self._configuration.parsing.file_by_file_parsing:
            for file in self._files:
                yield file

    @property
    def parent(self):
        return self._parent

    @property
    def configuration(self):
        return self._configuration

    @staticmethod
    def get_module(element: Any) -> Optional:
        if isinstance(element, SourceModule):
            return element
        if not hasattr(element, "parent"):
            return None
        return SourceModule.get_module(element.parent)
