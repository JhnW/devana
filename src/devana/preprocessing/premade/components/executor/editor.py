from typing import Any, Optional
from pathlib import Path
from abc import ABC, abstractmethod
from devana.preprocessing.premade.components.savers.filesaver import IDestiny
from devana.syntax_abstraction.organizers.sourcefile import SourceFile
from devana.code_generation.printers.default.defaultprinter import create_default_printer


class IEditable(ABC):
    """Basic interface for an object to an edition in the context of calling preprocessor."""

    @property
    @abstractmethod
    def editable(self) -> Any:
        """Should return an editable object."""

    @property
    @abstractmethod
    def destiny(self) -> IDestiny:
        """Should give information of destiny of content.
        If an editable object has similarity information inside it, this property has higher priority. """

class SourceFileEditor(IEditable):
    """Implementation fof C/C++ source file.
    Please remember that name, path and other information like that from source file instance will be ignored in the
    context of destiny."""

    def __init__(self, name: str, path_prefix: Optional[Path] = None, source: Optional[SourceFile] = None):
        self._destiny = SourceFileDestiny(self)
        self.source = source if source is not None else SourceFile()
        if source is None:
            self.source.header_guard = name.upper()
        self.name = name
        self.path_prefix = path_prefix


    @property
    def editable(self) -> Any:
        return self.source

    @property
    def destiny(self) -> IDestiny:
        return self._destiny


class SourceFileDestiny(IDestiny):
    """Source file destiny to using editable parent information and code printer to generate content."""

    def __init__(self, parent: SourceFileEditor):
        self._parent = parent
        self._printer = create_default_printer()

    @property
    def name(self) -> str:
        return self._parent.name

    @property
    def content(self) -> str:
        return self._printer.print(self._parent.source)

    @property
    def path_prefix(self) -> Optional[Path]:
        return self._parent.path_prefix
