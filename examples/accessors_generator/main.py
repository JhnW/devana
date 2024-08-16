from typing import Iterable, Tuple, Optional, List
from dataclasses import dataclass
from os import path, makedirs

from devana.code_generation.printers.default.defaultprinter import create_default_printer, CodePrinter
from devana.syntax_abstraction.classinfo import MethodInfo, Comment, FunctionInfo, AccessSpecifier, ClassInfo, FieldInfo
from devana.syntax_abstraction.organizers import ModuleFilter, SourceModule, SourceFile, SourceFileType, IncludeInfo
from devana.syntax_abstraction.syntax import ISyntaxElement

from devana.syntax_abstraction.functioninfo import BasicType, FunctionModification
from devana.syntax_abstraction.attribute import Attribute, AttributeDeclaration
from devana.syntax_abstraction.typeexpression import TypeModification


@dataclass
class HeaderFileData:
    name: str
    content: List[ISyntaxElement]

    @property
    def class_infos(self) -> Iterable[ClassInfo]:
        return filter(lambda element: isinstance(element, ClassInfo), self.content)


def get_devana_comments(comment: Comment) -> Iterable[str]:
    # Function to get all devana comments properly formatted.
    for comment_source in comment.text:
        if (formatted_comment := comment_source.lstrip()).startswith("devana:"):
            yield formatted_comment


def get_field_name(field: FieldInfo) -> str:
    # Function to retrieve the field name.
    name: str = field.name.capitalize()

    if field.associated_comment:
        for text in get_devana_comments(field.associated_comment):
            if text.startswith("devana: custom-name="):
                name = text.split("=")[1]
                break

    return name


def create_field_methods(field: FieldInfo) -> Tuple[MethodInfo, MethodInfo]:
    # Function to generate setter and getter for field.
    def should_ignore_attributes(comment: Optional[Comment]) -> bool:
        return "devana: ignore-attributes" in get_devana_comments(comment) if comment else False

    field_name: str = get_field_name(field)
    maybe_unused_attribute: Attribute = Attribute("maybe_unused")
    nodiscard_attribute: Attribute = Attribute("nodiscard")

    field_setter = MethodInfo()
    field_setter.body = f"{field.name} = new{field.name.capitalize()};"
    field_setter.access_specifier = AccessSpecifier.PUBLIC

    field_setter.name = f"set{field_name}"
    field_setter.return_type = BasicType.VOID

    setter_arg = FunctionInfo.Argument()
    setter_arg.name = f"new{field.name.capitalize()}"
    setter_arg.type.details = field.type
    if field.type.name == "string":
        setter_arg.type.modification |= TypeModification.CONST | TypeModification.REFERENCE

    field_setter.arguments.append(setter_arg)

    field_getter = MethodInfo()
    field_getter.body = f"return {field.name};"
    field_getter.access_specifier = AccessSpecifier.PUBLIC

    field_getter.name = f"get{field_name}"
    field_getter.return_type = field.type
    field_getter.modification |= FunctionModification.CONST

    if not should_ignore_attributes(field.associated_comment):
        field_getter.attributes.append(
            AttributeDeclaration([nodiscard_attribute, maybe_unused_attribute])
        )
        field_setter.attributes.append(
            AttributeDeclaration([maybe_unused_attribute])
        )

    return field_setter, field_getter


def create_class_methods(class_info: ClassInfo):
    # Function to generate methods for all class fields.
    def should_ignore_field(comment: Optional[Comment]) -> bool:
        return "devana: ignore-field" in get_devana_comments(comment) if comment else False

    for constructor in class_info.constructors:
        if constructor.body == "{}":
            # We need to define body (as empty in this case) to say devana: it is function definition.
            constructor.body = ""

    for private_field in filter(lambda field: isinstance(field, FieldInfo), class_info.private):
        if should_ignore_field(private_field.associated_comment):
            continue

        class_info.content.extend(create_field_methods(field=private_field))


def load_files_content() -> Iterable[HeaderFileData]:
    module_filter = ModuleFilter(allowed_filter=[".h"])  # Accept only header files.
    source = SourceModule("HEADERS", "./input", module_filter=module_filter)
    for file in source.files:
        yield HeaderFileData(file.name, file.content)


def main():
    if not path.exists("./output"):
        makedirs(path.dirname("./output/"))

    printer: CodePrinter = create_default_printer()

    iostream_include = IncludeInfo()
    iostream_include.value = "iostream"
    iostream_include.is_standard = True  # to write this as <iostream> instead of "iostream"

    string_include = IncludeInfo()
    string_include.value = "string"
    string_include.is_standard = True  # to write this as <string> instead of "string"

    for file_data in load_files_content():
        file_name: str = file_data.name

        header_file = SourceFile()
        header_file.type = SourceFileType.HEADER

        # Convert guard against 'EXAMPLE.H' to 'EXAMPLE_H'
        header_file.header_guard = file_name.upper().replace(".", "_")
        header_file.includes.extend([string_include, iostream_include])

        for class_info in file_data.class_infos:
            create_class_methods(class_info)
            header_file.content.append(class_info)

        with open(f"./output/{file_name}", "w+", encoding="utf-8") as file:
            file.write(printer.print(header_file))


if __name__ == "__main__":
    main()
