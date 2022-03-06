extern "C" void foo();
extern "C" double foo2(int a)
{
    return a*0.5;
}
extern "C" {
    void foo3();
    double foo4(int a)
    {
        return a*0.5;
    }
}

namespace ExternNamespace {

extern "C" float namespace_func();

}


float ExternNamespace::namespace_func() {
    return 7.5f;
}