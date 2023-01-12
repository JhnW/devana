from devana.code_generation.printers.icodeprinter import ICodePrinter
from devana.syntax_abstraction.templateinfo import TemplateInfo
from devana.code_generation.printers.dispatcherinjectable import DispatcherInjectable


class TemplateParameterPrinter(ICodePrinter, DispatcherInjectable):
    """Printer for template parameter."""

    def print(self, source: TemplateInfo.TemplateParameter, _1=None, _2=None) -> str:

        text = f"{source.specifier} {source.name}"
        if source.is_variadic:
            return f"{text}..."
        if source.default_value:
            return f"{text} = {source.default_value}"
        return text
