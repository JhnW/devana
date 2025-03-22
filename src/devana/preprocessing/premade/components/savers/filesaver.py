from typing import  Type, Iterable, Optional, Callable
from dataclasses import dataclass
from abc import ABC, abstractmethod
from pathlib import Path
from devana.preprocessing.preprocessor import IDestination

class IDestiny(ABC):
    """The basic element on which FileSaver operates."""

    @property
    @abstractmethod
    def name(self) -> str:
        """The name of the file, including the extension. This will be used to save as the file name."""

    @property
    @abstractmethod
    def content(self) -> str:
        """The contents of the file as test - it will be saved."""

    @property
    @abstractmethod
    def path_prefix(self) -> Optional[Path]:
        """If set, it will be added to the root write path after which further path modifications are allowed."""


class FileSaver(IDestination):
    """Implementation that provides text file saving. It supports dynamically generated paths
    (in real use, probably based on the file extension extracted from the name) and supports defined path prefixes."""

    @dataclass
    class Configuration:
        """Core FileSaver configuration"""
        root_path: Path
        """Base path relative to which prefixes are added."""
        path_prefix_generator: Optional[Callable[[IDestiny], Path]] = None
        """If it exists, the function is called for each IDestiny and the generated prefix is
        appended after the fixed prefix from the IDestiny."""

    def __init__(self, configuration: Configuration):
        self._configuration = configuration

    @property
    def configuration(self) -> Configuration:
        """Current configuration."""
        return self._configuration

    @classmethod
    def get_required_type(cls) -> Type:
        return IDestiny

    def consume(self, data: Iterable[IDestiny]) -> Optional[IDestination.Artifacts]:
        result = IDestination.Artifacts()
        for d in data:
            root_path = self._configuration.root_path
            if d.path_prefix is not None:
                root_path /= d.path_prefix
            if self._configuration.path_prefix_generator is not None:
                root_path /= self._configuration.path_prefix_generator(d)
            path = root_path / d.name
            with open(path, "tw", encoding="utf-8") as f:
                f.write(d.content)
            result.files.append(path)
        return result
