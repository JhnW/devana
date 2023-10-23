import unittest
import os
from devana.syntax_abstraction.organizers.sourcefile import SourceFile
from devana.preprocessing.components.parser.attributeextractor import AttributeExtractor


class TestAttributeExtractor(unittest.TestCase):

    def setUp(self):
        self.source_file = SourceFile(os.path.dirname(__file__) + r"/source_files/attributes.hpp")

    def test_extract_all(self):
        extractor = AttributeExtractor()
        result = extractor.generate([self.source_file])
        self.assertEqual(len(result), 6)
