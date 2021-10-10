from abc import ABC, abstractmethod
from typing import Optional
from devana.code_generation.printers.configuration import PrinterConfiguration


class ICodePrinter(ABC):
    """Common interface for all printers."""

    @abstractmethod
    def print(self, source, config: Optional[PrinterConfiguration] = None, context: Optional = None) -> str:
        pass

    @property
    def is_fallback_handler(self) -> bool:
        return False
