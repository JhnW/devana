# import unittest
# from dataclasses import dataclass, field
# import dataclasses
# from typing import Optional, List
# from devana.preprocessing.components.property.parsers.attributeparser import AttributeParser
# from devana.preprocessing.components.property.parsers.descriptions import IDescribedProperty, IDescribedArgument
# from devana.syntax_abstraction.attribute import Attribute
#
#
# @dataclass
# class DescribedProperty(IDescribedProperty):
#     namespace: Optional[str] = dataclasses.MISSING
#     name: str = dataclasses.MISSING
#     arguments: List[IDescribedArgument] = field(default=lambda: [])
#
# class TestAttributesParserPositional(unittest.TestCase):
#
#     def test_empty_attribute(self):
#         attributes = [Attribute.from_text("devana::foo()")]
#         properties = [DescribedProperty("devana", "foo")]
#         parser = AttributeParser(properties)
#         results = list(parser.generate(attributes))
#         # self.assertEqual(len(results), 1)
#         # result = results[0]
#         # self.assertEqual(len(result.arguments.positional), 0)
#         # self.assertEqual(len(result.arguments.named), 0)
