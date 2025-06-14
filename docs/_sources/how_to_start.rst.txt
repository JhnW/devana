How to start
==================================
.. include:: _templates/disclaimer.rst

Devana released package is published on `PyPI <https://pypi.org/project/devana/>`_ and can be installed from there:

``pip install -U devana``

Please note the Devana using `libclang package <https://pypi.org/project/libclang/>`_ as parsing backend. This package
simplify installing native dependencies  but may not always work on your system.

The main principle
-----------------------
*Don't ask if you don't want the answer.*

Devana uses lazy evaluation of most fields. This affects not only performance, but also the ability
to read source files.

A given code element may not be supported by Devan (or hopefully not misidentified) but until you specifically
ask for it, you can still work with a partially compatible codebase without catching exceptions and
handling hundreds of errors, just by using information that is currently available.

Core concepts
--------------

Module
+++++++++++++++++

The entry point of using Devana is SoureModule (don't be confused with C++20 modules). SourceModule is a set of
sources and headers files sharing one namespace.  Elements not explicitly assigned to a namespace are treated as
belonging to a global unnamed namespace.

You cannot have ambiguous definitions in module scope, even if they are created by valid C ++ uses
(for example, two separately  compiled files). In that case, you should use multiple modules.

The entire contents of the declarations of types, functions, aliases in, namespaces, and other available
options are loaded into a special structure dividable within the module called the
:class:`~devana.syntax_abstraction.organizers.lexicon.Lexicon`,
regardless of the file inclusion hierarchy.

Lexicon and containers
++++++++++++++++++++++++++
Devana uses two parallel data structures to represent C ++ code, containers
(see :class:`~devana.syntax_abstraction.organizers.codecontainer.CodeContainer`) hierarchy and
:class:`~devana.syntax_abstraction.organizers.lexicon.Lexicon`.
Containers represent the exact matching of code elements to "described" elements, such as a specific file or namespace
instance. The lexicon describes elements in namespaces by merged multiple namespaces in different files, searching for
forward declarations, and providing a link between declarations and element definitions.

You should never want to manually edit the content of a lexicons. The lexicon is automatically updated based on the
container hierarchy. The only case of manual modification of a lexicon is when you intend to emulate the existence of
types not covered in the current module.

Possible problems
-----------------------

Memory usage
++++++++++++++++++++++++++
Devana uses the clanglib backend.In order to ensure that the physical source files are properly related to the result
of parsing C ++ code, each individual file is a separate translation unit in the sense of clang. This can result
in a fairly high demand for RAM. For most small to medium sized projects, this shouldn't be a problem.

If this is a real problem in your use case, consider breaking down the parsing into several stages using
multiple :class:`~devana.syntax_abstraction.organizers.sourcemodule.SourceModule` instances built sequentially.
In the future, sub-modules will be implemented to facilitate this procedure.

External types
++++++++++++++++++++++++++
For a large number of use cases, it is necessary to have information about all types within the files listed
in :class:`~devana.syntax_abstraction.organizers.sourcemodule.SourceModule`. Nobody should want to include
files with complex libraries, not necessarily Devan parsable, such as standard library or boost library.

So the question is what to do with such types? The simplest and recommended answer - avoid them. The second solution
is to wait for the upcoming corrections in the library to provide support for external types. We already
support external typedefs.
If you really have a problem with that, I recommend that you create a fake instance of the type
(along with its namespaces, etc.) and inject it into :class:`~devana.syntax_abstraction.organizers.lexicon.Lexicon`.


Examples
--------------

.. toctree::
   :maxdepth: 1

   demos/demo_include_map
   demos/demo_meta_info_enum
   demos/demo_accessors_generator
   demos/demo_low_level_preprocessor