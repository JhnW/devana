from typing import Optional
from devana.code_generation.printers.icodeprinter import ICodePrinter
from devana.code_generation.printers.dispatcherinjectable import DispatcherInjectable
from devana.code_generation.printers.configuration import PrinterConfiguration
from devana.code_generation.printers.formatter import Formatter
from devana.syntax_abstraction.variable import Variable, GlobalVariable
from devana.syntax_abstraction.functiontype import FunctionType


class VariablePrinter(ICodePrinter, DispatcherInjectable):
    """Printer for variable usage."""

    def print(self, source: Variable, config: Optional[PrinterConfiguration] = None, _=None) -> str:
        if config is None:
            config = PrinterConfiguration()
        if isinstance(source.type.details, FunctionType):
            fnc: FunctionType = source.type.details
            return_name = self._printer_dispatcher.print(fnc.return_type, config, source)
            args_names = ", ".join([self._printer_dispatcher.print(arg, config, source) for arg in fnc.arguments])
            prefix = "static " if source.type.modification.is_static else ""
            prefix += "inline " if source.type.modification.is_inline else ""
            mods = ""
            if source.type.modification.is_const:
                mods += "const "
            elif source.type.modification.is_volatile:
                mods += "volatile "
            elif source.type.modification.is_restrict:
                mods += "restrict "
            elif source.type.modification.is_constexpr:
                mods += "constexpr "
            elif source.type.modification.is_mutable:
                mods += "mutable "

            if source.type.modification.is_pointer:
                for _ in range(source.type.modification.pointer_order):
                    mods = mods + r"*"
            elif source.type.modification.is_reference:
                mods = mods + r"&"

            name = mods + source.name
            if source.type.modification.is_array:
                if source.type.modification.array_order is None:
                    name += r"[]"
                else:
                    name += "[" + "][".join(source.type.modification.array_order) + "]"
            result = f"{prefix}{return_name} ({name})({args_names})"
        else:
            result = f"{self.printer_dispatcher.print(source.type, config, source)} {source.name}"
            if source.type.modification.is_array:
                if source.type.modification.array_order is None:
                    result += "[]"
                else:
                    result += "[" + "][".join(source.type.modification.array_order) + "]"
        if source.default_value is not None:
            result += f" = {source.default_value}"

        return result


class GlobalVariablePrinter(VariablePrinter):
    """Printer for global variable declaration."""

    def print(self, source: GlobalVariable, config: Optional[PrinterConfiguration] = None, _=None) -> str:
        if config is None:
            config = PrinterConfiguration()
        result = super().print(source, config)
        formatter = Formatter(config)
        if source.associated_comment:
            formatter.print_line(self.printer_dispatcher.print(source.associated_comment, config, source))
        formatter.print_line(result + ";")
        return formatter.text
