import unittest
import sys
from devana.syntax_abstraction.organizers.sourcemodule import SourceModule, ModuleFilter


class TestSourceModule(unittest.TestCase):

    def setUp(self):
        pass
        self.module_path = sys.path[0] + r"/source_files/multiple_files/module"

    def test_simple_creation(self):
        module = SourceModule("Test_1", self.module_path)
        self.assertEqual(len(module.files), 3)

    def test_filter_allowed(self):
        f = ModuleFilter()
        f.allowed_filter = [r"\.h", r"\.hpp"]
        module = SourceModule("Test_1", self.module_path, f)
        self.assertEqual(len(module.files), 2)

    def test_filter_forbidden(self):
        f = ModuleFilter()
        f.forbidden_filter= [r"\.h", r"\.hpp"]
        module = SourceModule("Test_1", self.module_path, f)
        self.assertEqual(len(module.files), 1)

