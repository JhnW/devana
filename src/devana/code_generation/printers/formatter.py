from devana.code_generation.printers.configuration import PrinterConfiguration, Indent


class Formatter:
    """A class that helps create text strings based on a known configuration."""

    def __init__(self, config: PrinterConfiguration):
        self._cfg: PrinterConfiguration = config
        self._text: str = ""
        self._line: str = ""

    @property
    def line(self) -> str:
        """Current processing line."""
        return self._line

    @line.setter
    def line(self, value: str):
        self._line = value

    def next_line(self):
        """Format current processing line indent and newline character, next append it to text."""
        self._text += self._cfg.format_line(self._line)
        self._line = ""

    def accumulate_line(self):
        """Append current processing line to text without formatting."""
        self._text += self._line
        self._line = ""

    @property
    def text(self) -> str:
        """Result text."""
        return self._text

    @property
    def indent(self) -> Indent:
        return self._cfg.indent

    def print_line(self, text):
        """Format next part of text and accumulate this to text."""
        self._text += self._cfg.format_line(text)

    def clear(self):
        """Clear formatter state."""
        self._text = ""
        self._line = ""
