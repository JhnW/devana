namespace foo1
{
    struct FooStruct1
    {
        double a;
        double b;
    };

    namespace bar1
    {
        struct BarStruct1
        {
            double a;
            double b;
        };
    }

}

namespace foo2
{
    struct FooStruct2
    {
        double a;
        double b;

        enum FooStructEnum
        {
            FooEnumVal1,
            FooEnumVal2
        };
    };

    enum FooEnum2
    {
        FooEnumVal1,
        FooEnumVal2
    };

    template<typename T>
    struct FooStructTemplate2
    {
        T *data;
        enum FooEnum3
        {
            FooEnumVal1,
            FooEnumVal2
        };
    };

    typedef const int c_int;
}

namespace foo3
{
    using namespace foo1::bar1;

    struct FooStruct1
    {
        double a;
        double b;
    };

    const BarStruct1* fooReturnFunction_1();
    const foo1::bar1::BarStruct1* fooReturnFunction_2();
    const foo2::FooStruct2::FooStructEnum* fooReturnFunction_3();
    const foo2::FooStructTemplate2<float>::FooEnum3* fooReturnFunction_4();
    foo2::c_int* fooReturnFunction_5();

    void fooArgFunction_1(const BarStruct1* a);
    void fooArgFunction_2(const foo1::bar1::BarStruct1* a);
    void fooArgFunction_3(const foo2::FooStruct2::FooStructEnum* a);
    void fooArgFunction_4(const foo2::FooStructTemplate2<float>::FooEnum3* a);
    void fooArgFunction_5(foo2::c_int* a);

    template<typename T>
    const foo2::FooStructTemplate2<T>::FooEnum3* fooReturnFunctionTemplate();

    template<typename T>
    void fooArgFunctionTemplate(const foo2::FooStructTemplate2<T>::FooEnum3* a)
    {
    }


    struct FieldsTest
    {
        const BarStruct1* a1;
        const foo1::bar1::BarStruct1* a2;
        const foo2::FooStruct2::FooStructEnum* a3;
        const foo2::FooStructTemplate2<float>::FooEnum3* a4;
        foo2::c_int* a5;
    };

    typedef const BarStruct1* typedefFoo1;
    typedef const foo1::bar1::BarStruct1* typedefFoo2;
    typedef const foo2::FooStruct2::FooStructEnum* typedefFoo3;
    typedef const foo2::FooStructTemplate2<float>::FooEnum3* typedefFoo4;
    typedef foo2::c_int* typedefFoo5;

    template<typename T>
    void templateSpeFunc(T a) {}

    template<>
    void templateSpeFunc<const foo2::FooStruct2*>(const foo2::FooStruct2* a) {}

    template<typename T>
    struct templateSpecStruct
    {
        T a;
    };

    template<>
    struct templateSpecStruct<const foo2::FooStruct2>
    {
        const foo2::FooStruct2* b;
    };

    struct structChild: foo2::FooStruct2
    {
        float w;
    };
}

namespace foo1
{
    double splitFunction(int a, int b);
}

struct TheSameName
{
    int a;
};

namespace TheSameNameNamespace
{
    struct TheSameName
    {
        double x;
    };

    namespace TheSameNameNamespace2
    {
        struct TheSameName
        {
            double x;
        };
    }
}

void testTheSameNameFunc(const TheSameName& arg);
void testTheSameNameNamespaceFunc(const TheSameNameNamespace::TheSameName& arg);
void testTheSameNameTwoNamespaceFunc(const TheSameNameNamespace::TheSameNameNamespace2::TheSameName& arg);

TheSameName testTheSameNameFuncReturn();
TheSameNameNamespace::TheSameName testTheSameNameNamespaceFuncReturn();
TheSameNameNamespace::TheSameNameNamespace2::TheSameName ttestTheSameNameTwoNamespaceFuncReturn();

class ClassTestNamespaceDeductionTheSameName1: public TheSameName
{
};

class ClassTestNamespaceDeductionTheSameName2: public TheSameNameNamespace::TheSameName
{
};

class ClassTestNamespaceDeductionTheSameName3: public TheSameNameNamespace::TheSameNameNamespace2::TheSameName
{
};