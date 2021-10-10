from devana.code_generation.printers.icodeprinter import ICodePrinter
from devana.code_generation.printers.dispatcherinjectable import DispatcherInjectable
from devana.code_generation.printers.configuration import PrinterConfiguration
from devana.code_generation.printers.formatter import Formatter
from devana.syntax_abstraction.namespaceinfo import NamespaceInfo
from typing import Optional


class NamespacePrinter(ICodePrinter, DispatcherInjectable):

    def print(self, source: NamespaceInfo, config: Optional[PrinterConfiguration] = None, _=None) -> str:
        if config is None:
            config = PrinterConfiguration()
        formatter = Formatter(config)
        formatter.print_line(f"namespace {source.name}")
        formatter.print_line("{")
        formatter.indent.count += 1
        for c in source.content:
            formatter.line += self.printer_dispatcher.print(c, config, source)
        formatter.accumulate_line()
        formatter.indent.count -= 1
        formatter.print_line("}")
        return formatter.text
