Devana
======
![License: LGPL v2.1](https://img.shields.io/github/license/jhnw/devana)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/devana)
![PyPI - Status](https://img.shields.io/pypi/status/devana)
![PyPI - Format](https://img.shields.io/pypi/format/devana)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/devana)
\
[![Tests](https://github.com/JhnW/devana/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/JhnW/devana/actions/workflows/tests.yml)
[![Release](https://github.com/JhnW/devana/actions/workflows/release.yml/badge.svg)](https://github.com/JhnW/devana/actions/workflows/release.yml)
\
![PyPI](https://img.shields.io/pypi/v/devana)
![GitHub issues](https://img.shields.io/github/issues/jhnw/devana)
![Website](https://img.shields.io/website?url=https%3A%2F%2Fjhnw.github.io%2Fdevana%2F)
![PyPI - Downloads](https://img.shields.io/pypi/dm/devana)

Devana is a python tool that make it easy to parsing, format, transform and generate C++ (or C) code. 
This tool uses libclang to parse the code. Fundamental problems, bugs and missing features of libclang are fixed in 
Devann's internal code.\
Please note that Devana focuses on the header-level code e.g. class and functions definitions, templates resolving, 
typedefs and includes. Control statements, arithmetics operations etc. (pure body of functions) are supported as access
to raw string field "body". It is planned to introduce more control over this type of code in future versions.   
**Important:** Devana is still under development. At the moment, only parsing is available 
(almost full coverage of development plans). Please check [roadmap](http://jhnw.github.io/devana/roadmap.html).

## Installation
Devana is published on [PyPI](https://pypi.org/project/devana/) and can be installed from there:
>pip install -U devana

If you wish to install Devana for development purposes, refer to the contributors guide.

## How to start
You can find the complete guide in [this](http://jhnw.github.io/devana/how_to_start.html) section of the documentation.\
Demo applications are located in project repository inside demo folder.

## Documentation
Documentation is available from [GitHub Pages](http://jhnw.github.io/devana).

## Contributing
Please check [contributing guide](http://jhnw.github.io/devana/contributing.html) for take more details about contributing this project.\
For now, the most wanted help is bugreports, bugfix, writing test and parser features completion. You can write e-mail
to me directly with question about help.

## Testing
Continuous testing is [GitHub Actions](https://github.com/JhnW/devana/actions).
For information on running tests locally, refer to the contributors guide.

## Roadmap
A detailed list of missing functionalities and planned features can be found in the 
[documentation](http://jhnw.github.io/devana/roadmap.html).

