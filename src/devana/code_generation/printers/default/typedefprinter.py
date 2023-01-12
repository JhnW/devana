from typing import Optional
from devana.code_generation.printers.icodeprinter import ICodePrinter
from devana.code_generation.printers.dispatcherinjectable import DispatcherInjectable
from devana.code_generation.printers.configuration import PrinterConfiguration
from devana.code_generation.printers.formatter import Formatter
from devana.syntax_abstraction.typedefinfo import TypedefInfo
from devana.syntax_abstraction.typeexpression import TypeExpression
from devana.syntax_abstraction.classinfo import InheritanceInfo


class TypedefPrinter(ICodePrinter, DispatcherInjectable):
    """Printer for typedefs."""

    def print(self, source: TypedefInfo, config: Optional[PrinterConfiguration] = None,
              context: Optional = None) -> str:
        if config is None:
            config = PrinterConfiguration()
        formatter = Formatter(config)
        if isinstance(context, (TypeExpression, InheritanceInfo.InheritanceValue)):
            return source.name

        if source.associated_comment:
            formatter.print_line(self.printer_dispatcher.print(source.associated_comment, config, source))
        suffix = ""
        if source.type_info.modification.is_array:
            if source.type_info.modification.array_order is None:
                suffix = "[]"
            else:
                suffix = "[" + "][".join(source.type_info.modification.array_order) + "]"
        formatter.line = f"typedef {self.printer_dispatcher.print(source.type_info, config, source)} " \
                         f"{source.name}{suffix};"
        formatter.next_line()
        return formatter.text
