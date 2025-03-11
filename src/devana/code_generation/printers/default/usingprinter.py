from typing import Optional
from devana.code_generation.printers.icodeprinter import ICodePrinter
from devana.code_generation.printers.dispatcherinjectable import DispatcherInjectable
from devana.code_generation.printers.configuration import PrinterConfiguration
from devana.code_generation.printers.formatter import Formatter
from devana.syntax_abstraction.using import Using
from devana.syntax_abstraction.typeexpression import TypeExpression
from devana.syntax_abstraction.classinfo import InheritanceInfo


class UsingPrinter(ICodePrinter, DispatcherInjectable):
    """Printer for using syntax."""

    def print(self, source: Using, config: Optional[PrinterConfiguration] = None,
              context: Optional = None) -> str:
        if config is None:
            config = PrinterConfiguration()
        formatter = Formatter(config)
        if isinstance(context, (TypeExpression, InheritanceInfo.InheritanceValue)):
            return source.name

        if source.associated_comment:
            formatter.print_line(self.printer_dispatcher.print(source.associated_comment, config, source))

        template_prefix = ""
        if source.template:
            parameters = []
            for p in source.template.parameters:
                parameters.append(self.printer_dispatcher.print(p, config, source))
            parameters = ','.join(parameters)
            template_prefix = f"template<{parameters}>"
            if source.template.requires:
                template_prefix += " requires"
                for req in source.template.requires:
                    if isinstance(req, str):
                        template_prefix += f" {req}"
                        continue
                    template_prefix += f" {self.printer_dispatcher.print(req, config, source)}"
        if template_prefix:
            formatter.print_line(template_prefix)

        formatter.line = f"using {source.name} = {self.printer_dispatcher.print(source.type_info, config, source)};"
        formatter.next_line()
        return formatter.text
