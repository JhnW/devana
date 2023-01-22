from typing import Optional
from devana.code_generation.printers.icodeprinter import ICodePrinter
from devana.code_generation.printers.dispatcherinjectable import DispatcherInjectable
from devana.code_generation.printers.configuration import PrinterConfiguration
from devana.code_generation.printers.formatter import Formatter
from devana.syntax_abstraction.unioninfo import UnionInfo
from devana.syntax_abstraction.typeexpression import TypeExpression


class UnionPrinter(ICodePrinter, DispatcherInjectable):
    """Printer for union declaration."""

    def print(self, source: UnionInfo, config: Optional[PrinterConfiguration] = None, context: Optional = None) -> str:
        if config is None:
            config = PrinterConfiguration()
        formatter = Formatter(config)
        if isinstance(context, TypeExpression):
            return source.name
        else:

            if source.associated_comment:
                formatter.print_line(self.printer_dispatcher.print(source.associated_comment, config, source))

            formatter.line = "union "
            formatter.line += f"{source.name}"
            if source.is_declaration:
                formatter.line += ";"
                formatter.next_line()
            else:
                formatter.next_line()
                formatter.print_line("{")
                formatter.indent.count += 1
                for element in source.content:
                    formatter.line += self.printer_dispatcher.print(element, config, source)
                formatter.accumulate_line()
                formatter.indent.count -= 1
                formatter.print_line("};")
            return formatter.text
