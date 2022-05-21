from devana.code_generation.printers.icodeprinter import ICodePrinter
from devana.syntax_abstraction.variable import Variable, GlobalVariable
from devana.code_generation.printers.dispatcherinjectable import DispatcherInjectable
from devana.code_generation.printers.configuration import PrinterConfiguration
from devana.code_generation.printers.formatter import Formatter
from typing import Optional


class VariablePrinter(ICodePrinter, DispatcherInjectable):

    def print(self, source: Variable, config: Optional[PrinterConfiguration] = None, _=None) -> str:
        if config is None:
            config = PrinterConfiguration()
        result = f"{self.printer_dispatcher.print(source.type, config, source)} {source.name}"
        if source.type.modification.is_array:
            if source.type.modification.array_order is None:
                result += "[]"
            else:
                result += "["+"][".join(source.type.modification.array_order) + "]"
        if source.default_value is not None:
            result += f" = {source.default_value}"
        return result


class GlobalVariablePrinter(ICodePrinter, DispatcherInjectable):

    def print(self, source: GlobalVariable, config: Optional[PrinterConfiguration] = None, _=None) -> str:
        if config is None:
            config = PrinterConfiguration()
        result = f"{self.printer_dispatcher.print(source.type, config, source)} {source.name}"
        if source.default_value is not None:
            result += f" = {source.default_value}"
        formatter = Formatter(config)
        if source.associated_comment:
            formatter.print_line(self.printer_dispatcher.print(source.associated_comment, config, source))
        formatter.print_line(result+";")
        return formatter.text
