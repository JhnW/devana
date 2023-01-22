from typing import Optional
from devana.code_generation.printers.icodeprinter import ICodePrinter
from devana.code_generation.printers.dispatcherinjectable import DispatcherInjectable
from devana.code_generation.printers.configuration import PrinterConfiguration
from devana.syntax_abstraction.functiontype import FunctionType


class FunctionTypePrinter(ICodePrinter, DispatcherInjectable):
    """Printer for function use as type like function pointer."""

    def print(self, source: FunctionType, config: Optional[PrinterConfiguration] = None,
              _: Optional = None) -> str:
        return source.name
