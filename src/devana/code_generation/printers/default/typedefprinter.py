from devana.code_generation.printers.icodeprinter import ICodePrinter
from devana.code_generation.printers.dispatcherinjectable import DispatcherInjectable
from devana.code_generation.printers.configuration import PrinterConfiguration
from devana.code_generation.printers.formatter import Formatter
from devana.syntax_abstraction.typedefinfo import TypedefInfo
from typing import Optional


class TypedefPrinter(ICodePrinter, DispatcherInjectable):

    def print(self, source: TypedefInfo, config: Optional[PrinterConfiguration] = None, _=None) -> str:
        if config is None:
            config = PrinterConfiguration()
        formatter = Formatter(config)
        formatter.line = f"typedef {self.printer_dispatcher.print(source.type_info, config, source)} {source.name};"
        formatter.next_line()
        return formatter.text
