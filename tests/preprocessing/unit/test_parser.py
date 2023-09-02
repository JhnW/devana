import unittest
from enum import Enum, auto
from typing import Optional
from devana.preprocessing.generators.syntax import DataSignature, TypeKind, PreprocessorAttribute, AttributeSyntaxError
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

    class TestSource(ISource):

        @property
        def invoker(self):
            return None

        @property
        def target(self):
            return None

        @property
        def code(self):
            return None

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

    def test_parse_and_invoke_attribute_integer(self):

        def test_fnc(source: ISource, num: int) -> bool:
            return num > 5

        signature = DataSignature.from_callable(test_fnc)
        attr = PreprocessorAttribute(signature)
        call_result = attr.invoke(self.TestSource(), "test_fnc(7)", True)
        self.assertTrue(call_result)
        call_result = attr.invoke(self.TestSource(), "test_fnc( -6)", True)
        self.assertFalse(call_result)

    def test_parse_and_invoke_attribute_float(self):

        def test_fnc(source: ISource, num: float) -> bool:
            return num == 7.8

        signature = DataSignature.from_callable(test_fnc)
        attr = PreprocessorAttribute(signature)
        call_result = attr.invoke(self.TestSource(), "test_fnc(7.8)", True)
        self.assertTrue(call_result)
        call_result = attr.invoke(self.TestSource(), "test_fnc( -6)", True)
        self.assertFalse(call_result)

    def test_parse_and_invoke_attribute_string(self):

        def test_fnc(source: ISource, value: str) -> bool:
            return value == "test_str"

        signature = DataSignature.from_callable(test_fnc)
        attr = PreprocessorAttribute(signature)
        call_result = attr.invoke(self.TestSource(), 'test_fnc("test_str")', True)
        self.assertTrue(call_result)
        call_result = attr.invoke(self.TestSource(), 'test_fnc("no_test_str")', True)
        self.assertFalse(call_result)

    def test_parse_and_invoke_attribute_bool(self):

        def test_fnc(source: ISource, value: bool) -> bool:
            return value

        signature = DataSignature.from_callable(test_fnc)
        attr = PreprocessorAttribute(signature)
        call_result = attr.invoke(self.TestSource(), 'test_fnc(True)', True)
        self.assertTrue(call_result)
        call_result = attr.invoke(self.TestSource(), 'test_fnc(False)', True)
        self.assertFalse(call_result)

    def test_parse_and_invoke_attribute_optional(self):

        def test_fnc(source: ISource, value: Optional[bool]) -> int:
            if value is None:
                return 8
            return 7 if value else 10

        signature = DataSignature.from_callable(test_fnc)
        attr = PreprocessorAttribute(signature)
        call_result = attr.invoke(self.TestSource(), 'test_fnc(None)', True)
        self.assertEqual(call_result, 8)
        call_result = attr.invoke(self.TestSource(), 'test_fnc(True)', True)
        self.assertEqual(call_result, 7)
        call_result = attr.invoke(self.TestSource(), 'test_fnc(False)', True)
        self.assertEqual(call_result, 10)

    def test_parse_and_invoke_attribute_enum(self):

        class TestEnum(Enum):
            VAL_1 = auto()
            VAL_2 = auto()

        def test_fnc(source: ISource, value: TestEnum) -> bool:
            if value is TestEnum.VAL_1:
                return True
            return False

        signature = DataSignature.from_callable(test_fnc)
        attr = PreprocessorAttribute(signature)
        call_result = attr.invoke(self.TestSource(), 'test_fnc(VAL_1)', True)
        self.assertTrue(call_result)
        call_result = attr.invoke(self.TestSource(), 'test_fnc(VAL_2)', True)
        self.assertFalse(call_result)

    def test_parse_and_invoke_attribute_enum_wrong_value(self):
        class TestEnum(Enum):
            VAL_1 = auto()
            VAL_2 = auto()

        def test_fnc(source: ISource, value: TestEnum) -> bool:
            if value is TestEnum.VAL_1:
                return True
            return False

        signature = DataSignature.from_callable(test_fnc)
        attr = PreprocessorAttribute(signature)
        with self.assertRaises(AttributeSyntaxError):
            attr.invoke(self.TestSource(), 'test_fnc(VAL_3)', True)

    def test_parse_and_invoke_attribute_bool_wrong_value(self):

        def test_fnc(source: ISource, test: bool) -> bool:
            return test

        signature = DataSignature.from_callable(test_fnc)
        attr = PreprocessorAttribute(signature)
        with self.assertRaises(AttributeSyntaxError):
            attr.invoke(self.TestSource(), 'test_fnc(T)', True)

    def test_parse_and_invoke_attribute_int_to_float(self):

        def test_fnc(source: ISource, test: float) -> bool:
            return test > 12.0

        signature = DataSignature.from_callable(test_fnc)
        attr = PreprocessorAttribute(signature)
        call_result = attr.invoke(self.TestSource(), 'test_fnc(15)', True)
        self.assertTrue(call_result)

    def test_parse_and_invoke_attribute_int_to_float(self):

        def test_fnc(source: ISource, test: float) -> bool:
            return test > 12.0

        signature = DataSignature.from_callable(test_fnc)
        attr = PreprocessorAttribute(signature)
        call_result = attr.invoke(self.TestSource(), 'test_fnc(15)', True)
        self.assertTrue(call_result)

    def test_parse_and_invoke_attribute_str_comma(self):

        def test_fnc(source: ISource, test: str) -> bool:
            return test == "test, test,t6"

        signature = DataSignature.from_callable(test_fnc)
        attr = PreprocessorAttribute(signature)
        call_result = attr.invoke(self.TestSource(), 'test_fnc("test, test,t6")', True)
        self.assertTrue(call_result)

    def test_parse_and_invoke_attribute_str_comma(self):

        def test_fnc(source: ISource, test: str) -> bool:
            return test == "test, test,t6"

        signature = DataSignature.from_callable(test_fnc)
        attr = PreprocessorAttribute(signature)
        call_result = attr.invoke(self.TestSource(), 'test_fnc("test, test,t6")', True)
        self.assertTrue(call_result)

    def test_parse_and_invoke_attribute_multiple_arguments(self):

        def test_fnc(source: ISource, arg_1: str, arg_2: bool, arg_3: str, arg_4: bool) -> bool:
            return arg_1 == "1,2" and arg_2 and arg_3 == "True" and not arg_4

        signature = DataSignature.from_callable(test_fnc)
        attr = PreprocessorAttribute(signature)
        call_result = attr.invoke(self.TestSource(), 'test_fnc("1,2", True , "True",False)', True)
        self.assertTrue(call_result)

    def test_parse_and_invoke_attribute_multiple_arguments_default(self):

        def test_fnc(source: ISource, arg_1: bool, arg_2: bool = True) -> bool:
            return arg_2

        signature = DataSignature.from_callable(test_fnc)
        attr = PreprocessorAttribute(signature)
        call_result = attr.invoke(self.TestSource(), 'test_fnc(True)', True)
        self.assertTrue(call_result)
        call_result = attr.invoke(self.TestSource(), 'test_fnc(True, False)', True)
        self.assertFalse(call_result)

    def test_parse_attribute_from_devana_namespace(self):

        def test_fnc(source: ISource) -> bool:
            return True

        signature = DataSignature.from_callable(test_fnc, is_marker=False)
        attr = PreprocessorAttribute(signature)
        call_result = attr.invoke(self.TestSource(), 'devana::test_fnc()', False)
        self.assertTrue(call_result)

    def test_parse_attribute_from_two_namespace(self):

        def test_fnc(source: ISource) -> bool:
            return True

        signature = DataSignature.from_callable(test_fnc, namespace="test", is_marker=False)
        attr = PreprocessorAttribute(signature)
        call_result = attr.invoke(self.TestSource(), 'devana::test::test_fnc()', False)
        self.assertTrue(call_result)

    def test_parse_attribute_from_wrong_namespace(self):

        def test_fnc(source: ISource) -> bool:
            return True

        signature = DataSignature.from_callable(test_fnc, namespace="test", is_marker=False)
        attr = PreprocessorAttribute(signature)
        with self.assertRaises(Exception):
            attr.invoke(self.TestSource(), 'test2::test_fnc(True)', False)
