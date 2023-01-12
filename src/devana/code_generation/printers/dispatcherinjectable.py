from typing import Optional
from devana.code_generation.printers.icodeprinter import ICodePrinter


class DispatcherInjectable:
    """Mixin class for provide injectable ICodePrinter as internal printer for all types."""

    def __init__(self, printer_dispatcher: Optional = None):
        self._printer_dispatcher = printer_dispatcher

    @property
    def printer_dispatcher(self) -> ICodePrinter:
        return self._printer_dispatcher
