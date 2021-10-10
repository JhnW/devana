from devana.code_generation.printers.icodeprinter import ICodePrinter
from devana.syntax_abstraction.typeexpression import TypeExpression
from devana.syntax_abstraction.templateinfo import GenericTypeParameter
from devana.code_generation.printers.dispatcherinjectable import DispatcherInjectable
from devana.code_generation.printers.configuration import PrinterConfiguration
from typing import Optional


class TypeExpressionPrinter(ICodePrinter, DispatcherInjectable):

    def print(self, source: TypeExpression, config: Optional[PrinterConfiguration] = None, _=None) -> str:
        if config is None:
            config = PrinterConfiguration()
        prefix = ""
        suffix = ""

        if source.modification.is_static:
            prefix = "static "
        if source.modification.is_const:
            prefix += "const "
        if source.modification.is_constexpr:
            prefix += "constexpr "
        if source.modification.is_volatile:
            prefix += "volatile "
        if source.modification.is_restrict:
            prefix += "restrict "
        if source.modification.is_template:
            prefix += "template "

        if source.modification.is_pointer:
            for _ in range(source.modification.pointer_order):
                suffix += r"*"
        elif source.modification.is_reference:
            suffix = r"&"
        elif source.modification.is_rvalue_ref:
            suffix = r"&&"

        namespace = "::".join(source.namespaces)
        if namespace:
            namespace += "::"

        template = ""
        if source.template_arguments:
            template_str_list = []
            for t in source.template_arguments:
                template_str_list.append(self._printer_dispatcher.print(t, config, source))
            template = ",".join(template_str_list)
            template = f"<{template}>"

        return prefix + namespace + self._printer_dispatcher.print(source.details, config, source) + template + suffix


class GenericTypeParameterPrinter(ICodePrinter, DispatcherInjectable):

    def print(self, source: GenericTypeParameter, _1=None, _2=None) -> str:
        return source.name
