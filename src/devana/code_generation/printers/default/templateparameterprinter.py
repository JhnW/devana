from devana.code_generation.printers.icodeprinter import ICodePrinter
from devana.syntax_abstraction.templateinfo import TemplateInfo
from devana.code_generation.printers.dispatcherinjectable import DispatcherInjectable


class TemplateParameterPrinter(ICodePrinter, DispatcherInjectable):
    """Printer for template parameter."""

    def print(self, source: TemplateInfo.TemplateParameter, _1=None, _2=None) -> str:
        if isinstance(source.specifier, str):
            text = f"{source.specifier} {source.name}"
        else:
            if len(source.specifier.parameters) == 0:
                text = f"{source.specifier.name} {source.name}"
            else:
                parameters = []
                for p in source.specifier.parameters:
                    parameters.append(self.printer_dispatcher.print(p))
                parameters = ', '.join(parameters)
                text = f"{source.specifier.name}<{parameters}> {source.name}"

        if source.is_variadic:
            return f"{text}..."
        if source.default_value:
            return f"{text} = {source.default_value}"
        return text
