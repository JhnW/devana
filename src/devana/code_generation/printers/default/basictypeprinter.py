from devana.code_generation.printers.icodeprinter import ICodePrinter
from devana.syntax_abstraction.typeexpression import BasicType
from devana.code_generation.printers.dispatcherinjectable import DispatcherInjectable


class BasicTypePrinter(ICodePrinter, DispatcherInjectable):
    """Core type printer."""

    def print(self, source: BasicType, _1=None, _2=None) -> str:
        return source.name
