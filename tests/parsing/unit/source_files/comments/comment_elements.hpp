//test doc 1
void func_1();

/*test doc 2*/
void func_2();

/*
test doc 3.1
test doc 3.2
*/
void func_3();

//test 4.1
//test 4.2
//test 4.3
void func_4();

// test comment function basic
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
    Test doc for constructor
    */
    TestClassContent();

    //simple field doc
    TestClassContent *next;
};

enum TestCommentValue
{
    TET_VAL_1,
    /* test doc enum */
    TEST_VAL_2, //test doc bad
    TEST_VAL_3
};

//test concept comment
template<typename T>
concept TestConcept1 = true;

/*
Test more
complex comment
*/
template<typename T>
concept TestConcept2 = false;