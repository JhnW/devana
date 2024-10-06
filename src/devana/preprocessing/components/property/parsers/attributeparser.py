from typing import Iterable, Optional, Dict, Any
from itertools import count
from devana.preprocessing.components.property.parsers.types import *
from devana.preprocessing.components.property.parsers.descriptions import IDescribedProperty
from devana.preprocessing.preprocessor import IGenerator
from devana.syntax_abstraction.attribute import Attribute
from devana.preprocessing.components.property.parsers.result import Result, Arguments, Value, PropertySignature
from devana.preprocessing.components.property.parsers.configuration import Configuration
from devana.preprocessing.components.property.parsers.parser import ParsingBackend
from devana.preprocessing.components.property.parsers.types import parsable_element_from_described_type


class AttributeParser(IGenerator):
    """Parser implementation using C++ standard attributes."""

    def __init__(self, properties: Optional[List[IDescribedProperty]] = None,
                 configuration: Optional[Configuration] = None):
        self._properties = properties if properties is not None else []
        self._configuration = configuration if configuration else Configuration(ignore_unknown=True)
        self._backend = ParsingBackend()
        if self._configuration.ignore_unknown is False:
            raise ValueError("The attribute parser does not allow a restrictive approach to unknown attributes due to "
                             "the existence of attributes that are compiler extensions.")
        for prop in self._properties:
            self._validate_property(prop)
            self._add_types(prop)


    def add_property(self, prop: IDescribedProperty):
        self._validate_property(prop)
        self._properties.append(prop)
        self._add_types(prop)

    @classmethod
    def get_required_type(cls) -> Type:
        return Attribute

    @classmethod
    def get_produced_type(cls) -> Type:
        return Result

    def generate(self, data: Iterable[Attribute]) -> Iterable[Result]:
        for attr in data:

            def maybe_proto_gen(in_attr):
                maybe_prop_result = filter(lambda e: e.namespace == in_attr.namespace, self._properties)
                maybe_prop_result = list(filter(lambda e: e.name == in_attr.name, maybe_prop_result))
                return maybe_prop_result

            maybe_prop = maybe_proto_gen(attr)
            if len(maybe_prop) == 0:
                raise ValueError(f"Unknown property: {attr.name}  in namespace: {attr.namespace}")
            prop: IDescribedProperty = maybe_prop[0]
            # matching property find as prop, so lets parse arguments
            parsed_arguments = []
            if attr.arguments is not None:
                parsed_arguments = [self._backend.parse_argument(a) for a in attr.arguments]

            # check if positional arguments are not mixed with named ones
            is_positional_finished = False
            for a in parsed_arguments:
                if a.name is None and is_positional_finished:
                    raise ValueError(f"Mixed positional arguments and named is not allowed. Error in {prop.name}")
                if a.name is not None:
                    is_positional_finished = True

            result_args = Arguments()

            result_positional_arguments = []
            result_named_arguments: Dict[str, Any] = {}

            # now try a match parsing result to expected arguments

            for i, a in zip(count(), parsed_arguments):
                if a.name is None:
                    result_positional_arguments.append(a)
                else:
                    if a.name in result_named_arguments:
                        raise ValueError(f"Duplicated argument name {a.name} while parsing property {prop.name}.")
                    result_named_arguments[a.name] = a

            # now we need to do the main validation - connect the paired parameters with the expected arguments
            for i, a in zip(count(), result_positional_arguments):
                if i >= len(prop.arguments):
                    raise ValueError("Too many arguments.")
                expected_type = prop.arguments[i].type
                given_type = a.type
                if expected_type.name != given_type.name: # types have unique names
                    raise ValueError(f"Expected type {expected_type} but got {given_type}")
                result_args.positional.append(Value(a.value))

            for key in result_named_arguments:

                def expected_types_gen(expected_name: str, props: IDescribedProperty):
                    return list(filter(lambda e: e.name == expected_name, props.arguments))

                expected_type_list = expected_types_gen(key, prop)
                if len(expected_type_list) == 0:
                    raise ValueError(f"Unknown argument named {key} in {prop.name}")
                expected_type = expected_type_list[0].type
                given_type = result_named_arguments[key].type
                if expected_type.name != given_type.name: # types have unique names
                    raise ValueError(f"Expected type {expected_type} but got {given_type}")
                result_args.named[key] = Value(result_named_arguments[key].value)

            # now make a list of the remaining arguments based on the property description
            remaining_expected_args = prop.arguments.copy()
            del remaining_expected_args[: len(result_args.positional)]

            for key in result_args.named:
                def elements_gen(key_name: str, expected):
                    return list(filter(lambda e: e.name == key_name, expected))

                elements = elements_gen(key, remaining_expected_args)
                if len(elements) == 0:
                    raise ValueError(f"Unknown argument named {key} in {prop.name}")
                if len(elements) > 1:
                    raise ValueError(f"Multiple argument named {key} in {prop.name}")
                element = elements[0]
                remaining_expected_args.remove(element)

            # the parser does not provide default parameter values (because it is not its job)
            # but we need to check if the function signature is satisfied - that is,
            # if all parameters that do not
            # have default values have been provided
            if list(filter(lambda e: e.default_value is None, remaining_expected_args)):
                raise ValueError(f"Not all parameters were provided for: {prop.name}")

            signature = PropertySignature(
                name = prop.name,
                namespaces = [prop.namespace] if prop.namespace else [],
                arguments = [self._backend.types[n].result_type for n in [e.type.name for e in prop.arguments]]
            )

            yield Result(
                property = signature,
                arguments= result_args,
                target=attr.parent
            )


    @staticmethod
    def _validate_property(prop: IDescribedProperty):
        """Check if property is able to usage."""
        if not prop.namespace:
            raise ValueError("Due to the existence of compiler extension attributes and standard standard "
                             "attributes, it is required that preprocessor attributes use namespace.")
        # check duplicates
        for a1 in prop.arguments:
            for a2 in prop.arguments:
                if a1 != a2:
                    if (a1.name is not None or a2.name is not None) and a1.name == a2.name:
                        raise ValueError(f"Duplicated property name for property: {prop.name}")

    def _add_types(self, desc: IDescribedProperty):
        """Add types to parser from IDescribedProperty."""
        for arg in desc.arguments:
            self._backend.add_type(parsable_element_from_described_type(arg.type))
