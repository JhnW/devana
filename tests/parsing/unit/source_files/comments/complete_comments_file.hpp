/*
 * t1
 * t2
 * t3
 * t4
*/

//test comment function
int foo_1();

//test comment function template
template<typename T>
T fooTemplate(const T& arg)
{
    return T(arg);
}

//test comment function template spec
template<>
double fooTemplate(const double& arg)
{
    return arg*0.25f;
}

//test comment class basic
struct StructFoo
{

};

//test comment class template
template<typename T>
struct StructFooTemplate
{
    T* a;
};

//test comment namespace
namespace TestNamespace
{

}

//test comment global var
float global_var;

//test comment enum
enum TestEnum
{
    VAL_ENUM_1,
    VAL_ENUM_2
};

//test comment union
union UnionFoo
{
    char a;
    int b;
};

//test comment typedef
typedef UnionTypedef UnionFoo;

class TestClassContent
{
public:
    /*
    Test doc for constructor 1
    Test doc for constructor 2
    */
    TestClassContent();

    void TestMethod();

    //simple field doc
    TestClassContent *next;
};

enum TestCommentValue
{
    TET_VAL_1,
    /*test doc enum*/
    TEST_VAL_2, //test doc bad
    TEST_VAL_3
};
