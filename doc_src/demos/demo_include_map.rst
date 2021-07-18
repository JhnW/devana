Graph of internal dependencies
==================================================

Please find demo code in our `GitHub <https://github.com/JhnW/devana/tree/main/examples/includes_graph>`_.

This demo program will download and unpack `dlib <http://dlib.net/>`_. This step is optional and can be controlled
by programs argument. Then, the header files are parsed. On this basis, a dependency graph is generated.

If you don't have at least 16 GB of RAM, you should set the module path to the project subfolder in order to save memory
usage. You can also use this argument to try a different set of source files from a different project.

