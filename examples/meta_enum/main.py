#!/bin/bash/python3
from devana.syntax_abstraction.organizers.sourcemodule import SourceModule, ModuleFilter
from devana.syntax_abstraction.functioninfo import FunctionModification
from devana.syntax_abstraction.typeexpression import *
from devana.syntax_abstraction.classinfo import *
from devana.code_generation.printers.default.defaultprinter import create_default_printer
from devana.code_generation.stubtype import StubType
from devana.syntax_abstraction.enuminfo import EnumInfo
from devana.code_generation.printers.configuration import PrinterConfiguration
from devana.syntax_abstraction.organizers.sourcefile import SourceFile, IncludeInfo, SourceFileType
from shutil import copyfile


def create_enum_element() -> ClassInfo:
    element = ClassInfo()
    element.name = "EnumElement"

    constructor = ConstructorInfo()
    constructor.name = "EnumElement"
    constructor.access_specifier = AccessSpecifier.PUBLIC

    arg = FunctionInfo.Argument()
    arg.name = "name"
    arg.type = TypeExpression()
    arg.type.modification |= TypeModification.CONST | TypeModification.REFERENCE
    arg.type.details = StubType("std::string")
    constructor.arguments.append(arg)

    arg = FunctionInfo.Argument()
    arg.name = "value"
    arg.type = TypeExpression()
    arg.type.details = BasicType.INT
    constructor.arguments.append(arg)

    constructor.initializer_list = [ConstructorInfo.InitializerInfo("name", "name"),
                                    ConstructorInfo.InitializerInfo("value", "value")]
    constructor.body = ""  # we need to define body (as empty in this case) to say devana: it is function definition

    element.content.append(constructor)

    member = FieldInfo()
    member.access_specifier = AccessSpecifier.PUBLIC
    member.name = "name"
    member.type = TypeExpression()
    member.type.details = StubType("std::string")
    member.type.modification |= TypeModification.CONST
    element.content.append(member)

    member = FieldInfo()
    member.access_specifier = AccessSpecifier.PUBLIC
    member.name = "value"
    member.type = TypeExpression()
    member.type.details = BasicType.INT
    member.type.modification |= TypeModification.CONST
    element.content.append(member)

    return element


def create_enum_info_interface(member_type: ClassInfo) -> ClassInfo:
    interface = ClassInfo()
    interface.name = "EnumInformationInterface"
    interface.is_class = True
    interface.content.append(AccessSpecifier.PUBLIC)

    func = MethodInfo()
    func.name = "name"
    func.return_type.details = StubType("std::string")
    func.return_type.modification |= TypeModification.CONST | TypeModification.REFERENCE
    func.modification |= FunctionModification.CONST | FunctionModification.PURE_VIRTUAL
    func.access_specifier = AccessSpecifier.PUBLIC
    interface.content.append(func)

    func = MethodInfo()
    func.name = "count"
    func.return_type.details = StubType("size_t")
    func.modification |= FunctionModification.CONST | FunctionModification.PURE_VIRTUAL
    func.access_specifier = AccessSpecifier.PUBLIC
    interface.content.append(func)

    func = MethodInfo()
    func.name = "at"
    func.return_type.details = member_type
    func.return_type.modification |= TypeModification.CONST | TypeModification.REFERENCE
    func.modification |= FunctionModification.CONST | FunctionModification.PURE_VIRTUAL
    func.access_specifier = AccessSpecifier.PUBLIC
    func.arguments = [FunctionInfo.Argument()]
    func.arguments[0].name = "i"
    func.arguments[0].type = TypeExpression()
    func.arguments[0].type.details = StubType("size_t")
    interface.content.append(func)

    func = MethodInfo()
    func.name = "fromValue"
    func.return_type.details = member_type
    func.return_type.modification |= TypeModification.CONST | TypeModification.REFERENCE
    func.modification |= FunctionModification.CONST | FunctionModification.PURE_VIRTUAL
    func.access_specifier = AccessSpecifier.PUBLIC
    func.arguments = [FunctionInfo.Argument()]
    func.arguments[0].name = "value"
    func.arguments[0].type = TypeExpression()
    func.arguments[0].type.details = BasicType.INT
    interface.content.append(func)

    return interface


def create_enum_info_class(source_enum: EnumInfo, interface_type: ClassInfo, element_type: ClassInfo, ) -> ClassInfo:
    impl = ClassInfo()
    impl.is_class = True
    impl.name = f"{source_enum.name}EnumInformationInstance"
    impl.inheritance = InheritanceInfo()
    impl.inheritance.type_parents = [InheritanceInfo.InheritanceValue()]
    impl.inheritance.type_parents[0].access_specifier = AccessSpecifier.PUBLIC
    impl.inheritance.type_parents[0].type = interface_type

    impl.content.append(AccessSpecifier.PUBLIC)

    static_constructor = MethodInfo()
    static_constructor.name = "create"
    static_constructor.modification |= FunctionModification.STATIC
    static_constructor.return_type.modification |= TypeModification.CONST | TypeModification.POINTER
    static_constructor.return_type.details = impl
    static_constructor.body = f"if(_instance == nullptr) _instance = new {impl.name}();\n"
    static_constructor.body += "return _instance;"
    impl.content.append(static_constructor)

    func = MethodInfo()
    func.name = "name"
    func.return_type.details = StubType("std::string")
    func.return_type.modification |= TypeModification.CONST | TypeModification.REFERENCE
    func.modification |= FunctionModification.CONST | FunctionModification.VIRTUAL | FunctionModification.OVERRIDE
    func.access_specifier = AccessSpecifier.PUBLIC
    func.body = "return _name;"
    impl.content.append(func)

    func = MethodInfo()
    func.name = "count"
    func.return_type.details = StubType("size_t")
    func.modification |= FunctionModification.CONST | FunctionModification.VIRTUAL | FunctionModification.OVERRIDE
    func.access_specifier = AccessSpecifier.PUBLIC
    func.body = "return _values.size();"
    impl.content.append(func)

    func = MethodInfo()
    func.name = "at"
    func.return_type.details = element_type
    func.return_type.modification |= TypeModification.CONST | TypeModification.REFERENCE
    func.modification |= FunctionModification.CONST | FunctionModification.VIRTUAL | FunctionModification.OVERRIDE
    func.access_specifier = AccessSpecifier.PUBLIC
    func.arguments = [FunctionInfo.Argument()]
    func.arguments[0].name = "i"
    func.arguments[0].type = TypeExpression()
    func.arguments[0].type.details = StubType("size_t")
    func.body = "return _values.at(i);"
    impl.content.append(func)

    func = MethodInfo()
    func.name = "fromValue"
    func.return_type.details = element_type
    func.return_type.modification |= TypeModification.CONST | TypeModification.REFERENCE
    func.modification |= FunctionModification.CONST | FunctionModification.VIRTUAL | FunctionModification.OVERRIDE
    func.access_specifier = AccessSpecifier.PUBLIC
    func.arguments = [FunctionInfo.Argument()]
    func.arguments[0].name = "value"
    func.arguments[0].type = TypeExpression()
    func.arguments[0].type.details = BasicType.INT
    basic_printer = PrinterConfiguration()
    func.body = "for(size_t i = 0; i < _values.size(); i++)\n"
    func.body += basic_printer.format_line("{")
    basic_printer.indent += 1
    func.body += basic_printer.format_line("if(_values[i].value == value) return _values[i];")
    basic_printer.indent -= 1
    func.body += basic_printer.format_line("}")
    func.body += basic_printer.format_line('throw std::out_of_range("Value is not present in enum scope.");')
    impl.content.append(func)

    impl.content.append(AccessSpecifier.PRIVATE)

    constructor = ConstructorInfo()
    constructor.name = impl.name
    constructor.access_specifier = AccessSpecifier.PRIVATE

    initializer_list_array = "{" + ",".join(
        [f'{element_type.name}("{x.name}",{x.value})' for x in source_enum.content]) + "}"

    constructor.initializer_list = [ConstructorInfo.InitializerInfo("_name", f'"{source_enum.name}"'),
                                    ConstructorInfo.InitializerInfo("_values", initializer_list_array)]

    constructor.body = ""  # we need to define body (as empty in this case) to say devana: it is function definition
    impl.content.append(constructor)

    member = FieldInfo()
    member.access_specifier = AccessSpecifier.PRIVATE
    member.name = "_name"
    member.type = TypeExpression()
    member.type.details = StubType("std::string")
    member.type.modification |= TypeModification.CONST
    impl.content.append(member)

    member = FieldInfo()
    member.access_specifier = AccessSpecifier.PRIVATE
    member.name = "_values"
    member.type = TypeExpression()
    member.type.details = StubType(f"std::array<{element_type.name}, {len(source_enum.content)}>")
    member.type.modification |= TypeModification.CONST
    impl.content.append(member)

    member = FieldInfo()
    member.access_specifier = AccessSpecifier.PRIVATE
    member.name = "_instance"
    member.type = TypeExpression()
    member.type.details = impl
    member.type.modification |= TypeModification.POINTER | TypeModification.STATIC
    impl.content.append(member)

    return impl


def create_core_provider(interface_type: ClassInfo) -> FunctionInfo:
    provider = FunctionInfo()
    provider.name = "get_enum_info"
    provider.return_type.details = interface_type
    provider.return_type.modification = TypeModification.POINTER | TypeModification.CONST
    provider.template = TemplateInfo()
    provider.template.parameters = [TemplateInfo.TemplateParameter()]
    provider.template.parameters[0].name = "E"
    provider.body = "return nullptr;"
    return provider


def create_specialized_provider(interface_type: ClassInfo, source_enum: EnumInfo, impl: ClassInfo) -> FunctionInfo:
    provider = FunctionInfo()
    provider.name = "get_enum_info"
    provider.return_type.details = interface_type
    provider.return_type.modification = TypeModification.POINTER | TypeModification.CONST
    provider.template = TemplateInfo()
    provider.template.specialisation_values = [TypeExpression()]
    provider.template.specialisation_values[0].details = source_enum
    provider.body = f"return {impl.name}::create();"
    return provider


def enum_info_class_cpp(enum_class_info: ClassInfo):
    member = FieldInfo()
    member.access_specifier = AccessSpecifier.PRIVATE
    member.name = "_instance"
    member.type = TypeExpression()
    member.type.details = enum_class_info
    member.type.modification |= TypeModification.POINTER | TypeModification.STATIC
    member.lexicon = enum_class_info
    return member


if __name__ == "__main__":
    module_filter = ModuleFilter([r"enums\.h"])  # we want only one file
    source = SourceModule("API", "./input", module_filter)  # create parsing module
    file = source.files[0]  # in this example we are using one file
    copyfile("./input/enums.h", "./output/enums.h")  # copy input file to output directory without changes
    enum_value_info_code = create_enum_element()  # create core structure for enum value information
    interface_code = create_enum_info_interface(enum_value_info_code)  # create c++ abstract class
    provider_code = create_core_provider(interface_code)  # and template function as getter

    enums = filter(lambda enum: isinstance(enum, EnumInfo), file.content)  # we want only enums
    enum_info_classes = []
    enum_info_providers = []
    for e in enums:
        enum_info = create_enum_info_class(e, interface_code, enum_value_info_code)
        enum_info_classes.append(enum_info)
        enum_info_providers.append(create_specialized_provider(interface_code, e, enum_info))

    # main header file
    header_file = SourceFile()
    header_file.type = SourceFileType.HEADER
    header_file.header_guard = "META_ENUM_INFO"

    source_file_header = IncludeInfo()
    source_file_header.value = file.name
    header_file.includes.append(source_file_header)

    source_file_header = IncludeInfo()
    source_file_header.value = "string"
    source_file_header.is_standard = True  # to write him as <string> instead of "string"
    header_file.includes.append(source_file_header)

    source_file_header = IncludeInfo()
    source_file_header.value = "stdexcept"
    source_file_header.is_standard = True
    header_file.includes.append(source_file_header)

    source_file_header = IncludeInfo()
    source_file_header.value = "array"
    source_file_header.is_standard = True
    header_file.includes.append(source_file_header)

    header_file.content.append(enum_value_info_code)
    header_file.content.append(interface_code)
    header_file.content += enum_info_classes

    printer = create_default_printer()

    with open("./output/meta_enums.h", "w") as f:
        f.write(printer.print(header_file))

    # header for templates
    header_file = SourceFile()
    header_file.type = SourceFileType.HEADER
    header_file.header_guard = "META_ENUM_GETTER"

    source_file_header = IncludeInfo()
    source_file_header.value = "meta_enums.h"
    header_file.includes.append(source_file_header)
    header_file.content.append(provider_code)
    header_file.content += enum_info_providers

    with open("./output/meta_enums_getter.h", "w") as f:
        f.write(printer.print(header_file))

    # we need to create cpp file with static variable, but for now devana do not provide
    # pure way to namespace is variable def
    impl_file = SourceFile()
    impl_file.type = SourceFileType.IMPLEMENTATION
    source_file_header = IncludeInfo()
    source_file_header.value = "meta_enums.h"
    impl_file.includes.append(source_file_header)
    for e in enum_info_classes:
        impl_file.content.append(StubType(f"{e.name}* {e.name}::_instance = nullptr;\n"))

    with open("./output/meta_enums.cpp", "w") as f:
        f.write(printer.print(impl_file))
