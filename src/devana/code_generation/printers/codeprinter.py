from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from devana.code_generation.printers.icodeprinter import ICodePrinter
from devana.code_generation.printers.configuration import PrinterConfiguration


@dataclass
class PrinterRecord:
    """Light abstraction layer for a printer that does not implement the full set of functionalities. """
    printer: ICodePrinter
    context: Optional = None

    def print(self, source, config: Optional[PrinterConfiguration] = None, context: Optional = None):
        if config is None:
            config = PrinterConfiguration()
        return self.printer.print(source, config, context)


class PrinterGroup(ICodePrinter):
    """Collection of low-level printers for one type. Helps you find the right printer for context requirements."""

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
    """Collection of low-level printers for many types. CodePrinter will match correct printer to source object type."""

    def __init__(self, configuration: Optional[PrinterConfiguration] = None, is_fallback_allowed=False):
        self._printers: Dict[Any, ICodePrinter] = {}
        self._is_fallback_allowed = is_fallback_allowed
        self._configuration = configuration if configuration is not None else PrinterConfiguration()

    @property
    def is_fallback_allowed(self) -> bool:
        """Determines whether in the absence of a printer for a given type,
        it is possible to use a printer of its base type. """
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
        """Add a new printer to the collection of the given type."""
        if source_type not in self._printers:
            self._printers[source_type] = PrinterGroup()
        record = PrinterRecord(cls_printer(self), context)
        self._printers[source_type].append(record) # noqa

    def print(self, source, config: Optional[PrinterConfiguration] = None, context: Optional = None) -> str:
        """Prints code from a given source dynamically looking for suitable printers."""
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
