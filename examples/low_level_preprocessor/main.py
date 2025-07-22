from typing import Any, List
from pathlib import Path
from devana.preprocessing.premade.components.parser.extractor import CommentExtractor
from devana.preprocessing.premade.components.executor.executor import Executor
from devana.preprocessing.premade.components.executor.executable import Executable, Signature
from devana.preprocessing.premade.components.executor.environment import Environment, CallFrame, EnvironmentCreator
from devana.preprocessing.premade.components.executor.editor import SourceFileEditor
from devana.preprocessing.premade.components.savers.filesaver import FileSaver
from devana.syntax_abstraction.organizers import SourceModule, ModuleFilter
from devana.syntax_abstraction.organizers.sourcefile import SourceFile
from devana.preprocessing.preprocessor import Preprocessor
from devana.preprocessing.premade.components.parser.parser import Parser
from devana.syntax_abstraction.syntax import ISyntaxElement
from devana.syntax_abstraction.classinfo import ClassInfo
from devana.syntax_abstraction.enuminfo import EnumInfo
from devana.syntax_abstraction.functioninfo import FunctionInfo



# The following example shows how to use the devana preprocessor in a low-level way - if you need to modify its behavior
# or a more high-level preprocessor build wrapper is not yet available within the project.
# In this example, we will operate on one file and also generate one source file based on comments

# --------------------------------------------------
# Preparing the data source
# --------------------------------------------------

# Creates a standard devana module to parse input C++ files
module_filter = ModuleFilter([r"in\.hpp"])
module = SourceModule("MyAPICodeBase", "./input", module_filter)

# The class implementing the IExtractor interface provides input data - we'll use an extractor that
# works on comments in the code. You can write your own or use others (if they already exist).
extractor = CommentExtractor([module])

# --------------------------------------------------
# Preparing the function
# --------------------------------------------------

# We will prepare some sample preprocessor functions. They do not do any meaningful work,
# they are just a demonstration of using the API
# Context, and target parameters are required and passed by runtime.

# the most primitive function
def basic_log_all_fnc(context: CallFrame.IContext, target: Any):
    print(f"Vist: {target}")


# two twin functions to show the possibility of overloading for different targets
def basic_log_only_class_fnc(context: CallFrame.IContext, target: ClassInfo):
    print(f"Vist enum: {target}")

def basic_log_only_enum_fnc(context: CallFrame.IContext, target: EnumInfo):
    print(f"Vist class: {target}")

# This function takes two parameters, a list of versions that must be checked and a string that must be provided but
# does not have to be. Arguments with default names can also be passed out of the organization
# by name - see usage in the example input file.

def generate_stupid_function_based_on_class(context: CallFrame.IContext, target: EnumInfo,
                                            version: List[int], name: str = "Test"):

    # we assume that this output editor will be present in the in text - we will put it there in the next steps
    editor = context.get_editor("editor")
    # cast to expected content to edit
    source_file: SourceFile = editor.editable

    # Let's just create an example declaration of a dumb function
    function = FunctionInfo.create_default(source_file)
    function.name = f"{name}_{target.name}"
    for v in version:
        arg = FunctionInfo.Argument.create_default(function)
        arg.name = f"arg_{v}"
        function.arguments.append(arg)
    source_file.content.append(function)


#Now we need to create signatures for the functions under which they will be used. Fortunately, there is a ready method
# that allows you to create them based on argument names and type annotations in Python.

signature_1 = Signature.from_function(basic_log_all_fnc)
# change name, yu can check that why you will use bad logger it my cause error
signature_2 = Signature.from_function(basic_log_only_class_fnc, "Logger1")
signature_3 = Signature.from_function(basic_log_only_enum_fnc, "Logger2")
# namespace
signature_4 = Signature.from_function(generate_stupid_function_based_on_class, namespaces=["test_nm"])


# now create the final parser used as input of preprocessor; we need to provide all used signatures
parser = Parser(extractor, [signature_1, signature_2, signature_3, signature_4])

# --------------------------------------------------
# Preparing executable
# --------------------------------------------------

# Now we can move on to creating an instance of the class that executes our code

exe_1 = Executable(signature_1, Executable.TargetScope(), basic_log_all_fnc)
# for 3 and 4 we need to provide target
exe_2 = Executable(signature_2, Executable.TargetScope(ClassInfo), basic_log_only_class_fnc)
exe_3 = Executable(signature_3, Executable.TargetScope(EnumInfo), basic_log_only_enum_fnc)
exe_4 = Executable(signature_4, Executable.TargetScope(), generate_stupid_function_based_on_class)


# Now we need to create a function that will create executable environments.
# Environments are used to isolate contexts - you can create many of them. In this function, you can also
# filter property calls to divide them between different environments that have their own executors.
# However, we will now create a very basic function.

def environment_creator_fnc(calling_data: List[Environment.CallingData]) -> List[Environment]:
    # create initial state of editor, we can here add global data etc.
    file = SourceFile.create_default()
    file.header_guard = "META_DATA"
    editor_cpp = SourceFileEditor("Meta.hpp", source=file)
    # We put in editor two sets of data, editor and extra data in stares. For now any function uses states but
    #  you can change it to use state by your own
    context = Environment.Context({"editor":editor_cpp}, {"version": "5.7.1"})
    return [Environment[ISyntaxElement]([exe_1, exe_2, exe_3, exe_4],context, calling_data)]


environment_creator = EnvironmentCreator(environment_creator_fnc)
# here we need to list all executable uses in all environments
executor = Executor[ISyntaxElement](environment_creator, [exe_1, exe_2, exe_3, exe_4])

# --------------------------------------------------
# Preparing output
# --------------------------------------------------

# configure output directory
saver = FileSaver(FileSaver.Configuration(Path(__file__).parent))


# --------------------------------------------------
# Run
# --------------------------------------------------

# put all components together
preprocessor = Preprocessor(parser, executor, saver)
preprocessor.process()


