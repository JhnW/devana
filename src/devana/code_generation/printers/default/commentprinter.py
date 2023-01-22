from typing import Optional
from devana.code_generation.printers.icodeprinter import ICodePrinter
from devana.syntax_abstraction.comment import Comment, CommentMarker
from devana.code_generation.printers.dispatcherinjectable import DispatcherInjectable
from devana.code_generation.printers.configuration import PrinterConfiguration
from devana.code_generation.printers.formatter import Formatter


class CommentPrinter(ICodePrinter, DispatcherInjectable):
    """Printer for comments."""

    def print(self, source: Comment, config: Optional[PrinterConfiguration] = None, context: Optional = None) -> str:
        if config is None:
            config = PrinterConfiguration()
        formatter = Formatter(config)

        if source is None:
            return formatter.text

        if len(source.text) == 0:
            return formatter.text

        if source.marker == CommentMarker.MULTI_LINE and len(source.text) == 1:
            formatter.line = f"/*{source.text[0]}*/"
            formatter.accumulate_line()
            return formatter.text

        if source.marker == CommentMarker.MULTI_LINE:
            formatter.line = "/*"
            formatter.next_line()
        for index, line in enumerate(source.text):
            formatter.line = line if source.marker == CommentMarker.MULTI_LINE else "//" + line
            if index != len(source.text) - 1 or source.marker == CommentMarker.MULTI_LINE:
                formatter.next_line()
            else:
                formatter.accumulate_line()
        if source.marker == CommentMarker.MULTI_LINE:
            formatter.line = "*/"
            formatter.accumulate_line()

        return formatter.text
