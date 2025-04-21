from devana.code_generation.printers.icodeprinter import ICodePrinter
from devana.syntax_abstraction.templateinfo import TemplateInfo
from devana.code_generation.printers.dispatcherinjectable import DispatcherInjectable
from devana.syntax_abstraction.conceptinfo import ConceptUsage


class TemplateParameterPrinter(ICodePrinter, DispatcherInjectable):
    """Printer for template parameter."""

    def print(self, source: TemplateInfo.TemplateParameter, _1=None, _2=None) -> str:
        if isinstance(source.specifier, ConceptUsage):
            text = f"{self.printer_dispatcher.print(source.specifier)} {source.name}"
        else:
            text = f"{source.specifier} {source.name}"

        if source.is_variadic:
            return f"{text}..."
        if source.default_value:
            return f"{text} = {source.default_value}"
        return text
