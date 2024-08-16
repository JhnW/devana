from typing import Type, Iterable, Optional
from devana.preprocessing.components.property.parsers.types import *
from devana.preprocessing.components.property.parsers.descriptions import IDescribedProperty, IDescribedType
from devana.preprocessing.preprocessor import IGenerator
from devana.syntax_abstraction.attribute import Attribute
from devana.preprocessing.components.property.parsers.result import Result
from devana.preprocessing.components.property.parsers.configuration import Configuration


class AttributeParser(IGenerator):
    """Parser implementation using C++ standard attributes."""

    def __init__(self, properties: Optional[List[IDescribedProperty]] = None,
                 configuration: Optional[Configuration] = None):
        self._properties = properties if properties is not None else []
        self._configuration = configuration if configuration else Configuration(ignore_unknown=True)
        if self._configuration.ignore_unknown is False:
            raise ValueError("The attribute parser does not allow a restrictive approach to unknown attributes due to "
                             "the existence of attributes that are compiler extensions.")
        for p in self._properties:
            self._validate_property(p)

    def add_property(self, prop: IDescribedProperty):
        self._validate_property(prop)
        self._properties.append(prop)

    @classmethod
    def get_required_type(cls) -> Type:
        return Attribute

    @classmethod
    def get_produced_type(cls) -> Type:
        return Result

    def generate(self, data: Iterable[Attribute]) -> Iterable[Result]:
        return []

    @staticmethod
    def _validate_property(prop: IDescribedProperty):
        """Check if property is able to usage."""
        if not prop.namespace:
            raise ValueError("Due to the existence of compiler extension attributes and standard standard "
                             "attributes, it is required that preprocessor attributes use namespace.")
