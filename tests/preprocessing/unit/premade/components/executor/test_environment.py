import unittest
from typing import List
from devana.preprocessing.premade.components.executor.environment import Environment
from devana.preprocessing.premade.components.executor.executable import CallFrame, Signature, Executable


class TestEnvironmentRun(unittest.TestCase):


    class ContextTestTarget:
        pass

    class ContextTestTargetSub(ContextTestTarget):
        pass

    class ContextTestTargetNextSub(ContextTestTargetSub):
        pass

    def setUp(self):
        self.context = Environment.Context({"test_editor": []}, {"test_state": 7})

    def test_simple_run(self):

        def function_test(context: CallFrame.IContext, target: TestEnvironmentRun.ContextTestTarget):
            l: List = context.get_editor("test_editor")
            l.append(7)
        empty_executable = Executable(Signature.from_function(function_test),
                                                 Executable.TargetScope(TestEnvironmentRun.ContextTestTarget),
                                                 function_test)

        calling_data = Environment.CallingData(CallFrame.Arguments([], {}), TestEnvironmentRun.ContextTestTarget(),
                                               empty_executable.signature)
        environment = Environment([empty_executable], self.context, [calling_data])
        environment.call()
        self.assertEqual( 1, len(self.context.get_editor("test_editor")))
        self.assertEqual( 7, self.context.get_editor("test_editor")[0])

    def test_positional_args_run(self):

        def function_test(context: CallFrame.IContext, target: TestEnvironmentRun.ContextTestTarget, a: int):
            l: List = context.get_editor("test_editor")
            l.append(a)
        empty_executable = Executable(Signature.from_function(function_test),
                                                 Executable.TargetScope(TestEnvironmentRun.ContextTestTarget),
                                                 function_test)

        calling_data = Environment.CallingData(CallFrame.Arguments([CallFrame.Arguments.Value(12)], {}),
                                               TestEnvironmentRun.ContextTestTarget(),
                                               empty_executable.signature)
        environment = Environment([empty_executable], self.context, [calling_data])
        environment.call()
        self.assertEqual( 1, len(self.context.get_editor("test_editor")))
        self.assertEqual( 12, self.context.get_editor("test_editor")[0])


    def test_named_args_used_run(self):

        def function_test(context: CallFrame.IContext, target: TestEnvironmentRun.ContextTestTarget, a: int = 9):
            l: List = context.get_editor("test_editor")
            l.append(a)
        empty_executable = Executable(Signature.from_function(function_test),
                                                 Executable.TargetScope(TestEnvironmentRun.ContextTestTarget),
                                                 function_test)

        calling_data = Environment.CallingData(CallFrame.Arguments([], {"a": CallFrame.Arguments.Value(12)}),
                                               TestEnvironmentRun.ContextTestTarget(),
                                               empty_executable.signature)
        environment = Environment([empty_executable], self.context, [calling_data])
        environment.call()
        self.assertEqual(1, len(self.context.get_editor("test_editor")))
        self.assertEqual( 12, self.context.get_editor("test_editor")[0])


    def test_named_args_not_used_run(self):

        def function_test(context: CallFrame.IContext, target: TestEnvironmentRun.ContextTestTarget, a: int = 9):
            l: List = context.get_editor("test_editor")
            l.append(a)
        empty_executable = Executable(Signature.from_function(function_test),
                                                 Executable.TargetScope(TestEnvironmentRun.ContextTestTarget),
                                                 function_test)

        calling_data = Environment.CallingData(CallFrame.Arguments([], {}),
                                               TestEnvironmentRun.ContextTestTarget(),
                                               empty_executable.signature)
        environment = Environment([empty_executable], self.context, [calling_data])
        environment.call()
        self.assertEqual( 1, len(self.context.get_editor("test_editor")))
        self.assertEqual(9, self.context.get_editor("test_editor")[0])


    def test_namespace_run(self):

        def function_test(context: CallFrame.IContext, target: TestEnvironmentRun.ContextTestTarget):
            l: List = context.get_editor("test_editor")
            l.append(15)
        empty_executable = Executable(Signature.from_function(function_test, namespaces=["test"]),
                                                 Executable.TargetScope(TestEnvironmentRun.ContextTestTarget),
                                                 function_test)

        calling_data = Environment.CallingData(CallFrame.Arguments([], {}),
                                               TestEnvironmentRun.ContextTestTarget(),
                                               empty_executable.signature)
        environment = Environment([empty_executable], self.context, [calling_data])
        environment.call()
        self.assertEqual(1, len(self.context.get_editor("test_editor")))
        self.assertEqual(15, self.context.get_editor("test_editor")[0])

    def test_target_subclass_given_base_in_signature_run(self):

        def function_test(context: CallFrame.IContext, target: TestEnvironmentRun.ContextTestTarget):
            l: List = context.get_editor("test_editor")
            l.append(15)
        empty_executable = Executable(Signature.from_function(function_test),
                                                 Executable.TargetScope(TestEnvironmentRun.ContextTestTarget),
                                                 function_test)

        calling_data = Environment.CallingData(CallFrame.Arguments([], {}),
                                               TestEnvironmentRun.ContextTestTargetSub(),
                                               empty_executable.signature)
        environment = Environment([empty_executable], self.context, [calling_data])
        environment.call()
        self.assertEqual(1, len(self.context.get_editor("test_editor")))
        self.assertEqual(15, self.context.get_editor("test_editor")[0])

    def test_target_subclass_given_subclass_in_signature_run(self):

        def function_test(context: CallFrame.IContext, target: TestEnvironmentRun.ContextTestTarget):
            l: List = context.get_editor("test_editor")
            l.append(15)
        empty_executable = Executable(Signature.from_function(function_test),
                                                 Executable.TargetScope(TestEnvironmentRun.ContextTestTargetSub),
                                                 function_test)

        calling_data = Environment.CallingData(CallFrame.Arguments([], {}),
                                               TestEnvironmentRun.ContextTestTargetSub(),
                                               empty_executable.signature)
        environment = Environment([empty_executable], self.context, [calling_data])
        environment.call()
        self.assertEqual(1, len(self.context.get_editor("test_editor")))
        self.assertEqual(15, self.context.get_editor("test_editor")[0])


    def test_target_base_given_subclass_in_signature_run(self):

        def function_test(context: CallFrame.IContext, target: TestEnvironmentRun.ContextTestTarget):
            l: List = context.get_editor("test_editor")
            l.append(15)
        empty_executable = Executable(Signature.from_function(function_test),
                                                 Executable.TargetScope(TestEnvironmentRun.ContextTestTargetSub),
                                                 function_test)

        calling_data = Environment.CallingData(CallFrame.Arguments([], {}),
                                               TestEnvironmentRun.ContextTestTarget(),
                                               empty_executable.signature)
        environment = Environment([empty_executable], self.context, [calling_data])
        environment.call()
        self.assertEqual(1, len(self.context.get_editor("test_editor")))
        self.assertEqual(15, self.context.get_editor("test_editor")[0])


    def test_target_subclass_given_base_in_signature_run(self):

        def function_test(context: CallFrame.IContext, target: TestEnvironmentRun.ContextTestTarget):
            l: List = context.get_editor("test_editor")
            l.append(15)
        empty_executable = Executable(Signature.from_function(function_test),
                                                 Executable.TargetScope(TestEnvironmentRun.ContextTestTarget),
                                                 function_test)

        calling_data = Environment.CallingData(CallFrame.Arguments([], {}),
                                               TestEnvironmentRun.ContextTestTargetSub(),
                                               empty_executable.signature)
        environment = Environment([empty_executable], self.context, [calling_data])
        self.assertRaises(RuntimeError, environment.call)


    def test_match_right_target_when_multiple_given_base_class_in_call_data(self):

        def function_test_1(context: CallFrame.IContext, target: TestEnvironmentRun.ContextTestTargetSub):
            l: List = context.get_editor("test_editor")
            l.append(15)

        def function_test_2(context: CallFrame.IContext, target: TestEnvironmentRun.ContextTestTargetNextSub):
            l: List = context.get_editor("test_editor")
            l.append(21)

        executable_1 = Executable(Signature.from_function(function_test_1),
                                                 Executable.TargetScope(TestEnvironmentRun.ContextTestTargetSub),
                                                 function_test_1)

        executable_2 = Executable(Signature.from_function(function_test_2),
                                                 Executable.TargetScope(TestEnvironmentRun.ContextTestTargetNextSub),
                                                 function_test_2)


        calling_data = Environment.CallingData(CallFrame.Arguments([], {}),
                                               TestEnvironmentRun.ContextTestTargetSub(),
                                               executable_1.signature)
        environment = Environment([executable_1, executable_2], self.context, [calling_data])
        environment.call()
        self.assertEqual(1, len(self.context.get_editor("test_editor")))
        self.assertEqual(15, self.context.get_editor("test_editor")[0])


    def test_match_right_target_when_multiple_given_base_subclass_in_call_data(self):

        def function_test_1(context: CallFrame.IContext, target: TestEnvironmentRun.ContextTestTargetSub):
            l: List = context.get_editor("test_editor")
            l.append(15)

        def function_test_2(context: CallFrame.IContext, target: TestEnvironmentRun.ContextTestTargetNextSub):
            l: List = context.get_editor("test_editor")
            l.append(21)

        executable_1 = Executable(Signature.from_function(function_test_1, name="function_test"),
                                                 Executable.TargetScope(TestEnvironmentRun.ContextTestTargetSub),
                                                 function_test_1)

        executable_2 = Executable(Signature.from_function(function_test_2, name="function_test"),
                                                 Executable.TargetScope(TestEnvironmentRun.ContextTestTargetNextSub),
                                                 function_test_2)


        calling_data = Environment.CallingData(CallFrame.Arguments([], {}),
                                               TestEnvironmentRun.ContextTestTargetNextSub(),
                                               executable_1.signature)
        environment = Environment([executable_1, executable_2], self.context, [calling_data])
        environment.call()
        self.assertEqual(1, len(self.context.get_editor("test_editor")))
        self.assertEqual(21, self.context.get_editor("test_editor")[0])

    def test_match_right_target_when_multiple_given_base_fallback(self):

        def function_test_1(context: CallFrame.IContext, target: TestEnvironmentRun.ContextTestTargetSub):
            l: List = context.get_editor("test_editor")
            l.append(15)

        def function_test_2(context: CallFrame.IContext, target: TestEnvironmentRun.ContextTestTargetNextSub):
            l: List = context.get_editor("test_editor")
            l.append(21)

        executable_1 = Executable(Signature.from_function(function_test_1, name="function_test"),
                                                 Executable.TargetScope(TestEnvironmentRun.ContextTestTargetSub),
                                                 function_test_1)

        executable_2 = Executable(Signature.from_function(function_test_2, name="function_test"),
                                                 Executable.TargetScope(TestEnvironmentRun.ContextTestTargetNextSub),
                                                 function_test_2)


        calling_data = Environment.CallingData(CallFrame.Arguments([], {}),
                                               TestEnvironmentRun.ContextTestTarget(),
                                               executable_1.signature)
        environment = Environment([executable_1, executable_2], self.context, [calling_data])
        environment.call()
        self.assertEqual(1, len(self.context.get_editor("test_editor")))
        self.assertEqual(15, self.context.get_editor("test_editor")[0])