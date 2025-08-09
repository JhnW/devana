import unittest
import os

from typing import Optional
from devana.preprocessing.premade.components.flow.dataprovider import SyntaxElementDataProvider
from devana.preprocessing.premade.components.executor.environment import Environment, CallFrame
from devana.preprocessing.premade.components.parser.parser import Signature
from devana.syntax_abstraction.organizers.sourcemodule import SourceModule
from devana.syntax_abstraction.syntax import ISyntaxElement


def data_factory(element: ISyntaxElement) -> Optional[Environment.CallingData]:
    name: Optional[str] = getattr(element, "name", None)
    if name and name.startswith("p_"):
        return Environment.CallingData(
            arguments=CallFrame.Arguments(positional=[], named={}),
            target=element,
            signature=Signature(name="Parsable")
        )


class TestSyntaxElementDataProvider(unittest.TestCase):

    def setUp(self):
        self._module = SourceModule("Elements", os.path.dirname(__file__) + r"/source_files/elements")

    def test_syntax_element_data_provider_with_deep_search(self):
        provider = SyntaxElementDataProvider([self._module], [data_factory])
        result = provider.feed()
        self.assertEqual(len(result), 3)

        for data in result:
            self.assertTrue(isinstance(data, Environment.CallingData))
            self.assertEqual(len(data.arguments.positional), 0)
            self.assertEqual(len(data.arguments.named), 0)
            self.assertEqual(data.signature.name, "Parsable")
            self.assertEqual(data.signature.namespaces, [])

    def test_syntax_element_data_provider_without_deep_search(self):
        provider = SyntaxElementDataProvider([self._module], [data_factory], deep_search=False)
        result = provider.feed()
        self.assertEqual(len(result), 2)

        for data in result:
            self.assertTrue(isinstance(data, Environment.CallingData))
            self.assertEqual(len(data.arguments.positional), 0)
            self.assertEqual(len(data.arguments.named), 0)
            self.assertEqual(data.signature.name, "Parsable")
            self.assertEqual(data.signature.namespaces, [])
