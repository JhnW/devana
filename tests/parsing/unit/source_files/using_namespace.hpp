namespace foo
{
    void fnc1(int a);
    double fnc2(int a);
    namespace bar
    {
        int fnc3();
    }
}

using namespace foo;
using namespace foo::bar;