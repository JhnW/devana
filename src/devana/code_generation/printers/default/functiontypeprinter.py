from devana.syntax_abstraction.functiontype import FunctionType
from devana.code_generation.printers.icodeprinter import ICodePrinter
from devana.syntax_abstraction.functioninfo import FunctionInfo, FunctionModification
from devana.syntax_abstraction.classinfo import ClassInfo
from devana.syntax_abstraction.externc import ExternC
from devana.code_generation.printers.dispatcherinjectable import DispatcherInjectable
from devana.code_generation.printers.configuration import PrinterConfiguration
from devana.code_generation.printers.formatter import Formatter
from .utilityprinters import namespaces_string
from typing import Optional
from devana.syntax_abstraction.functiontype import FunctionType


class FunctionTypePrinter(ICodePrinter, DispatcherInjectable):

    def print(self, source: FunctionType, config: Optional[PrinterConfiguration] = None,
              _: Optional = None) -> str:
        return  source.name
