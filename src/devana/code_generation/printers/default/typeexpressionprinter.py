from typing import Optional
from devana.code_generation.printers.icodeprinter import ICodePrinter
from devana.syntax_abstraction.typeexpression import TypeExpression
from devana.syntax_abstraction.templateinfo import GenericTypeParameter
from devana.syntax_abstraction.functiontype import FunctionType
from devana.code_generation.printers.dispatcherinjectable import DispatcherInjectable
from devana.code_generation.printers.configuration import PrinterConfiguration


class TypeExpressionPrinter(ICodePrinter, DispatcherInjectable):
    """Printer for syntax of type usage."""

    def print(self, source: TypeExpression, config: Optional[PrinterConfiguration] = None, _=None) -> str:
        if config is None:
            config = PrinterConfiguration()
        if isinstance(source.details, FunctionType):
            return self._print_with_function_pointer(source, config)
        return self._print_with_standard_type(source, config)

    def _print_with_standard_type(self, source: TypeExpression, config: PrinterConfiguration) -> str:
        prefix = ""
        suffix = ""

        if source.modification.is_inline:
            prefix = "inline "
        if source.modification.is_static:
            prefix = "static "
        if source.modification.is_const:
            prefix += "const "
        if source.modification.is_constexpr:
            prefix += "constexpr "
        if source.modification.is_constinit:
            prefix += "constinit "
        if source.modification.is_volatile:
            prefix += "volatile "
        if source.modification.is_restrict:
            prefix += "restrict "
        if source.modification.is_template:
            prefix += "template "
        if source.modification.is_mutable:
            prefix += "mutable "

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

    def _print_with_function_pointer(self, source: TypeExpression, config: PrinterConfiguration) -> str:
        fnc: FunctionType = source.details
        return_name = self._printer_dispatcher.print(fnc.return_type, config, source)
        args_names = ", ".join([self._printer_dispatcher.print(arg, config, source) for arg in fnc.arguments])
        prefix = "static " if source.modification.is_static else ""
        mods = ""
        if source.modification.is_const:
            mods += "const "
        elif source.modification.is_volatile:
            mods += "volatile "
        elif source.modification.is_restrict:
            mods += "restrict "
        elif source.modification.is_constexpr:
            mods += "constexpr "
        elif source.modification.is_mutable:
            mods += "mutable "

        if source.modification.is_pointer:
            for _ in range(source.modification.pointer_order):
                mods = r"*" + mods
        elif source.modification.is_reference:
            mods = r"&" + mods
        elif source.modification.is_array:
            if source.modification.array_order is None:
                mods += r"[]"
            else:
                mods += "[" + "][".join(source.modification.array_order) + "]"
        elif source.modification.is_rvalue_ref:
            mods = r"&&" + mods
        name = f"{prefix}{return_name} ({mods})({args_names})"
        return name


class GenericTypeParameterPrinter(ICodePrinter, DispatcherInjectable):
    """Printer for generic type of template like T."""

    def print(self, source: GenericTypeParameter, _1=None, _2=None) -> str:
        return source.name
