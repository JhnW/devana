from devana.code_generation.printers.icodeprinter import ICodePrinter
from devana.code_generation.printers.configuration import PrinterConfiguration
from dataclasses import dataclass
from typing import List, Optional, Dict


@dataclass
class PrinterRecord:
    printer: ICodePrinter
    context: Optional = None

    def print(self, source, config: Optional[PrinterConfiguration] = None, context: Optional = None):
        if config is None:
            config = PrinterConfiguration()
        return self.printer.print(source, config, context)


class PrinterGroup(ICodePrinter):

    def __init__(self):
        self._printers: List[PrinterRecord] = []

    def append(self, printer):
        self._printers.append(printer)

    def print(self, source, config: Optional[PrinterConfiguration] = None, context: Optional = None):
        if not self._printers:
            raise ValueError("Empty printer.")
        printer = None
        for i in range(len(self._printers)):
            p = self._printers[i]
            if context is None:
                if p.context is None:
                    printer = p
                    break
            else:
                if p.context is None:
                    printer = p
                if p.context == type(context):
                    printer = p
                    break

        if printer is None:
            raise ValueError("Cannot match printer.")
        return printer.print(source, config, context)


class CodePrinter(ICodePrinter):

    def __init__(self, configuration: Optional[PrinterConfiguration] = None, is_fallback_allowed=False):
        self._printers: Dict[any, ICodePrinter] = {}
        self._is_fallback_allowed = is_fallback_allowed
        self._configuration = configuration if configuration is not None else PrinterConfiguration()

    @property
    def is_fallback_allowed(self) -> bool:
        return self._is_fallback_allowed

    @is_fallback_allowed.setter
    def is_fallback_allowed(self, value):
        self._is_fallback_allowed = value

    @property
    def configuration(self) -> PrinterConfiguration:
        return self._configuration

    @configuration.setter
    def configuration(self, value):
        self._configuration = value

    def register(self, cls_printer, source_type, context: Optional = None):
        if source_type not in self._printers:
            self._printers[source_type] = PrinterGroup()
        record = PrinterRecord(cls_printer(self), context)
        self._printers[source_type].append(record)

    def print(self, source, config: Optional[PrinterConfiguration] = None, context: Optional = None) -> str:
        cfg = config if config is not None else self.configuration
        if type(source) in self._printers:
            return self._printers[type(source)].print(source, cfg, context)
        if self._is_fallback_allowed:
            for key in self._printers:
                if issubclass(type(source), key):
                    if self._printers[key].is_fallback_handler:
                        return self._printers[key].print(source, cfg, context)
        msg = f"Printer for provided type: {source} do not exist."
        raise ValueError(msg)
