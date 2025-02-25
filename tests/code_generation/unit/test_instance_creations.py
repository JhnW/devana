from devana.syntax_abstraction.organizers.sourcefile import SourceFile, IncludeInfo, SourceFileType
from devana.syntax_abstraction.typeexpression import TypeModification
from devana.syntax_abstraction.usingnamespace import UsingNamespace
from devana.syntax_abstraction.namespaceinfo import NamespaceInfo
from devana.syntax_abstraction.functiontype import FunctionType
from devana.syntax_abstraction.variable import GlobalVariable
from devana.syntax_abstraction.typedefinfo import TypedefInfo
from devana.syntax_abstraction.conceptinfo import ConceptInfo
from devana.syntax_abstraction.unioninfo import UnionInfo
from devana.syntax_abstraction.enuminfo import EnumInfo
from devana.syntax_abstraction.externc import ExternC
from devana.syntax_abstraction.using import Using
from devana.syntax_abstraction.classinfo import *

from devana.utility.init_params import init_params
import unittest

class TestInstanceCreations(unittest.TestCase):

    def test_variable_creation(self):
        variable = Variable.from_params(
            name="testVar",
            default_value=10,
            type=TypeExpression.from_params(
                details=BasicType.INT,
                modification=TypeModification.CONST
            )
        )
        self.assertEqual(variable.type.details, BasicType.INT)
        self.assertEqual(variable.type.modification, TypeModification.CONST)
        self.assertEqual(variable.default_value, 10)
        self.assertEqual(variable.name, "testVar")

    def test_global_variable_creation(self):
        global_variable = GlobalVariable.from_params(
            name="testGlobalVar",
            default_value=5.1,
            type=TypeExpression.from_params(
                details=BasicType.FLOAT,
                modification=TypeModification.CONSTEXPR
            )
        )
        self.assertEqual(global_variable.type.details, BasicType.FLOAT)
        self.assertEqual(global_variable.type.modification, TypeModification.CONSTEXPR)
        self.assertEqual(global_variable.default_value, 5.1)
        self.assertEqual(global_variable.name, "testGlobalVar")

    def test_usingnamespace_creation(self):
        usingnamespace = UsingNamespace.from_params(namespaces=["foo", "bar"])
        self.assertEqual(usingnamespace.namespaces, ["foo", "bar"])

    def test_using_creation(self):
        using = Using.from_params(
            name="str",
            type_info=TypeExpression.from_params(
                details=StubType("std::string")
            )
        )
        self.assertEqual(using.name, "str")
        self.assertEqual(using.type_info.details.name, "std::string")

    def test_union_creation(self):
        union = UnionInfo.from_params(
            name="testUnion",
            is_declaration=True,
        )
        self.assertEqual(union.name, "testUnion")
        self.assertEqual(union.content, [])
        self.assertEqual(union.is_declaration, True)
        self.assertFalse(union.is_definition, False)

    def test_type_expression_creation(self):
        type_expr = TypeExpression.from_params(
            modification=TypeModification.CONST | TypeModification.REFERENCE,
            namespaces=["foo"],
            details=BasicType.CHAR,
        )
        self.assertEqual(type_expr.name, "const char&")
        self.assertEqual(type_expr.namespaces, ["foo"])

    def test_typedef_creation(self):
        using = TypedefInfo.from_params(
            name="str",
            type_info=TypeExpression.from_params(
                details=StubType("std::string")
            )
        )
        self.assertEqual(using.name, "str")
        self.assertEqual(using.type_info.details.name, "std::string")

    def test_template_creation(self):
        template = TemplateInfo.from_params(
            parameters=[
                TemplateInfo.TemplateParameter.from_params(
                    name="A"
                ),
                TemplateInfo.TemplateParameter.from_params(
                    name="B"
                )
            ],
            is_empty=False
        )
        self.assertEqual(len(template.parameters), 2)
        self.assertEqual(template.is_empty, False)

    def test_namespace_creation(self):
        namespace = NamespaceInfo.from_params(
            namespace="cat",
            content=[
                FunctionInfo.from_params(
                    name="isSleeping",
                    return_type=BasicType.BOOL,
                    body="return true;"
                )
            ]
        )
        self.assertEqual(namespace.namespace, "cat")
        self.assertTrue(isinstance(namespace.content[0], FunctionInfo))

    def test_function_type_creation(self):
        function_type = FunctionType.from_params(
            return_type=BasicType.VOID,
            arguments=[]
        )
        self.assertEqual(function_type.return_type, BasicType.VOID)
        self.assertEqual(function_type.arguments, [])

    def test_function_info_creation(self):
        function_info = FunctionInfo.from_params(
            name="sayHello",
            return_type=BasicType.VOID,
            modification=TypeModification.INLINE,
            body='std::cout << "Hello, " << name << std::endl;',
            arguments=[
                FunctionInfo.Argument.from_params(
                    name="name",
                    type=TypeExpression.from_params(
                        details=StubType("std::string"),
                        modification=TypeModification.CONST | TypeModification.REFERENCE
                    ),
                )
            ]
        )
        self.assertEqual(function_info.name, "sayHello")
        self.assertEqual(function_info.return_type, BasicType.VOID)
        self.assertEqual(len(function_info.arguments), 1)
        self.assertEqual(function_info.body, 'std::cout << "Hello, " << name << std::endl;')
        self.assertEqual(function_info.modification, TypeModification.INLINE)

    def test_externc_creation(self):
        extern_c = ExternC.from_params(
            content=[
                FunctionInfo.from_params(
                    name="foo",
                    return_type=BasicType.VOID,
                )
            ]
        )
        self.assertEqual(len(extern_c.content), 1)
        self.assertEqual(extern_c.allowed_namespaces, [])

    def test_enum_creation(self):
        my_enum = EnumInfo.from_params(
            name="betterLanguagesThanCpp",
            values=[
                EnumInfo.EnumValue.from_params(
                    name="Zig",
                    value=0,
                    is_default=True
                ),
                EnumInfo.EnumValue.from_params(
                    name="Rust",
                    value=1
                )
            ]
        )
        self.assertEqual(my_enum.name, "betterLanguagesThanCpp")
        self.assertEqual(my_enum.is_definition, True)
        self.assertEqual(my_enum.is_scoped, False)
        self.assertEqual(len(my_enum.values), 2)
        self.assertEqual(my_enum.is_declaration, False)

    def test_class_member_creation(self):
        class_member = ClassMember.from_params(
            access_specifier=AccessSpecifier.PROTECTED
        )
        self.assertEqual(class_member.access_specifier, AccessSpecifier.PROTECTED)

    def test_method_creation(self):
        method = MethodInfo.from_params(
            name="getName",
            return_type=StubType("std::string"),
            body="return name;"
        )
        self.assertEqual(method.name, "getName")
        self.assertEqual(method.return_type.name, "std::string")
        self.assertEqual(method.body, "return name;")

    def test_constructor_creation(self):
        constructor = ConstructorInfo.from_params(
            name="testConstructor",
            initializer_list=[
                ConstructorInfo.InitializerInfo("a", 10)
            ]
        )
        self.assertEqual(constructor.name, "testConstructor")
        self.assertEqual(len(constructor.initializer_list), 1)
        self.assertIsNone(constructor.return_type)

    def test_destructor_creation(self):
        destructor = DestructorInfo.from_params(
            name="testDestructor"
        )
        self.assertEqual(destructor.name, "testDestructor")
        self.assertEqual(destructor.type, MethodType.DESTRUCTOR)
        self.assertIsNone(destructor.return_type)

    def test_field_creation(self):
        field = FieldInfo.from_params(
            name="testField",
            associated_comment=Comment()
        )
        self.assertEqual(field.name, "testField")
        self.assertIsNotNone(field.associated_comment)

    def test_section_creation(self):
        parent = ClassInfo.from_params(name="testClass", is_class=True)
        section = SectionInfo.from_params(
            parent=parent,
            type=AccessSpecifier.PUBLIC,
        )
        self.assertEqual(section.type, AccessSpecifier.PUBLIC)
        self.assertEqual(section.is_unnamed, True)

    def test_inheritance_creation(self):
        inheritance = InheritanceInfo.from_params(
            type_parents=[
                InheritanceInfo.InheritanceValue.from_params(
                    access_specifier=AccessSpecifier.PUBLIC,
                    is_virtual=False
                )
            ]
        )
        self.assertIsNone(inheritance.parent)
        self.assertEqual(len(inheritance.type_parents), 1)

    def test_class_creation(self):
        parent = ClassInfo.from_params(
            name="testClass",
            is_class=True,
            is_definition=True
        )
        self.assertEqual(parent.name, "testClass")
        self.assertEqual(parent.is_definition, True)
        self.assertEqual(parent.is_class, True)

    def test_source_file_creation(self):
        source_file = SourceFile.from_params(
            type=SourceFileType.HEADER,
            header_guard="testHeaderGuard",
        )
        self.assertEqual(source_file.type, SourceFileType.HEADER)
        self.assertEqual(source_file.header_guard, "testHeaderGuard")

    def test_include_creation(self):
        include_info = IncludeInfo.from_params(
            value="string",
            is_standard=True
        )
        self.assertEqual(include_info.value, "string")
        self.assertEqual(include_info.is_standard, True)

    def test_concept_creation(self):
        concept_info = ConceptInfo.from_params(
            name="ConceptName",
            body="false"
        )
        self.assertEqual(concept_info.name, "ConceptName")
        self.assertEqual(concept_info.body, "false")
        self.assertIsNotNone(concept_info.template)

    def test_init_params(self):
        class A:
            @classmethod
            @init_params()
            def create(cls, value: int):
                return cls()

        class B(A):
            value: int = 0

        class C(B):
            @classmethod
            @init_params()
            def create(cls, value: int, name: Optional[str] = None):
                return cls()

        class D(C):
            def __init__(self):
                self._name = "name"

            @property
            def name(self) -> str:
                return self._name

            @name.setter
            def name(self, value: str):
                self._name = f"D_{value}"

        class E(D):
            @property
            def name(self) -> str:
                return "Always default"

        with self.subTest("Cases that should raise AttributeError"):
            self.assertRaises(AttributeError, A.create, value=10)
            self.assertRaises(AttributeError, C.create, value=5)
            self.assertRaises(AttributeError, E.create, value=10, name="test")

        with self.subTest("Cases that should succeed"):
            my_b = B.create(value=10)
            self.assertEqual(my_b.value, 10)

            my_d = D.create(value=5, name="test")
            self.assertEqual(my_d.name, "D_test")
            my_d.name = "test2"
            self.assertEqual(my_d.name, "D_test2")