import unittest
from enum import Enum, auto
from typing import Optional
from devana.preprocessing.generators.syntax import DataSignature, TypeKind
from devana.preprocessing.sources.source import ISource


# noinspection DuplicatedCode,PyUnusedLocal
class TestParserFromFunctionSignature(unittest.TestCase):

    def test_signature_name_from_callable(self):

        def test_fnc(source: ISource):
            pass

        signature: DataSignature = DataSignature.from_callable(test_fnc)
        self.assertEqual(signature.name, "test_fnc")

    def test_signature_argument_string(self):

        def test_fnc(source: ISource, arg_1: str):
            pass

        signature: DataSignature = DataSignature.from_callable(test_fnc)
        self.assertEqual(signature.name, "test_fnc")
        self.assertEqual(len(signature.arguments), 1)
        self.assertEqual(signature.arguments[0].name, "arg_1")
        self.assertEqual(signature.arguments[0].type.kind, TypeKind.STRING)
        self.assertFalse(signature.arguments[0].has_default)

    def test_signature_argument_bool(self):

        def test_fnc(source: ISource, arg_1: bool):
            pass

        signature: DataSignature = DataSignature.from_callable(test_fnc)
        self.assertEqual(signature.name, "test_fnc")
        self.assertEqual(len(signature.arguments), 1)
        self.assertEqual(signature.arguments[0].name, "arg_1")
        self.assertEqual(signature.arguments[0].type.kind, TypeKind.BOOL)
        self.assertFalse(signature.arguments[0].has_default)

    def test_signature_argument_number(self):

        with self.subTest("int"):
            def test_fnc(source: ISource, arg_1: int):
                pass
            signature: DataSignature = DataSignature.from_callable(test_fnc)
            self.assertEqual(signature.name, "test_fnc")
            self.assertEqual(len(signature.arguments), 1)
            self.assertEqual(signature.arguments[0].name, "arg_1")
            self.assertEqual(signature.arguments[0].type.kind, TypeKind.INT)
            self.assertFalse(signature.arguments[0].has_default)

        with self.subTest("float"):
            def test_fnc(source: ISource, arg_1: float):
                pass
            signature: DataSignature = DataSignature.from_callable(test_fnc)
            self.assertEqual(signature.name, "test_fnc")
            self.assertEqual(len(signature.arguments), 1)
            self.assertEqual(signature.arguments[0].name, "arg_1")
            self.assertEqual(signature.arguments[0].type.kind, TypeKind.REAL)
            self.assertFalse(signature.arguments[0].has_default)

    def test_signature_argument_enum(self):

        class TestEnum(Enum):
            VAL_1 = auto()
            VAL_2 = auto()

        def test_fnc(source: ISource, arg_1: TestEnum):
            pass

        signature: DataSignature = DataSignature.from_callable(test_fnc)
        self.assertEqual(signature.name, "test_fnc")
        self.assertEqual(len(signature.arguments), 1)
        self.assertEqual(signature.arguments[0].name, "arg_1")
        self.assertEqual(signature.arguments[0].type.kind, TypeKind.ENUM)
        self.assertEqual(signature.arguments[0].type.details, TestEnum)

    def test_signature_optional_argument(self):

        def test_fnc(source: ISource, arg_1: Optional[str]):
            pass

        signature: DataSignature = DataSignature.from_callable(test_fnc)
        self.assertEqual(signature.name, "test_fnc")
        self.assertEqual(len(signature.arguments), 1)
        self.assertEqual(signature.arguments[0].name, "arg_1")
        self.assertEqual(signature.arguments[0].type.kind, TypeKind.OPTIONAL)
        self.assertEqual(signature.arguments[0].type.details.kind, TypeKind.STRING)
        self.assertFalse(signature.arguments[0].has_default)

    def test_signature_default_value(self):

        def test_fnc(source: ISource, arg_1: str, arg_2: int = 7):
            pass

        signature: DataSignature = DataSignature.from_callable(test_fnc)
        self.assertEqual(signature.name, "test_fnc")
        self.assertEqual(len(signature.arguments), 2)
        self.assertEqual(signature.arguments[0].name, "arg_1")
        self.assertEqual(signature.arguments[1].name, "arg_2")
        self.assertFalse(signature.arguments[0].has_default)
        self.assertTrue(signature.arguments[1].has_default)
