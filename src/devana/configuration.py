from enum import Enum, auto
from dataclasses import dataclass, field
import logging
import platform
from pathlib import Path
from abc import ABC, abstractmethod
from typing import List, Optional, Any


class IValidateConfig(ABC):
    """Every sub-config should implement this interface to provide cohesion and implementation check."""

    @abstractmethod
    def validate(self):
        """This method do not return value. Each problem should be reported as an appropriate exception.
        This exception will be propagated to the client using the library."""


@dataclass
class CommentsParsing(IValidateConfig):
    """The class defines how and how extensively the parsing of comments in the code is performed."""

    accumulate: bool = True
    """Setting that defines whether consecutive C ++ style one-line comments starting
    with '//' will be combined into a single collective instance."""
    unpinned_comments_allowed: bool = False
    """Specifies whether to parse or omit comments that are not attached to the code
    (they do not precede classes, functions, type definitions, class fields, methods, etc.).
    This does not affect the parsing of the file preamble."""
    deep_parsing: bool = False
    """Defines parsing of additional content, e.g. comments to function arguments."""
    remove_blank_lines: bool = True
    """If the first and last lines are empty (after initial processing by other rules) they will be deleted."""
    remove_asterisks: bool = True
    """Removal of leading '*' characters from text parsing and subsequent whitespace."""

    def validate(self):
        if self.deep_parsing:
            raise NotImplementedError("Deep parsing is not implemented for now.")
        if self.unpinned_comments_allowed:
            raise NotImplementedError("Unpinned comments is not implemented for now.")


class LanguageStandard(Enum):
    """Defines according to the rules which language version the parsing of files will take place."""

    class LanguageStandardData:
        """Version of C++ or C standard."""

        def __init__(self, options: List[str], value):
            self._value = value
            self._options = options

        @property
        def _compiler_option(self) -> List[str]:
            """Compiler option, for internal usage."""
            return self._options

        @property
        def options(self) -> List[str]:
            return self._options

    C_89 = LanguageStandardData(["-std=c89"], auto())
    C_99 = LanguageStandardData(["-std=c99"], auto())
    C_11 = LanguageStandardData(["-std=c11"], auto())
    C_17 = LanguageStandardData(["-std=c17"], auto())
    CPP_98 = LanguageStandardData(["-xc++", "-std=c++98"], auto())
    CPP_03 = LanguageStandardData(["-xc++", "-std=c++98"], auto())
    CPP_11 = LanguageStandardData(["-xc++", "-std=c++11"], auto())
    CPP_17 = LanguageStandardData(["-xc++", "-std=c++17"], auto())
    CPP_20 = LanguageStandardData(["-xc++", "-std=c++20"], auto())

    @classmethod
    def create_default(cls):
        return cls.CPP_17


class ParsingErrorPolicy(Enum):
    """Rules for dealing with errors when parsing."""
    IGNORE = auto()
    """Ignore all errors."""
    LOG = auto()
    """Only log error."""
    ABORT = auto()
    """Throw exception."""

    @classmethod
    def create_default(cls):
        return cls.IGNORE


class StandardLibraryMode(Enum):
    """C/C++ Standard Library delivery mode."""
    NONE = auto()
    """Disable standard library delivery."""
    PLATFORM = auto()
    """Library provided by the default compiler on your platform, if any are installed."""
    DEVANA_CLANG = auto()
    """Library shipped with Devan. Recommended choice for Linux platform."""
    CUSTOM = auto()
    """Use  custom std Library provided by path."""

    @classmethod
    def create_default(cls):
        """This feature is platform dependent, trying to return the best way to provide a standard library
        for a given machine.
        For macOS platform, you may need to provide libc path from your xcode or other sdk."""
        return cls.PLATFORM if platform.system() == 'Windows' else cls.DEVANA_CLANG


@dataclass
class StandardLibraryConfiguration(IValidateConfig):
    """Configuration of std usage."""
    mode: StandardLibraryMode = field(default_factory=lambda: StandardLibraryMode.create_default())
    """Delivery mode"""
    path: Optional[Path] = None
    """Path for custom standard library, if any."""

    def validate(self):
        if self.mode is StandardLibraryMode.CUSTOM and self.path is None:
            raise ValueError("For custom mode path is required.")
        if self.path is not None and not self.path.is_dir():
            raise ValueError("Path must be directory.")

    def get_compilation_flags(self) -> List[str]:
        if self.mode is StandardLibraryMode.PLATFORM:
            return []
        no_std_flags: List[str] = ["-nostdinc++"]
        if self.mode is StandardLibraryMode.CUSTOM:
            path = [f"-I{self.path}"] if self.path else []
            return no_std_flags + path
        if self.mode is StandardLibraryMode.DEVANA_CLANG:
            from devana import __path__ as root_path  # pylint: disable=import-outside-toplevel
            std_path = [f"-I{root_path[0]}/libcxx/include", f"-I{root_path[0]}/libcxx/internal"]
            return no_std_flags + std_path
        return []


@dataclass
class IncludesSet(IValidateConfig):
    """A set of directories containing header files. """
    directories: List[Path] = field(default_factory=lambda: [])

    def validate(self):
        for directory in self.directories:
            if not directory.is_dir() or not directory.exists():
                raise ValueError("Paths to existing directories are required.")

    def get_compilation_flags(self) -> List[str]:
        return [f"-I{d}" for d in self.directories]


@dataclass
class ParsingConfiguration(IValidateConfig):
    """Code parser configuration."""
    comments: CommentsParsing = field(default_factory=lambda: CommentsParsing())
    """Comments parsing settings."""
    language_version: LanguageStandard = field(default_factory=lambda: LanguageStandard.create_default())
    """C or C++ standard version."""
    error_strategy: ParsingErrorPolicy = field(default_factory=lambda: ParsingErrorPolicy.create_default())
    """Behavior when non-parsable elements are detected."""
    standard_library: StandardLibraryConfiguration = field(default_factory=lambda: StandardLibraryConfiguration())
    """How to provide the language standard library."""
    libraries: IncludesSet = field(default_factory=lambda: IncludesSet())
    """Library search directories. It can contain both normal paths to directories, header paths that will support
    parsing, and paths to the location of an external library that will not be parsed within the module."""
    compiler_commands: List[str] = field(default_factory=lambda: [])
    """Allows you to use any valid clang commands."""
    file_by_file_parsing: bool = False
    """If true, it does not load all files into memory and builds a full type lexicon for all given files.
    Instead, it parses files about one another, treating other files as external dependencies.
    This is a less powerful solution but more economical in terms of RAM. When working with larger projects,
    we recommend creating multiple modules used sequentially, containing a small slice of local context
    instead of this option."""

    def validate(self):
        self.comments.validate()
        self.standard_library.validate()
        self.libraries.validate()

    def parsing_options(self) -> List[str]:
        includes = self.libraries.get_compilation_flags()
        std_library = self.standard_library.get_compilation_flags()
        language = self.language_version.value.options
        other_commands = self.compiler_commands
        return language + includes + std_library + other_commands


@dataclass
class Configuration(IValidateConfig):
    """Main configuration."""
    parsing: ParsingConfiguration = field(default_factory=lambda: ParsingConfiguration())
    """Configuring the parsing of C ++ files, this is how the C ++ code will be transformed
    into the appropriate python classes instances."""
    logger: logging = field(default_factory=lambda: Configuration._create_default_logger())
    """Currently used standard logger instance."""

    def validate(self):
        self.parsing.validate()

    @staticmethod
    def get_configuration(this: Any):
        while True:
            if hasattr(this, "configuration"):
                return this.configuration
            if not hasattr(this, "parent"):
                return Configuration()
            this = this.parent

    @staticmethod
    def _create_default_logger():
        logger = logging.getLogger("devana")
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.WARNING)
        return logger
