from enum import Enum, auto
from dataclasses import dataclass
import logging


class ConservativeLevel(Enum):
    HIGH = auto(),
    MEDIUM = auto()
    LOW = auto()


@dataclass
class Configuration:
    conservative_level: ConservativeLevel = ConservativeLevel.MEDIUM
    logger = logging



