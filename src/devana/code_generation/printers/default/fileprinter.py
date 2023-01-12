from typing import Optional
from devana.code_generation.printers.icodeprinter import ICodePrinter
from devana.code_generation.printers.dispatcherinjectable import DispatcherInjectable
from devana.code_generation.printers.configuration import PrinterConfiguration
from devana.code_generation.printers.formatter import Formatter
from devana.syntax_abstraction.organizers.sourcefile import SourceFile, IncludeInfo


class FilePrinter(ICodePrinter, DispatcherInjectable):
    """Printer for whole file."""

    def print(self, source: SourceFile, config: Optional[PrinterConfiguration] = None, context: Optional = None) -> str:
        if config is None:
            config = PrinterConfiguration()
        formatter = Formatter(config)

        if source.preamble:
            formatter.print_line(self.printer_dispatcher.print(source.preamble, config, source))
            formatter.next_line()

        if source.header_guard:
            formatter.print_line(f"#ifndef {source.header_guard}")
            formatter.print_line(f"#define {source.header_guard}")
            formatter.next_line()

        for include in source.includes:
            formatter.line += self.printer_dispatcher.print(include, config, source)
        if source.includes and source.content:
            formatter.next_line()

        for element in source.content:
            formatter.line += self.printer_dispatcher.print(element, config, source)
        formatter.next_line()

        if source.header_guard:
            formatter.print_line(f"#endif //{source.header_guard}")

        return formatter.text


class IncludePrinter(ICodePrinter, DispatcherInjectable):
    """Printer for include directive."""

    def print(self, source: IncludeInfo, config: Optional[PrinterConfiguration] = None,
              context: Optional = None) -> str:
        if config is None:
            config = PrinterConfiguration()
        formatter = Formatter(config)
        formatter.line = "#include "
        if source.is_standard:
            value_begin = "<"
            value_end = ">"
        else:
            value_begin = '"'
            value_end = value_begin
        formatter.line += f"{value_begin}{source.value}{value_end}"
        formatter.next_line()
        return formatter.text
