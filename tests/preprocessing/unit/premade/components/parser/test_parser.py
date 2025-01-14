import unittest
from typing import List
from enum import Enum, auto
from devana.preprocessing.premade.components.parser.parser import Parser, Signature
from devana.preprocessing.premade.components.parser.extractor import IExtractor, ExtractedFunction
from devana.syntax_abstraction.externc import ExternC


class TestParser(unittest.TestCase):

    class ExtractorForTestsAll(IExtractor):
        def extract(self) -> List[ExtractedFunction]:
            return [ExtractedFunction('text_namespace::foo("text", 7, true)', ExternC())]

    class ExtractorForTestsEnum(IExtractor):
        def extract(self) -> List[ExtractedFunction]:
            return [ExtractedFunction('foo(TEST_VALUE_2)', ExternC())]

    def test_parser(self):
        parser = Parser(self.ExtractorForTestsAll(), [Signature("foo", ["text_namespace"],
                                                             Signature.Arguments([str, int, bool]))])
        result = parser.feed()
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].signature.name, 'foo')
        self.assertEqual(result[0].signature.namespaces, ['text_namespace'])
        self.assertEqual(len(result[0].arguments.positional), 3)
        self.assertEqual(result[0].arguments.positional[0].content, "text")
        self.assertEqual(result[0].arguments.positional[1].content, 7)
        self.assertEqual(result[0].arguments.positional[2].content, True)

    def test_parsing_with_enum(self):

        class TestEnum(Enum):
            TEST_VALUE_1 = auto()
            TEST_VALUE_2 = auto()
            TEST_VALUE_3 = auto()

        parser = Parser(self.ExtractorForTestsEnum(), [Signature("foo", [], Signature.Arguments([TestEnum]))])
        result = parser.feed()
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].signature.name, 'foo')
        self.assertEqual(result[0].signature.namespaces, [])
        self.assertEqual(len(result[0].arguments.positional), 1)
        self.assertEqual(result[0].arguments.positional[0].content, TestEnum.TEST_VALUE_2)
