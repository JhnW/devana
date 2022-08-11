from enum import Enum, auto
from dataclasses import dataclass, field
import logging
from abc import ABC, abstractmethod
from typing import List


class IValidateConfig(ABC):
    """Every sub-config should implement this interface to provide cohesion and implementation check."""

    @abstractmethod
    def validate(self):
        """This method do not return value. Each problem should be reported as an appropriate exception.
        This exception will be propagated to the client using the library."""
        pass


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
        def __init__(self, options: List[str], value):
            self._value = value
            self._options = options

        @property
        def _compiler_option(self) -> List[str]:
            """Compiler option, for internal usage"""
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
    IGNORE = auto()
    """Ignore all errors."""
    LOG = auto()
    """Only log error."""
    ABORT = auto()
    """Throw exception."""

    @classmethod
    def create_default(cls):
        return cls.IGNORE


@dataclass
class ParsingConfiguration(IValidateConfig):
    comments: CommentsParsing = field(default_factory=lambda: CommentsParsing())
    """Comments parsing settings."""
    language_version: LanguageStandard = field(default_factory=lambda: LanguageStandard.create_default())
    """C or C++ standard version."""
    error_strategy: ParsingErrorPolicy = field(default_factory=lambda: ParsingErrorPolicy.create_default())
    """Behavior when non-parsable elements are detected."""

    def validate(self):
        self.comments.validate()


@dataclass
class Configuration(IValidateConfig):
    parsing: ParsingConfiguration = field(default_factory=lambda: ParsingConfiguration())
    """Configuring the parsing of C ++ files, this is how the C ++ code will be transformed 
    into the appropriate python classes instances."""
    logger: logging = field(default_factory=lambda: Configuration._create_default_logger())
    """Currently used standard logger instance."""

    def validate(self):
        self.parsing.validate()

    @staticmethod
    def get_configuration(this: any):
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
