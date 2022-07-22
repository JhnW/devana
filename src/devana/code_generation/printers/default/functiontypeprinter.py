from devana.code_generation.printers.icodeprinter import ICodePrinter
from devana.code_generation.printers.dispatcherinjectable import DispatcherInjectable
from devana.code_generation.printers.configuration import PrinterConfiguration
from devana.syntax_abstraction.functiontype import FunctionType
from typing import Optional


class FunctionTypePrinter(ICodePrinter, DispatcherInjectable):

    def print(self, source: FunctionType, config: Optional[PrinterConfiguration] = None,
              _: Optional = None) -> str:
        return source.name
