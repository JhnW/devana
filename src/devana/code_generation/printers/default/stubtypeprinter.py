from devana.code_generation.printers.icodeprinter import ICodePrinter
from devana.code_generation.printers.dispatcherinjectable import DispatcherInjectable
from devana.code_generation.stubtype import StubType


class StubTypePrinter(ICodePrinter, DispatcherInjectable):

    def print(self, source: StubType, _1=None, _2=None) -> str:
        return source.name
