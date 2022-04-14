from enum import Enum, auto
from dataclasses import dataclass, field
import logging
from abc import ABC, abstractmethod


class ConservativeLevel(Enum):
    HIGH = auto()
    MEDIUM = auto()
    LOW = auto()


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


@dataclass
class ParsingConfiguration(IValidateConfig):
    comments: CommentsParsing = field(default_factory=lambda: CommentsParsing())
    """Comments parsing settings."""

    def validate(self):
        self.comments.validate()


@dataclass
class Configuration(IValidateConfig):
    parsing: ParsingConfiguration = field(default_factory=lambda: ParsingConfiguration())
    """Configuring the parsing of C ++ files, this is how the C ++ code will be transformed 
    into the appropriate python classes instances."""
    conservative_level: ConservativeLevel = ConservativeLevel.MEDIUM
    """Currently not used. May be removed / moved elsewhere in future revisions without warning."""
    logger = logging
    """Currently not used. May be removed / moved elsewhere in future revisions without warning."""

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
