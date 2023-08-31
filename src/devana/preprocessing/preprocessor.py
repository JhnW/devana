from typing import List, Optional
from pathlib import Path
import re
from dataclasses import dataclass
from devana.syntax_abstraction.organizers.sourcemodule import SourceModule, SourceFile
from devana.preprocessing.action import Action
from abc import ABC, abstractmethod


@dataclass
class TargetsFilter:
    """Regular expressions to filter files and paths to process."""
    allowed_filter: Optional[List[str]] = None
    forbidden_filter: Optional[List[str]] = None


class PreprocessorGroup:

    def __init__(self, filters: Optional[TargetsFilter]):
        self._filters = filters if filters else TargetsFilter

    def process(self, module: SourceModule):

        allowed = []
        forbidden = []
        if self._filters.allowed_filter:
            for f in self._filters.allowed_filter:
                allowed.append(re.compile(f))
        if self._filters.forbidden_filter:
            for f in self._filters.forbidden_filter:
                forbidden.append(re.compile(f))

        def is_on_list(file_path: str, filter_regex: List) -> bool:
            for regex in filter_regex:
                match = regex.search(file_path)
                if match:
                    return True
            return False

        for file in module.files:
            if forbidden:
                if is_on_list(str(file.path), forbidden):
                    continue
            if allowed:
                if not is_on_list(str(file.path), allowed):
                    continue
            self._process(file)

    def _process(self, target: SourceFile):
        pass
