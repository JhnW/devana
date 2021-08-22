from devana.code_generation.printers.icodeprinter import ICodePrinter
from devana.syntax_abstraction.functioninfo import FunctionInfo, FunctionModification
from devana.syntax_abstraction.classinfo import ClassInfo
from devana.code_generation.printers.dispatcherinjectable import DispatcherInjectable
from devana.code_generation.printers.configuration import PrinterConfiguration
from devana.code_generation.printers.formatter import Formatter
from typing import Optional


class FunctionPrinter(ICodePrinter, DispatcherInjectable):

    @staticmethod
    def _is_modification_scope(source: FunctionInfo) -> bool:
        """Determine to print modifications only in class scope."""
        mod: FunctionModification = source.modification
        if mod.is_explicit or mod.is_final or mod.is_virtual or mod.is_override:
            if type(source.parent) is ClassInfo:
                return True
        return False

    def print(self, source: FunctionInfo, config: Optional[PrinterConfiguration] = None, _=None) -> str:
        if config is None:
            config = PrinterConfiguration()
        formatter = Formatter(config)
        return_type = self.printer_dispatcher.print(source.return_type, config, source)
        name = source.name
        args = []
        for arg in source.arguments:
            args.append(self.printer_dispatcher.print(arg, config, source))
        args = ", ".join(args)
        result = f"{return_type} {name}({args})"

        if source.modification.is_static:
            result = "static " + result
        if source.modification.is_inline:
            result = "inline " + result
        if source.modification.is_constexpr:
            result = "constexpr " + result
        if source.modification.is_const:
            result += " const"
        if source.modification.is_volatile:
            result += " volatile"

        if source.modification.is_default:
            result += " = default"
        if source.modification.is_delete:
            result += " = delete"
        if source.modification.is_pure_virtual:
            result = f"virtual {result} = 0"

        if self._is_modification_scope(source):
            if source.modification.is_explicit:
                result = "explicit " + result
            if source.modification.is_final:
                result += " final"
            if source.modification.is_virtual:
                result = "virtual " + result
            if source.modification.is_override:
                result += "override"

        if source.is_declaration:
            result += ";"
            formatter.line = result
            formatter.next_line()
        else:
            formatter.line = result
            formatter.next_line()
            formatter.print_line("{")
            formatter.indent.count += 1
            for line in source.body.splitlines(False):
                formatter.print_line(line)
            formatter.indent.count -= 1
            formatter.print_line("}")
        return formatter.text
