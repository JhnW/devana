Demo Low Level Preprocessor
==================================================

Please find demo code in our `GitHub <https://github.com/JhnW/devana/tree/main/examples/demo_low_level_preprocessor>`_.

This documentation provides a step-by-step guide on how to use the Devana preprocessor in a low-level way to modify its behavior or when a more high-level preprocessor build wrapper is not yet available within the project. In this example, we will operate on one file and generate one source file based on comments.

Preparing the Data Source
-------------------------

First, we need to create a standard Devana module to parse input C++ files. We will use a `ModuleFilter` to filter the files and a `SourceModule` to represent the module.

.. code-block:: python

    from devana.syntax_abstraction.organizers import SourceModule, ModuleFilter

    module_filter = ModuleFilter([r"in\\.hpp"])
    module = SourceModule("MyAPICodeBase", "./input", module_filter)

Next, we create an extractor that works on comments in the code. The `CommentExtractor` class implements the `IExtractor` interface and provides input data.

.. code-block:: python

    from devana.preprocessing.premade.components.parser.extractor import CommentExtractor

    extractor = CommentExtractor([module])

Preparing the Function
----------------------

We will prepare some sample preprocessor functions. These functions do not perform any meaningful work; they are just a demonstration of using the API. Context and target parameters are required and passed by runtime.

.. code-block:: python

    from devana.preprocessing.premade.components.executor.executable import CallFrame
    from devana.syntax_abstraction.classinfo import ClassInfo
    from devana.syntax_abstraction.enuminfo import EnumInfo
    from devana.syntax_abstraction.functioninfo import FunctionInfo

    def basic_log_all_fnc(context: CallFrame.IContext, target: Any):
        print(f"Visit: {target}")

    def basic_log_only_class_fnc(context: CallFrame.IContext, target: ClassInfo):
        print(f"Visit class: {target}")

    def basic_log_only_enum_fnc(context: CallFrame.IContext, target: EnumInfo):
        print(f"Visit enum: {target}")

    def generate_stupid_function_based_on_class(context: CallFrame.IContext, target: EnumInfo, version: List[int], name: str = "Test"):
        editor = context.get_editor("editor")
        source_file: SourceFile = editor.editable
        function = FunctionInfo.create_default(source_file)
        function.name = f"{name}_{target.name}"
        for v in version:
            arg = FunctionInfo.Argument.create_default(function)
            arg.name = f"arg_{v}"
            function.arguments.append(arg)
        source_file.content.append(function)

Now we need to create signatures for the functions under which they will be used. The `Signature` class provides a method to create them based on argument names and type annotations in Python.

.. code-block:: python

    from devana.preprocessing.premade.components.executor.executable import Signature

    signature_1 = Signature.from_function(basic_log_all_fnc)
    signature_2 = Signature.from_function(basic_log_only_class_fnc, "Logger1")
    signature_3 = Signature.from_function(basic_log_only_enum_fnc, "Logger2")
    signature_4 = Signature.from_function(generate_stupid_function_based_on_class, namespaces=["test_nm"])

Next, we create the final parser used as input for the preprocessor. We need to provide all used signatures.

.. code-block:: python

    from devana.preprocessing.premade.components.parser.parser import Parser

    parser = Parser(extractor, [signature_1, signature_2, signature_3, signature_4])

Preparing the Executable
------------------------

Now we can create an instance of the class that executes our code.

.. code-block:: python

    from devana.preprocessing.premade.components.executor.executor import Executor
    from devana.preprocessing.premade.components.executor.executable import Executable

    exe_1 = Executable(signature_1, Executable.TargetScope(), basic_log_all_fnc)
    exe_2 = Executable(signature_2, Executable.TargetScope(ClassInfo), basic_log_only_class_fnc)
    exe_3 = Executable(signature_3, Executable.TargetScope(EnumInfo), basic_log_only_enum_fnc)
    exe_4 = Executable(signature_4, Executable.TargetScope(), generate_stupid_function_based_on_class)

Next, we create a function that will create executable environments. Environments are used to isolate contexts.

.. code-block:: python

    from devana.preprocessing.premade.components.executor.environment import Environment, EnvironmentCreator
    from devana.syntax_abstraction.syntax import ISyntaxElement
    from devana.preprocessing.premade.components.executor.editor import SourceFileEditor
    from devana.syntax_abstraction.organizers.sourcefile import SourceFile

    def environment_creator_fnc(calling_data: List[Environment.CallingData]) -> List[Environment]:
        file = SourceFile.create_default()
        file.header_guard = "META_DATA"
        editor_cpp = SourceFileEditor("Meta.hpp", source=file)
        context = Environment.Context({"editor": editor_cpp}, {"version": "5.7.1"})
        return [Environment[ISyntaxElement]([exe_1, exe_2, exe_3, exe_4], context, calling_data)]

    environment_creator = EnvironmentCreator(environment_creator_fnc)
    executor = Executor[ISyntaxElement](environment_creator, [exe_1, exe_2, exe_3, exe_4])

Preparing the Output
--------------------

Configure the output directory.

.. code-block:: python

    from devana.preprocessing.premade.components.savers.filesaver import FileSaver
    from pathlib import Path

    saver = FileSaver(FileSaver.Configuration(Path(__file__).parent))

Running the Preprocessor
------------------------

Finally, we put all components together and run the preprocessor.

.. code-block:: python

    from devana.preprocessing.preprocessor import Preprocessor

    preprocessor = Preprocessor(parser, executor, saver)
    preprocessor.process()