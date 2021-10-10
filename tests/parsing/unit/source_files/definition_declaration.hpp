enum TestEnum;
class TestClass;
struct TestStruct;
double TestFunction(int a);
double TestFunction(double a);
union TestUnion;

enum TestEnum
{
    Val1
};

class TestClass
{
    double a;
};

struct TestStruct
{
    char b;
};

double TestFunction(int a)
{
    return 7.5*a;
}

double TestFunction(double a)
{
    return 2.5*a;
}

union TestUnion
{
    char a;
    double b;
};

double TestFunction(float a);
double TestFunction(char a)
{
    return 255.0*a;
}

namespace TestNamespace
{
    class TestClass
    {
        double x;
        char TestMethod();
    };

    double TestFunction(float a)
    {
        return a * 99.9f;
    }

   double TestFunction(double a);
};

class TestNamespace::TestClass;

double TestNamespace::TestFunction(float a);

double TestNamespace::TestFunction(double a)
{
    return a*a*0.25;
}

char TestNamespace::TestClass::TestMethod()
{
    return 120;
}

namespace TestNamespace2
{
    class TestClass2;
}
