from typing import Optional
from devana.syntax_abstraction.usingnamespace import UsingNamespace
from devana.code_generation.printers.icodeprinter import ICodePrinter
from devana.code_generation.printers.dispatcherinjectable import DispatcherInjectable
from devana.code_generation.printers.configuration import PrinterConfiguration
from devana.code_generation.printers.formatter import Formatter
from .utilityprinters import namespaces_string


class UsingNamespacePrinter(ICodePrinter, DispatcherInjectable):
    """Printer for using namespace syntax."""

    def print(self, source: UsingNamespace, config: Optional[PrinterConfiguration] = None, _: Optional = None) -> str:
        if config is None:
            config = PrinterConfiguration()
        formatter = Formatter(config)
        formatter.line = "using namespace "
        formatter.line += f"{namespaces_string(source.namespaces)};"
        formatter.next_line()
        return formatter.text
