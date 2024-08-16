import unittest
import os
from devana.syntax_abstraction.organizers.sourcefile import SourceFile
from devana.preprocessing.components.extractors.commentextractor import CommentExtractor


class TestCommentExtractor(unittest.TestCase):

    def setUp(self):
        self.source_file = SourceFile(os.path.dirname(__file__) + r"/source_files/comments.hpp")

    def test_extract_all(self):
        extractor = CommentExtractor()
        result = extractor.generate([self.source_file])
        self.assertEqual(len(result), 6)
