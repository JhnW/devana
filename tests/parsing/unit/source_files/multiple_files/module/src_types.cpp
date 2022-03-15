#include "inc_types.hpp"

static Parent variable;
static TestNamespace::Parent variable_namespace;

void test_function_arg(const Parent& arg);
Parent test_function_return();
void test_function_arg_namespace(const TestNamespace::Parent& arg);
TestNamespace::Parent test_function_return_namespace();
TestNamespace::TestInnerNamespace::Parent test_function_return_namespace_deep();

class TestClass1: public Parent
{
};

class TestClass2: public TestNamespace::Parent
{
};

class TestClass3: virtual public TestNamespace::Parent
{
};