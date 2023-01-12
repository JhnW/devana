from typing import Optional
from devana.code_generation.printers.icodeprinter import ICodePrinter
from devana.syntax_abstraction.attribute import AttributeDeclaration, Attribute
from devana.code_generation.printers.dispatcherinjectable import DispatcherInjectable
from devana.code_generation.printers.configuration import PrinterConfiguration


class AttributeDeclarationPrinter(ICodePrinter, DispatcherInjectable):
    """Printer for attribute."""

    def print(self, source: AttributeDeclaration, config: Optional[PrinterConfiguration] = None,
              context: Optional = None) -> str:
        if config is None:
            config = PrinterConfiguration()

        namespace = "" if source.using_namespace is None else f"using {source.using_namespace} : "
        attrs = ", ".join([self.printer_dispatcher.print(attr, config, source) for attr in source.attributes])

        return f"[[{namespace}{attrs}]]"


class AttributePrinter(ICodePrinter, DispatcherInjectable):
    """Printer for code attribute."""

    def print(self, source: Attribute, config: Optional[PrinterConfiguration] = None, context: Optional = None) -> str:
        args = "" if source.arguments is None else f'({",".join(source.arguments)})'
        namespace = "" if source.namespace is None or (source.namespace == "") else f"{source.namespace}::"
        if isinstance(context, AttributeDeclaration):
            if context.using_namespace == source.namespace:
                namespace = ""
        return f"{namespace}{source.name}{args}"
