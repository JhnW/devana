Generate meta information for enums
==================================================

Please find demo code in our `GitHub <https://github.com/JhnW/devana/tree/main/examples/meta_enum>`_.

This demo program will read input header file located in input directory and product set headers and source files in
output directory. Basing on defined enums in input/enums.h it will produce implementation of classes and template
functions for each enum who provide meta information abut enum: name, count of fields, names and values of fields.

This example is shoe you a bit real application of Devana. Enum meta information wil be useful for automatic generate
combo box list in GUI etc.

