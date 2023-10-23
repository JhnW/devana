from typing import Optional
from devana.code_generation.printers.icodeprinter import ICodePrinter
from devana.syntax_abstraction.functioninfo import FunctionInfo, FunctionModification
from devana.syntax_abstraction.classinfo import ClassInfo
from devana.syntax_abstraction.externc import ExternC
from devana.code_generation.printers.dispatcherinjectable import DispatcherInjectable
from devana.code_generation.printers.configuration import PrinterConfiguration
from devana.code_generation.printers.formatter import Formatter
from devana.code_generation.printers.default.variableprinter import VariablePrinter
from .utilityprinters import namespaces_string


class FunctionPrinter(ICodePrinter, DispatcherInjectable):
    """Printer for function declaration."""

    @staticmethod
    def _is_modification_scope(source: FunctionInfo) -> bool:
        """Determine to print modifications only in class scope."""
        mod: FunctionModification = source.modification
        if mod.is_explicit or mod.is_final or mod.is_virtual or mod.is_override:
            if isinstance(source.parent, ClassInfo):
                return True
        return False

    def print(self, source: FunctionInfo, config: Optional[PrinterConfiguration] = None,
              context: Optional = None) -> str:
        if config is None:
            config = PrinterConfiguration()
        formatter = Formatter(config)

        if source.associated_comment:
            formatter.print_line(self.printer_dispatcher.print(source.associated_comment, config, source))
        for attribute in config.attributes.filter(source.attributes):
            formatter.print_line(self.printer_dispatcher.print(attribute, config, source))

        template_prefix = ""
        template_suffix = ""
        if source.template:
            parameters = []
            for p in source.template.parameters:
                parameters.append(self.printer_dispatcher.print(p, config, source))
            parameters = ','.join(parameters)
            template_prefix = f"template<{parameters}>"

            specialisation_values = []

            for s in source.template.specialisation_values:
                if isinstance(s, str):
                    specialisation_values.append(s)
                else:
                    specialisation_values.append(self.printer_dispatcher.print(s, config, source))
            if specialisation_values:
                specialisation_values = ','.join(specialisation_values)
                template_suffix = f"<{specialisation_values}>"

        if template_prefix:
            formatter.print_line(template_prefix)

        return_type = ""
        if source.return_type is not None:
            return_type = self.printer_dispatcher.print(source.return_type, config, source)
        if source.namespaces:
            name = namespaces_string(source.namespaces) + "::" + source.name
        else:
            name = source.name
        args = []
        for arg in source.arguments:
            args.append(self.printer_dispatcher.print(arg, config, source))
        args = ", ".join(args)
        if source.return_type is not None:
            result = f"{return_type} {name}{template_suffix}({args})"
        else:
            result = f"{name}{template_suffix}({args})"

        if source.modification.is_static:
            result = "static " + result
        if source.modification.is_inline:
            result = "inline " + result
        if source.modification.is_constexpr:
            result = "constexpr " + result
        if source.modification.is_consteval:
            result = "consteval " + result
        if source.modification.is_const:
            result += " const"
        if source.modification.is_volatile:
            result += " volatile"
        if source.modification.is_noexcept:
            result += " noexcept"

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

        if source.prefix:
            result = f"{source.prefix} {result}"

        if source.is_declaration:
            result += ";"
            if isinstance(context, ExternC) and len(context.content) == 1:
                return result  # extern c element will format new line and indent
            else:
                formatter.print_line(result)
        else:
            if not isinstance(context, ExternC) or (isinstance(context, ExternC) and len(context.content) != 1):
                formatter.line = result
            formatter.next_line()
            formatter.print_line("{")
            formatter.indent.count += 1
            body = source.body.splitlines(False)
            # remove brackets
            if body[0][0] == "{" and body[-1][-1] == "}":
                body[0] = body[0][1:]
                body[-1] = body[-1][:-1]
                if body[0] == "":
                    body = body[1:]
                if body[-1] == "":
                    body = body[:-1]
            for line in body:
                formatter.print_line(line)
            formatter.indent.count -= 1
            if isinstance(context, ExternC) and len(context.content) == 1:
                return result + formatter.text + "}"
            else:
                formatter.print_line("}")
        return formatter.text


class ArgumentPrinter(VariablePrinter):
    """Printer for arguments used in function declaration."""

    def print(self, source: FunctionInfo.Argument, config: Optional[PrinterConfiguration] = None, _=None) -> str:
        result = super().print(source, config)
        attributes = []
        for attribute in config.attributes.filter(source.attributes):
            attributes.append(self.printer_dispatcher.print(attribute, config, source))

        if attributes:
            result = " ".join(attributes) + " " + result
        return result
