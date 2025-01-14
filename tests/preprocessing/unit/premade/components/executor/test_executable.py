from devana.preprocessing.premade.components.executor.executable import Executable, CallFrame, Signature
from devana.preprocessing.premade.components.savers.filesaver import IDestiny
from devana.preprocessing.premade.components.executor.editor import IEditable
from pathlib import Path
import unittest
from typing import List, Any, Optional


class DestinyForTest(IDestiny):
    @property
    def name(self) -> str:
        return "test_name"

    @property
    def content(self) -> str:
        return "test_content"

    @property
    def path_prefix(self) -> Optional[Path]:
        return None


class ListEditor(IEditable):

    def __init__(self):
        self._editor = []

    @property
    def editable(self) -> Any:
        return self._editor

    @property
    def destiny(self) -> IDestiny:
        return DestinyForTest()


class ContextForTests(CallFrame.IContext):

    def __init__(self):
        self._editor = ListEditor()
        self._state = True

    @property
    def editors(self):
        return [self._editor]

    def get_editor(self, name: str) -> Any:
        return self._editor

    def get_state(self, name: str) -> Any:
        return self._state

class TestExecutorRun(unittest.TestCase):

    @staticmethod
    def function_no_args(ctx: CallFrame.IContext, target: None):
        l: List = ctx.get_editor("").editable
        l.append(1)
        l.append(2)

    def test_no_arguments_executor(self):
        executable = Executable[None](Signature("test_call"), Executable.TargetScope(), self.function_no_args)
        context = ContextForTests()
        frame = CallFrame[None](CallFrame.Arguments(), None, context)
        executable.call(frame)
        self.assertEqual(2, len(context.get_editor("").editable))
        self.assertEqual(1, context.get_editor("").editable[0])
        self.assertEqual(2, context.get_editor("").editable[1])

    def test_not_enough_positional_arguments(self):
        signature = Signature("test_call")
        signature.arguments.positional = [int, str, int]
        signature.arguments.named = {"a": str, "b": int, "c": str}

        executable = Executable[None](signature, Executable.TargetScope(), self.function_no_args)
        context = ContextForTests()
        frame_arguments = CallFrame.Arguments()
        frame_arguments.positional = [CallFrame.Arguments.Value(7), CallFrame.Arguments.Value("test")]
        frame = CallFrame[None](frame_arguments, None, context)
        self.assertRaises(ValueError, executable.call, frame)

    def test_too_many_positional_arguments(self):
        signature = Signature("test_call")
        signature.arguments.positional = [int, int]
        signature.arguments.named = {"a": str }

        executable = Executable[None](signature, Executable.TargetScope(), self.function_no_args)
        context = ContextForTests()
        frame_arguments = CallFrame.Arguments()
        frame_arguments.positional = [CallFrame.Arguments.Value(7), CallFrame.Arguments.Value("test"),
                                      CallFrame.Arguments.Value("test"), CallFrame.Arguments.Value("test")]
        frame = CallFrame[None](frame_arguments, None, context)
        self.assertRaises(ValueError, executable.call, frame)

    def test_wrong_type_of_positional_arguments(self):
        signature = Signature("test_call")
        signature.arguments.positional = [int, int]
        signature.arguments.named = {"a": str }

        executable = Executable[None](signature, Executable.TargetScope(), self.function_no_args)
        context = ContextForTests()
        frame_arguments = CallFrame.Arguments()
        frame_arguments.positional = [CallFrame.Arguments.Value(7), CallFrame.Arguments.Value("test")]
        frame = CallFrame[None](frame_arguments, None, context)
        #executable.call(frame)
        self.assertRaises(ValueError, executable.call, frame)

    def test_wrong_type_of_named_arguments(self):
        signature = Signature("test_call")
        signature.arguments.positional = [int, int]
        signature.arguments.named = {"a": str }

        executable = Executable[None](signature, Executable.TargetScope(), self.function_no_args)
        context = ContextForTests()
        frame_arguments = CallFrame.Arguments()
        frame_arguments.positional = [CallFrame.Arguments.Value(7), CallFrame.Arguments.Value(8)]
        frame_arguments.named = {"a": CallFrame.Arguments.Value(8) }
        frame = CallFrame[None](frame_arguments, None, context)
        self.assertRaises(ValueError, executable.call, frame)

    def test_wrong_name_of_named_arguments(self):
        signature = Signature("test_call")
        signature.arguments.positional = [int, int]
        signature.arguments.named = {"a": str }

        executable = Executable[None](signature, Executable.TargetScope(), self.function_no_args)
        context = ContextForTests()
        frame_arguments = CallFrame.Arguments()
        frame_arguments.positional = [CallFrame.Arguments.Value(7), CallFrame.Arguments.Value(8)]
        frame_arguments.named = {"b": CallFrame.Arguments.Value("test_value") }
        frame = CallFrame[None](frame_arguments, None, context)
        self.assertRaises(ValueError, executable.call, frame)


class TestExecutorConstructors(unittest.TestCase):


    def test_create_no_args_signature_from_function(self):

        def function_1(target: str, context: str, a: str, b: str):
            pass

        signature = Signature.from_function(function_1)
        self.assertEqual("function_1", signature.name)
        self.assertEqual([], signature.namespaces)
        self.assertEqual([str, str], signature.arguments.positional)
        self.assertEqual({}, signature.arguments.named)

    def test_create_with_named_args_signature_from_function(self):

        def function_1(target: str, context: str, a: Optional[List[int]] = None):
            pass

        signature = Signature.from_function(function_1)
        self.assertEqual("function_1", signature.name)
        self.assertEqual([], signature.namespaces)
        self.assertEqual([], signature.arguments.positional)
        self.assertEqual({"a": Optional[List[int]]}, signature.arguments.named)
