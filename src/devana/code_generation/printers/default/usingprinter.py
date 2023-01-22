from typing import Optional
from devana.code_generation.printers.icodeprinter import ICodePrinter
from devana.code_generation.printers.dispatcherinjectable import DispatcherInjectable
from devana.code_generation.printers.configuration import PrinterConfiguration
from devana.code_generation.printers.formatter import Formatter
from devana.syntax_abstraction.using import Using
from devana.syntax_abstraction.typeexpression import TypeExpression
from devana.syntax_abstraction.classinfo import InheritanceInfo


class UsingPrinter(ICodePrinter, DispatcherInjectable):
    """Printer for using syntax."""

    def print(self, source: Using, config: Optional[PrinterConfiguration] = None,
              context: Optional = None) -> str:
        if config is None:
            config = PrinterConfiguration()
        formatter = Formatter(config)
        if isinstance(context, (TypeExpression, InheritanceInfo.InheritanceValue)):
            return source.name

        if source.associated_comment:
            formatter.print_line(self.printer_dispatcher.print(source.associated_comment, config, source))
        formatter.line = f"using {source.name} = {self.printer_dispatcher.print(source.type_info, config, source)};"
        formatter.next_line()
        return formatter.text
