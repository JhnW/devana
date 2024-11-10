import unittest
from dataclasses import dataclass
import dataclasses
from  pathlib import Path
from typing import Optional
from unittest.mock import patch, mock_open
from devana.preprocessing.components.savers.file_saver import FileSaver, IDestiny


@dataclass
class TestDestiny(IDestiny):
    name: str = dataclasses.MISSING
    content: str = dataclasses.MISSING
    path_prefix: Optional[Path] = dataclasses.MISSING


class TestFileSaver(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open)
    def test_basic_file_saver(self, mock_open_file):
        saver = FileSaver(FileSaver.Configuration(Path("/test")))
        destiny = TestDestiny("TestFileName.cpp", "Content tested", None)
        result = saver.consume([destiny])
        mock_open_file.assert_called_with(Path("/test/TestFileName.cpp"), "tw", encoding="utf-8")
        self.assertEqual(len(result.files), 1)
        self.assertEqual(result.files[0].name, "TestFileName.cpp")

    @patch("builtins.open", new_callable=mock_open)
    def test_add_prefix_for_file_saver(self, mock_open_file):
        saver = FileSaver(FileSaver.Configuration(Path("/test")))
        destiny = TestDestiny("TestFileName.cpp", "Content tested", Path("test_prefix"))
        result = saver.consume([destiny])
        mock_open_file.assert_called_with(Path("/test/test_prefix/TestFileName.cpp"), "tw", encoding="utf-8")
        self.assertEqual(len(result.files), 1)
        self.assertEqual(result.files[0].name, "TestFileName.cpp")


    @patch("builtins.open", new_callable=mock_open)
    def test_add_dynamic_prefix_for_file_saver(self, mock_open_file):
        saver = FileSaver(FileSaver.Configuration(Path("/test"), lambda e: Path("dynamic_prefix")))
        destiny = TestDestiny("TestFileName.cpp", "Content tested", None)
        result = saver.consume([destiny])
        mock_open_file.assert_called_with(Path("/test/dynamic_prefix/TestFileName.cpp"), "tw", encoding="utf-8")
        self.assertEqual(len(result.files), 1)
        self.assertEqual(result.files[0].name, "TestFileName.cpp")

    @patch("builtins.open", new_callable=mock_open)
    def test_add_dynamic_ans_static_prefix_for_file_saver(self, mock_open_file):
        saver = FileSaver(FileSaver.Configuration(Path("/test"), lambda e: Path("dynamic_prefix")))
        destiny = TestDestiny("TestFileName.cpp", "Content tested", Path("test_prefix"))
        result = saver.consume([destiny])
        mock_open_file.assert_called_with(Path("/test/test_prefix/dynamic_prefix/TestFileName.cpp"), "tw", encoding="utf-8")
        self.assertEqual(len(result.files), 1)
        self.assertEqual(result.files[0].name, "TestFileName.cpp")
