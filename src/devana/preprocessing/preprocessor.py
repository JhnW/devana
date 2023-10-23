from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, List, Type, Iterable, Any
from dataclasses import dataclass


class IInputContract(ABC):
    """Contract that allows you to define what specific type is required."""

    @classmethod
    @abstractmethod
    def get_required_type(cls) -> Type:
        """Specifies the required input type. In common cases should be interfaced."""


class IOutputContract(ABC):
    """Contract that allows you to define what specific type is provided in the output."""

    @classmethod
    @abstractmethod
    def get_produced_type(cls) -> Type:
        """Specifies a result type, typically as an interface."""


class ISource(IOutputContract, ABC):
    """The data source interface for the processor.
    Typical implementation assumes reading files (json or header files) and returning the parsed output of
    the generator, for example, C++ type systems from Devana."""

    @abstractmethod
    def feed(self) -> Iterable[Any]:
        """Create data, one by one."""


class IDestination(IInputContract, ABC):
    """Interface specifying a class that manages the recording of preprocessor output artifacts.
    Typical use case is the generation of c++ code to files on disk, but other outputs are also possible,
    although the artifacts are generally focused on the disk."""

    @dataclass
    class Artifacts:
        """Resulting preprocessor artifacts."""
        files: List[Path]
        """List of touching files."""

    @abstractmethod
    def consume(self, data: Iterable[Any]) -> Optional[Artifacts]:
        """Consume data from generator and save it."""


class IGenerator(IInputContract, IOutputContract, ABC):
    """A preprocessing unit which, based on general input data, generates output data by implementing methods of binding
    input and output data."""

    @abstractmethod
    def generate(self, data: Iterable[Any]) -> Iterable[Any]:
        """Generate data like generate code."""


class Preprocessor:
    """A preprocessor class that, through aggregation, combines the provided data source,
    generator or class that saves input data into one coherent entity.
    It also provides validation contracts of the classes used."""

    def __init__(self, source: ISource, generator: IGenerator, destination: IDestination):
        self._source = source
        self._generator = generator
        self._destination = destination
        if not self._is_contracts_match():
            raise ValueError("Input ad output types do not match.")

    @property
    def generator(self) -> IGenerator:
        return self._generator

    @property
    def source(self) -> ISource:
        return self._source

    @property
    def destination(self) -> IDestination:
        return self._destination

    def process(self) -> Optional[IDestination.Artifacts]:
        return self._process(self._source, self._generator, self._destination)

    def _is_contracts_match(self) -> bool:
        if not issubclass(self._source.get_produced_type(), self._generator.get_required_type()):
            return False
        if not issubclass(self._generator.get_produced_type(), self._destination.get_required_type()):
            return False
        return True

    @staticmethod
    def _process(source: ISource, generator: IGenerator, destination: IDestination) -> Optional[IDestination.Artifacts]:
        return destination.consume(generator.generate(source.feed()))
