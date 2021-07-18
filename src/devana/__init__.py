from ._version import __version__

"""
Devana is a python tool that make it easy to parsing, format, transform and generate C++ (or C) code. 
This tool uses libclang to parse the code. Fundamental problems, bugs and missing features of libclang are fixed in 
Devann's internal code.

Please note that Devana focuses on the header-level code e.g. class and functions definitions, templates resolving, 
typedefs and includes. Control statements, arithmetics operations etc. (pure body of functions) are supported as access
to raw string field "body". It is planned to introduce more control over this type of code in future versions.   
Devana is still under development. At the moment, only parsing is available. 
"""
