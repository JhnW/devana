import unittest
import os
from devana.preprocessing.premade.components.parser.extractor import CommentExtractor
from devana.syntax_abstraction.organizers.sourcemodule import SourceModule


class TestCommentExtractor(unittest.TestCase):

    def setUp(self):
        self._module = SourceModule("Text module", os.path.dirname(__file__) + r"/source_files/comments")

    def test_extract_one(self):
        extractor = CommentExtractor([self._module])
        result = extractor.extract()
        self.assertEqual(7, len(result))
        self.assertEqual(" Test comment 1.", result[0].text)
        self.assertEqual("Test comment 2.", result[1].text)
        self.assertEqual(" Test comment 3.", result[2].text)
        self.assertEqual("Test comment 4.", result[3].text)
        self.assertEqual("Bla bla bla.", result[4].text)
        self.assertEqual(" Test comment 5.", result[5].text)
        self.assertEqual(" Test comment 6.", result[6].text)
        self.assertEqual(list(self._module.files)[0].content[0], result[0].parent)

    def test_extract_filter(self):
        extractor = CommentExtractor([self._module], lambda _: False)
        result = extractor.extract()
        self.assertEqual(0, len(result))
