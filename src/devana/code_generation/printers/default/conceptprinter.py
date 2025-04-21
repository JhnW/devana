from typing import Optional
from devana.code_generation.printers.icodeprinter import ICodePrinter
from devana.syntax_abstraction.conceptinfo import ConceptInfo, ConceptUsage
from devana.code_generation.printers.dispatcherinjectable import DispatcherInjectable
from devana.code_generation.printers.configuration import PrinterConfiguration
from devana.code_generation.printers.formatter import Formatter


class ConceptPrinter(ICodePrinter, DispatcherInjectable):
    """Printer for concept definition."""

    def print(self, source: ConceptInfo, config: Optional[PrinterConfiguration] = None,
              context: Optional = None) -> str:
        if config is None:
            config = PrinterConfiguration()
        formatter = Formatter(config)
        if source.associated_comment:
            formatter.print_line(self.printer_dispatcher.print(source.associated_comment, config, source))

        parameters = [self.printer_dispatcher.print(p, config, source) for p in source.template.parameters]
        parameters = ', '.join(parameters)

        formatter.print_line(f"template<{parameters}>")
        formatter.print_line(f"concept {source.name} = {source.body};")
        return formatter.text

class ConceptUsagePrinter(ICodePrinter, DispatcherInjectable):
    """Printer for concept usage."""

    def print(self, source: ConceptUsage, config: Optional[PrinterConfiguration] = None,
              context: Optional = None) -> str:
        name = "::".join((*source.namespaces, source.name))
        if len(source.parameters) == 0:
            return name

        parameters = ', '.join(
            self.printer_dispatcher.print(p, config, source) for p in source.parameters
        )
        return f"{name}<{parameters}>"
