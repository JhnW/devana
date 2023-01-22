from typing import Optional
from devana.code_generation.printers.icodeprinter import ICodePrinter
from devana.code_generation.printers.dispatcherinjectable import DispatcherInjectable
from devana.code_generation.printers.configuration import PrinterConfiguration
from devana.code_generation.printers.formatter import Formatter
from devana.syntax_abstraction.externc import ExternC


class ExternCPrinter(ICodePrinter, DispatcherInjectable):
    """Printer for extern c syntax."""

    def print(self, source: ExternC, config: Optional[PrinterConfiguration] = None, _=None) -> str:
        if config is None:
            config = PrinterConfiguration()
        formatter = Formatter(config)
        if len(source.content) == 1:
            formatter.print_line('extern "C" ' + self.printer_dispatcher.print(source.content[0], config, source))
        else:
            formatter.print_line('extern "C"')
            formatter.print_line("{")
            formatter.indent.count += 1
            for c in source.content:
                formatter.line += self.printer_dispatcher.print(c, config, source)
            formatter.accumulate_line()
            formatter.indent.count -= 1
            formatter.print_line("}")
        return formatter.text
