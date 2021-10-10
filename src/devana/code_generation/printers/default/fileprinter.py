from devana.code_generation.printers.icodeprinter import ICodePrinter
from devana.code_generation.printers.dispatcherinjectable import DispatcherInjectable
from devana.code_generation.printers.configuration import PrinterConfiguration
from devana.code_generation.printers.formatter import Formatter
from devana.syntax_abstraction.organizers.sourcefile import SourceFile, IncludeInfo
from typing import Optional


class FilePrinter(ICodePrinter, DispatcherInjectable):

    def print(self, source: SourceFile, config: Optional[PrinterConfiguration] = None, context: Optional = None) -> str:
        if config is None:
            config = PrinterConfiguration()
        formatter = Formatter(config)
        for include in source.includes:
            formatter.line += self.printer_dispatcher.print(include, config, source)
        if source.includes and source.content:
            formatter.next_line()
        for element in source.content:
            formatter.line += self.printer_dispatcher.print(element, config, source)
        formatter.next_line()
        return formatter.text


class IncludePrinter(ICodePrinter, DispatcherInjectable):

    def print(self, source: IncludeInfo, config: Optional[PrinterConfiguration] = None,
              context: Optional = None) -> str:
        if config is None:
            config = PrinterConfiguration()
        formatter = Formatter(config)
        formatter.line = f"#inlude "
        if source.is_standard:
            value_begin = "<"
            value_end = ">"
        else:
            value_begin = '"'
            value_end = value_begin
        formatter.line += f"{value_begin}{source.value}{value_end}"
        formatter.next_line()
        return formatter.text
