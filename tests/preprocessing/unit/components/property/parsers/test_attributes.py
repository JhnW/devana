import unittest
from dataclasses import dataclass
import dataclasses
from typing import Optional, List, Any
from devana.preprocessing.components.property.parsers.attributeparser import AttributeParser
from devana.preprocessing.components.property.parsers.descriptions import (
    IDescribedProperty, IDescribedArgument, IDescribedType, IDescribedValue)
from devana.preprocessing.components.property.parsers.types import FloatType, StringType
from devana.syntax_abstraction.attribute import Attribute


@dataclass
class TestDescribedProperty(IDescribedProperty):
    namespace: Optional[str] = dataclasses.MISSING
    name: str = dataclasses.MISSING
    arguments: List[IDescribedArgument] = dataclasses.MISSING


@dataclass
class TestDescribedType(IDescribedType):
    name: str = dataclasses.MISSING


@dataclass
class TestDescribedValue(IDescribedValue):
    type: IDescribedType = dataclasses.MISSING
    content_as_string: str = dataclasses.MISSING
    content: Optional[Any] = dataclasses.MISSING


@dataclass
class TestDescribedArgument(IDescribedArgument):
    name: Optional[str] = dataclasses.MISSING
    type: IDescribedType = dataclasses.MISSING
    default_value: Optional[IDescribedValue] = dataclasses.MISSING


class TestAttributesParser(unittest.TestCase):

    def test_empty_attribute(self):
        attributes = [Attribute.from_text("devana::foo()")]
        properties = [TestDescribedProperty("devana", "foo", [])]
        parser = AttributeParser(properties)
        results = list(parser.generate(attributes))
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(len(result.arguments.positional), 0)
        self.assertEqual(len(result.arguments.named), 0)

    def test_attribute_string(self):
        attributes = [Attribute.from_text('devana::foo("Text 1")')]
        properties = [TestDescribedProperty("devana", "foo", [
            TestDescribedArgument(None, TestDescribedType("String"), None)
        ])]
        parser = AttributeParser(properties)
        results = list(parser.generate(attributes))
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(len(result.arguments.positional), 1)
        self.assertEqual(len(result.arguments.named), 0)
        arg = result.arguments.positional[0]
        self.assertEqual(arg.type, str)
        self.assertEqual(arg.content, "Text 1")

    def test_attribute_float(self):
        attributes = [Attribute.from_text('devana::foo(7.5)')]
        properties = [TestDescribedProperty("devana", "foo", [
            TestDescribedArgument(None, TestDescribedType("Float"), None)
        ])]
        parser = AttributeParser(properties)
        results = list(parser.generate(attributes))
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(len(result.arguments.positional), 1)
        self.assertEqual(len(result.arguments.named), 0)
        arg = result.arguments.positional[0]
        self.assertEqual(arg.type, float)
        self.assertEqual(arg.content, 7.5)

    def test_attribute_float_without_dot(self):
        attributes = [Attribute.from_text('devana::foo(7)')]
        properties = [TestDescribedProperty("devana", "foo", [
            TestDescribedArgument(None, TestDescribedType("Float"), None)
        ])]
        parser = AttributeParser(properties)
        results = list(parser.generate(attributes))
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(len(result.arguments.positional), 1)
        self.assertEqual(len(result.arguments.named), 0)
        arg = result.arguments.positional[0]
        self.assertEqual(arg.type, float)
        self.assertEqual(arg.content, 7)

    def test_attribute_named_string(self):
        attributes = [Attribute.from_text('devana::foo(arg1="Text 1")')]
        properties = [TestDescribedProperty("devana", "foo", [
            TestDescribedArgument("arg1", TestDescribedType("String"), None)
        ])]
        parser = AttributeParser(properties)
        results = list(parser.generate(attributes))
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(len(result.arguments.positional), 0)
        self.assertEqual(len(result.arguments.named), 1)
        arg = result.arguments.named["arg1"]
        self.assertEqual(arg.type, str)
        self.assertEqual(arg.content, "Text 1")

    def test_attribute_two_named_arguments_position_unmatch(self):
        attributes = [Attribute.from_text('devana::foo(arg2="Text 1", arg1=768)')]
        properties = [TestDescribedProperty("devana", "foo", [
            TestDescribedArgument("arg1", TestDescribedType("Float"), None),
            TestDescribedArgument("arg2", TestDescribedType("String"), None)
        ])]
        parser = AttributeParser(properties)
        results = list(parser.generate(attributes))
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(len(result.arguments.positional), 0)
        self.assertEqual(len(result.arguments.named), 2)
        arg = result.arguments.named["arg1"]
        self.assertEqual(arg.type, float)
        self.assertEqual(arg.content, 768)
        arg = result.arguments.named["arg2"]
        self.assertEqual(arg.type, str)
        self.assertEqual(arg.content, "Text 1")

    def test_attribute_two_one_positional_one_named(self):
        attributes = [Attribute.from_text('devana::foo("Text 1", arg1="Text 2")')]
        string_type = TestDescribedType("String")
        properties = [TestDescribedProperty("devana", "foo", [
            TestDescribedArgument(None, string_type, None),
            TestDescribedArgument("arg1", string_type, None)
        ])]
        parser = AttributeParser(properties)
        results = list(parser.generate(attributes))
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(len(result.arguments.positional), 1)
        self.assertEqual(len(result.arguments.named), 1)
        arg = result.arguments.positional[0]
        self.assertEqual(arg.type, str)
        self.assertEqual(arg.content, "Text 1")
        arg = result.arguments.named["arg1"]
        self.assertEqual(arg.type, str)
        self.assertEqual(arg.content, "Text 2")

    def test_attribute_positional_wrong_type(self):
        attributes = [Attribute.from_text('devana::foo(888, arg1=98)')]
        properties = [TestDescribedProperty("devana", "foo", [
            TestDescribedArgument(None, StringType(), None),
            TestDescribedArgument("arg1", FloatType(), None)
        ])]
        parser = AttributeParser(properties)
        with self.assertRaises(ValueError):
            list(parser.generate(attributes))

    def test_attribute_named_wrong_type(self):
        attributes = [Attribute.from_text('devana::foo(arg2=888, arg1=98)')]
        properties = [TestDescribedProperty("devana", "foo", [
            TestDescribedArgument("arg2", StringType(), None),
            TestDescribedArgument("arg1", FloatType(), None)
        ])]
        parser = AttributeParser(properties)
        with self.assertRaises(ValueError):
            list(parser.generate(attributes))

    def test_attribute_named_wrong_name(self):
        attributes = [Attribute.from_text('devana::foo(arg=888)')]
        properties = [TestDescribedProperty("devana", "foo", [
            TestDescribedArgument("arg1", FloatType(), None)
        ])]
        parser = AttributeParser(properties)
        with self.assertRaises(ValueError):
            list(parser.generate(attributes))

    def test_attribute_too_many_arguments(self):
        attributes = [Attribute.from_text('devana::foo(0.1, 0.2, 0.3, 0.4)')]
        float_type = TestDescribedType("Float")
        properties = [TestDescribedProperty("devana", "foo", [
            TestDescribedArgument(None, float_type, None),
            TestDescribedArgument(None, float_type, None),
        ])]
        parser = AttributeParser(properties)
        with self.assertRaises(ValueError):
            list(parser.generate(attributes))

    def test_attribute_duplicated_named_argument(self):
        attributes = [Attribute.from_text('devana::foo(arg=0.6, arg=5)')]
        float_type = TestDescribedType("Float")
        properties = [TestDescribedProperty("devana", "foo", [
            TestDescribedArgument("arg", float_type, None)
        ])]
        parser = AttributeParser(properties)
        with self.assertRaises(ValueError):
            list(parser.generate(attributes))

    def test_attribute_positional_default_values_used_declaration(self):
        attributes = [Attribute.from_text('devana::foo(0.8)')]
        float_type = TestDescribedType("Float")
        properties = [TestDescribedProperty("devana", "foo", [
            TestDescribedArgument(None, float_type, None),
            TestDescribedArgument(None, float_type, TestDescribedValue(float_type, "0.7", 0.7)),
        ])]
        AttributeParser(properties)


    def test_attribute_positional_default_values_parsed(self):
        attributes = [Attribute.from_text('devana::foo(0.8)')]
        float_type = TestDescribedType("Float")
        properties = [TestDescribedProperty("devana", "foo", [
            TestDescribedArgument(None, float_type, None),
            TestDescribedArgument(None, float_type, TestDescribedValue(float_type, "0.7", 0.7)),
        ])]
        parser = AttributeParser(properties)
        results = list(parser.generate(attributes))
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(len(result.arguments.positional), 1)
        self.assertEqual(len(result.arguments.named), 0)
        self.assertEqual(result.arguments.positional[0].content, 0.8)
