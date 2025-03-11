from typing import Optional
from devana.code_generation.printers.icodeprinter import ICodePrinter
from devana.syntax_abstraction.conceptinfo import ConceptInfo
from devana.code_generation.printers.dispatcherinjectable import DispatcherInjectable
from devana.code_generation.printers.configuration import PrinterConfiguration
from devana.code_generation.printers.formatter import Formatter


class ConceptPrinter(ICodePrinter, DispatcherInjectable):
    """Printer for concept declaration."""

    def print(self, source: ConceptInfo, config: Optional[PrinterConfiguration] = None,
              context: Optional = None) -> str:
        if config is None:
            config = PrinterConfiguration()
        formatter = Formatter(config)
        if source.is_requirement:
            parameters = []
            for p in source.parameters:
                parameters.append(self.printer_dispatcher.print(p, config, source))
            parameters = ', '.join(parameters)
            if len(parameters) > 0:
                return f"{source.name}<{parameters}>"
            return source.name
        parameters = []
        for p in source.template.parameters:
            parameters.append(self.printer_dispatcher.print(p, config, source))
        parameters = ', '.join(parameters)
        template_prefix = f"template<{parameters}>"
        formatter.print_line(template_prefix)

        formatter.print_line(f"concept {source.name} = {source.body};")
        return formatter.text
